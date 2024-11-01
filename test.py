import sys
import subprocess
import json
import time
import argparse

def check_requirements(machine_id):
    unmet_reasons = []

    # Build the command
    cmd = ['./vast', 'search', 'offers', f"machine_id={machine_id} verified=any rentable=true", '--raw']
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd)}")
        print(e.stderr)
        sys.exit(1)

    if output == '[]':
        unmet_reasons.append(f"Machine ID {machine_id} not found or not rentable. Please ensure the machine is listed and not rented on demand.")
    else:
        # Parse the JSON output
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            print(f"Error parsing JSON output from command: {' '.join(cmd)}")
            print(output)
            sys.exit(1)

        if not data:
            unmet_reasons.append(f"Machine ID {machine_id} not found or not rentable. Please ensure the machine is listed and not rented on demand.")
        else:
            # Extract the relevant fields from the first element
            offer = data[0]
            cuda_version = float(offer.get('cuda_max_good', 0))
            reliability = float(offer.get('reliability', 0))
            direct_ports = int(offer.get('direct_port_count', 0))
            pcie_bandwidth = float(offer.get('pcie_bw', 0))
            inet_down_speed = float(offer.get('inet_down', 0))
            inet_up_speed = float(offer.get('inet_up', 0))
            gpu_ram = float(offer.get('gpu_ram', 0))

            # Check each requirement and add to the list if not met
            if cuda_version < 12.4:
                unmet_reasons.append(f"CUDA version is {cuda_version} (required >= 12.4)")
            if reliability <= 0.90:
                unmet_reasons.append(f"Reliability is {reliability} (required > 0.90)")
            if direct_ports <= 3:
                unmet_reasons.append(f"Direct port count is {direct_ports} (required > 3)")
            if pcie_bandwidth <= 2.85:
                unmet_reasons.append(f"PCIe bandwidth is {pcie_bandwidth} (required > 2.85)")
            if inet_down_speed <= 10:
                unmet_reasons.append(f"Internet download speed is {inet_down_speed} Mb/s (required > 10 Mb/s)")
            if inet_up_speed <= 10:
                unmet_reasons.append(f"Internet upload speed is {inet_up_speed} Mb/s (required > 10 Mb/s)")
            if gpu_ram <= 7:
                unmet_reasons.append(f"GPU RAM is {gpu_ram} MB (required > 7 GB)")

    if len(unmet_reasons) == 0:
        print(f"Machine ID {machine_id} meets all the requirements.")
        return True
    else:
        print(f"Machine ID {machine_id} does not meet the requirements:")
        for reason in unmet_reasons:
            print(f"- {reason}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Test Script')
    parser.add_argument('machine_id', help='Machine ID')
    parser.add_argument('--debugging', action='store_true', help='Enable debugging output')

    args = parser.parse_args()

    machine_id = args.machine_id
    debugging = args.debugging

    # Call check_requirements before proceeding
    if not check_requirements(machine_id):
        sys.exit(1)  # Exit if requirements are not met

    # Step 1: Search offers based on the machine_id
    search_cmd = ['./vast', 'search', 'offers', f"machine_id={machine_id}", 'verified=any' ,'--raw']
    result = subprocess.run(search_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error running command: {' '.join(search_cmd)}")
        print(result.stderr)
        sys.exit(1)

    try:
        offers = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON output from command: {' '.join(search_cmd)}")
        print(e)
        sys.exit(1)

    if not offers:
        print(f"No offers found for machine_id {machine_id}")
        sys.exit(1)

    # Step 2: Pick an offer (e.g., the first one)
    offer = offers[0]
    ask_contract_id = offer['ask_contract_id']

   # Step 3: Create the instance using the selected offer
    create_cmd = [
        './vast', 'create', 'instance', str(ask_contract_id),
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
        sys.exit(1)

    try:
        instance_info = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON output from command: {' '.join(create_cmd)}")
        print(e)
        sys.exit(1)

    # Adjusted to get 'instance_id' from 'new_contract'
    instance_id = instance_info.get('new_contract')
    if not instance_id:
        print("Could not get instance ID from create instance output.")
        sys.exit(1)

    # Step 4: Wait for the instance to start up
    def wait_for_instance(instance_id, timeout=300, interval=10):
        start_time = time.time()
        while time.time() - start_time < timeout:
            cmd = ['./vast', 'show', 'instance', str(instance_id), '--raw']
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(f"Error running command: {' '.join(cmd)}")
                print(result.stderr)
                return False
            try:
                instance_info = json.loads(result.stdout)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON output from command: {' '.join(cmd)}")
                print(e)
                return False
            intended_status = instance_info.get('intended_status', 'unknown')
            actual_status = instance_info.get('actual_status', 'unknown')
            if intended_status == 'running' and actual_status == 'running':
                return instance_info
            else:
                print(f"Instance {instance_id} status: intended={intended_status}, actual={actual_status}. Waiting...")
                time.sleep(interval)
        print(f"Instance {instance_id} did not become running within {timeout} seconds.")
        return False

    instance_info = wait_for_instance(instance_id)
    if not instance_info:
        print("Instance did not start properly.")
        sys.exit(1)

    # Step 5: Get the IP address, port, machine_id, and delay
    # Get the public_ipaddr from instance_info
    ip_address = instance_info.get('public_ipaddr')
    if not ip_address:
        print("Could not get IP address from instance info.")
        sys.exit(1)

    # Get the port mapping for port 5000
    ports = instance_info.get('ports', {})
    port_mappings = ports.get('5000/tcp', [])
    if not port_mappings:
        print("Could not find port mapping for port 5000.")
        sys.exit(1)
    # Assuming the first mapping
    port = port_mappings[0].get('HostPort')
    if not port:
        print("Could not get host port for port 5000.")
        sys.exit(1)

    delay = '15'    # You can adjust this as needed

    # Step 6: Start machinetester.py with the obtained parameters
    machinetester_cmd = [
        'python3', 'machinetester.py', ip_address, port, str(instance_id), machine_id, delay
    ]
    if debugging:
        machinetester_cmd.append('--debugging')

    print(f"Starting machinetester.py with command: {' '.join(machinetester_cmd)}")
    subprocess.run(machinetester_cmd)

if __name__ == '__main__':
    main()
