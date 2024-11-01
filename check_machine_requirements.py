import sys
import subprocess
import json

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
            verified_status = offer.get('verified', 'unknown')

            # Check each requirement and add to the list if not met
            if cuda_version < 12.4:
                unmet_reasons.append(f"CUDA version is {cuda_version} (required >= 12.4)")
            if reliability <= 0.90:
                unmet_reasons.append(f"Reliability is {reliability} (required > 0.90)")
            if direct_ports <= 3:
                unmet_reasons.append(f"Direct port count is {direct_ports} (required > 3)")
            if pcie_bandwidth <= 2.9:
                unmet_reasons.append(f"PCIe bandwidth is {pcie_bandwidth} (required > 2.85)")
            if inet_down_speed <= 10:
                unmet_reasons.append(f"Internet download speed is {inet_down_speed} Mb/s (required > 10 Mb/s)")
            if inet_up_speed <= 10:
                unmet_reasons.append(f"Internet upload speed is {inet_up_speed} Mb/s (required > 10 Mb/s)")
            if gpu_ram <= 7:
                unmet_reasons.append(f"GPU RAM is {gpu_ram} GB (required > 7 GB)")

    if len(unmet_reasons) == 0:
        print(f"Machine ID {machine_id} meets all the requirements.")
        sys.exit(0)
    else:
        print(f"Machine ID {machine_id} does not meet the requirements:")
        for reason in unmet_reasons:
            print(f"- {reason}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <machine_id>")
        sys.exit(1)

    machine_id = sys.argv[1]
    check_requirements(machine_id)
