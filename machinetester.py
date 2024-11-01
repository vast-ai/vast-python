import sys
import subprocess
import time
import json
import argparse
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def is_non_negative_integer(s):
    return s.isdigit()

def is_instance(instance_id, debugging=False):
    retry_count = 0
    max_retries = 3

    while retry_count < max_retries:
        try:
            result = subprocess.run(['./vast', 'show', 'instance', instance_id, '--raw'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            json_output = result.stdout.strip()
            if debugging:
                print(f"is_instance(): Output from vast show instance: {json_output}")
            # Break the loop if command is successful
            break
        except subprocess.CalledProcessError as e:
            if debugging:
                print(f"is_instance(): Error running vast show instance: {e}")
                print(f"is_instance(): stderr: {e.stderr}")
            # Increment the retry count
            retry_count += 1
            if retry_count == max_retries:
                return 'unknown'

    try:
        data = json.loads(json_output)
        intended_status = data.get('intended_status', 'unknown')
        if debugging:
            print(f"is_instance(): Intended status: {intended_status}")
    except json.JSONDecodeError as e:
        if debugging:
            print(f"is_instance(): JSON decode error: {e}")
            print(f"is_instance(): json_output: {json_output}")
        return 'unknown'

    if intended_status in ['running', 'offline', 'exited', 'created']:
        return intended_status
    else:
        return 'unknown'

def main():
    parser = argparse.ArgumentParser(description='Machine Tester Script')
    parser.add_argument('IP', help='IP address')
    parser.add_argument('PORT', help='Port number')
    parser.add_argument('instances_id', help='Instance ID')
    parser.add_argument('machine_id', help='Machine ID')
    parser.add_argument('delay', help='Startup delay (non-negative integer)')
    parser.add_argument('--debugging', action='store_true', help='Enable debugging output')

    args = parser.parse_args()

    IP = args.IP
    PORT = args.PORT
    instances_id = args.instances_id
    machine_id = args.machine_id
    delay = args.delay
    debugging = args.debugging

    if not is_non_negative_integer(delay):
        print(f"Usage: {sys.argv[0]} <IP> <Port> <instances_id> <machine_id> <startup delay> [--debugging]")
        with open("Error_testresults.log", "a") as f:
            f.write(f"{machine_id}:{instances_id} usage error \n")
        sys.exit(1)

    delay = int(delay)

    # Validate the delay variable
    if delay > 0:
        if debugging:
            print(f"Sleeping for {delay} seconds before starting tests.")
        time.sleep(delay)

    start_time = time.time()
    no_response_seconds = 0
    printed_lines = set()

    while time.time() - start_time < 300:
        try:
            if debugging:
                print(f"Sending GET request to https://{IP}:{PORT}/progress")
            response = requests.get(f'https://{IP}:{PORT}/progress', verify=False, timeout=10)
            message = response.text.strip()
            if debugging:
                print(f"Received message: '{message}'")
        except requests.exceptions.RequestException as e:
            if debugging:
                print(f"Error making HTTPS request: {e}")
            message = ''

        # Process the message
        if message:
            lines = message.split('\n')
            new_lines = [line for line in lines if line not in printed_lines]
            for line in new_lines:
                if line == 'DONE':
                    print("Test completed successfully.")
                    with open("Pass_testresults.log", "a") as f:
                        f.write(f"{machine_id}\n")
                    if debugging:
                        print(f"Test passed. Destroying instance {instances_id}.")
                    subprocess.run(['./vast', 'destroy', 'instance', instances_id])
                    sys.exit(0)
                elif line.startswith('ERROR'):
                    print(line)
                    with open("Error_testresults.log", "a") as f:
                        f.write(f"{machine_id}:{instances_id} {line}\n")
                    if debugging:
                        print(f"Test failed with error: {line}. Destroying instance {instances_id}.")
                    subprocess.run(['./vast', 'destroy', 'instance', instances_id])
                    sys.exit(1)
                else:
                    print(line)
                printed_lines.add(line)
            no_response_seconds = 0  # Reset if a response is received
        else:
            no_response_seconds += 20
            if debugging:
                print(f"No message received. Incremented no_response_seconds to {no_response_seconds}.")

        # Check instance status using is_instance function
        status = is_instance(instances_id, debugging)
        if debugging:
            print(f"Instance {instances_id} status: {status}")

        if status == 'running':
            # If no response for 60 seconds with running instance, log and exit
            if no_response_seconds >= 60:
                with open("Error_testresults.log", "a") as f:
                    f.write(f"{machine_id}:{instances_id} No response from port {PORT} for 60s with running instance\n")
                if debugging:
                    print(f"No response for 60s with running instance. Destroying instance {instances_id}.")
                subprocess.run(['./vast', 'destroy', 'instance', instances_id])
                sys.exit(1)
        else:
            # Handle other statuses (offline, exited, created, unknown)
            with open("Error_testresults.log", "a") as f:
                f.write(f"{machine_id}:{instances_id} Instance status '{status}' during testing.\n")
            if debugging:
                print(f"Instance {instances_id} status '{status}'. Destroying instance.")
            subprocess.run(['./vast', 'destroy', 'instance', instances_id])
            sys.exit(1)

        # Wait for 20 seconds before the next iteration
        if debugging:
            print("Waiting for 20 seconds before the next check.")
        time.sleep(20)

    # Destroy the instance after the loop completes if it was running
    if debugging:
        print(f"Time limit reached. Destroying instance {instances_id}.")
    else:
        print(f"Time limit reached. Destroying instance {instances_id}.")
    subprocess.run(['./vast', 'destroy', 'instance', instances_id])

    print(f"Machine: {machine_id} Done with testing remote.py results {message}")

if __name__ == '__main__':
    main()
