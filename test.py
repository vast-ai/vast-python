import sys
import subprocess
import json
import time
import argparse

# Global variable to store instance ID
instance_id = None

def destroy_instance():
    """Destroy the instance if it exists."""
    global instance_id
    if instance_id:
        print(f"Destroying instance {instance_id} before exit.")
        subprocess.run(['./vast.py', 'destroy', 'instance', str(instance_id)])
        instance_id = None  # Clear instance_id after destroying

def check_requirements(machine_id):
    unmet_reasons = []
    cmd = ['./vast.py', 'search', 'offers', f"machine_id={machine_id} verified=any rentable=true", '--raw']
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd)}")
        print(e.stderr)
        destroy_instance()
        sys.exit(1)

    if output == '[]':
        unmet_reasons.append(f"Machine ID {machine_id} not found or not rentable.")
    else:
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            print(f"Error parsing JSON output from command: {' '.join(cmd)}")
            print(output)
            destroy_instance()
            sys.exit(1)

        if not data:
            unmet_reasons.append(f"Machine ID {machine_id} not found or not rentable.")
        else:
            offer = data[0]
            # Checking each requirement and adding to the list if not met
            if float(offer.get('cuda_max_good', 0)) < 12.4:
                unmet_reasons.append("CUDA version < 12.4")
            if float(offer.get('reliability', 0)) <= 0.90:
                unmet_reasons.append("Reliability <= 0.90")
            if int(offer.get('direct_port_count', 0)) <= 3:
                unmet_reasons.append("Direct port count <= 3")
            if float(offer.get('pcie_bw', 0)) <= 2.85:
                unmet_reasons.append("PCIe bandwidth <= 2.85")
            if float(offer.get('inet_down', 0)) <= 10:
                unmet_reasons.append("Download speed <= 10 Mb/s")
            if float(offer.get('inet_up', 0)) <= 10:
                unmet_reasons.append("Upload speed <= 10 Mb/s")
            if float(offer.get('gpu_ram', 0)) <= 7:
                unmet_reasons.append("GPU RAM <= 7 GB")

    if unmet_reasons:
        print(f"Machine ID {machine_id} does not meet the requirements:")
        for reason in unmet_reasons:
            print(f"- {reason}")
        destroy_instance()
        sys.exit(1)
    else:
        print(f"Machine ID {machine_id} meets all the requirements.")
        return True

def main():
    global instance_id
    parser = argparse.ArgumentParser(description='Test Script')
    parser.add_argument('machine_id', help='Machine ID')
    parser.add_argument('--debugging', action='store_true', help='Enable debugging output')
    args = parser.parse_args()

    machine_id = args.machine_id
    debugging = args.debugging

    if not check_requirements(machine_id):
        sys.exit(1)

    # Search offers based on the machine_id
    search_cmd = ['./vast.py', 'search', 'offers', f"machine_id={machine_id}", 'verified=any', '--raw']
    result = subprocess.run(search_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error running command: {' '.join(search_cmd)}")
        print(result.stderr)
        destroy_instance()
        sys.exit(1)

    try:
        offers = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Error parsing JSON output from command: {' '.join(search_cmd)}")
        destroy_instance()
        sys.exit(1)

    if not offers:
        print(f"No offers found for machine_id {machine_id}")
        destroy_instance()
        sys.exit(1)

    offer = offers[0]
    ask_contract_id = offer['ask_contract_id']

    # Create the instance
    create_cmd = [
        './vast.py', 'create', 'instance', str(ask_contract_id),
        '--image', 'jjziets/vasttest:latest',
        '--ssh',
        '--direct',
        '--env', '-e TZ=PDT -e XNAME=XX4 -p 5000:5000',
        '--disk', '20',
        '--onstart-cmd', 'python3 remote.py',
        '--raw'
    ]

    result = subprocess.run(create_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error running command: {' '.join(create_cmd)}")
        print(result.stderr)
        destroy_instance()
        sys.exit(1)

    try:
        instance_info = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Error parsing JSON output from command: {' '.join(create_cmd)}")
        destroy_instance()
        sys.exit(1)

    instance_id = instance_info.get('new_contract')
    if not instance_id:
        print("Could not get instance ID from create instance output.")
        destroy_instance()
        sys.exit(1)

    # Wait for the instance to start up
    def wait_for_instance(instance_id, timeout=900, interval=10):
        start_time = time.time()
        while time.time() - start_time < timeout:
            cmd = ['./vast.py', 'show', 'instance', str(instance_id), '--raw']
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(f"Error running command: {' '.join(cmd)}")
                print(result.stderr)
                return False
            try:
                instance_info = json.loads(result.stdout)
            except json.JSONDecodeError:
                print(f"Error parsing JSON output from command: {' '.join(cmd)}")
                return False
            if instance_info.get('intended_status') == 'running' and instance_info.get('actual_status') == 'running':
                return instance_info
            print(f"Instance {instance_id} status: waiting...")
            time.sleep(interval)
        print(f"Instance {instance_id} did not become running within {timeout} seconds.")
        return False

    # Main execution with a try-finally block to ensure cleanup
    try:
        instance_info = wait_for_instance(instance_id)
        if not instance_info:
            print("Instance did not start properly.")
            destroy_instance()
            sys.exit(1)
        
        # Obtain IP and Port information, assuming success up to this point
        ip_address = instance_info.get('public_ipaddr')
        if not ip_address:
            print("Could not get IP address from instance info.")
            destroy_instance()
            sys.exit(1)
        
        port_mappings = instance_info.get('ports', {}).get('5000/tcp', [])
        if not port_mappings:
            print("Could not find port mapping for port 5000.")
            destroy_instance()
            sys.exit(1)
        
        port = port_mappings[0].get('HostPort')
        if not port:
            print("Could not get host port for port 5000.")
            destroy_instance()
            sys.exit(1)
        
        # Start machinetester.py
        delay = '15'
        machinetester_cmd = ['python3', 'machinetester.py', ip_address, port, str(instance_id), machine_id, delay]
        if debugging:
            machinetester_cmd.append('--debugging')
        print(f"Starting machinetester.py with command: {' '.join(machinetester_cmd)}")
        subprocess.run(machinetester_cmd)

    finally:
        destroy_instance()

if __name__ == '__main__':
    main()
