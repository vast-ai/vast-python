import subprocess
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from datetime import datetime
from tqdm import tqdm
import time

def run_vast_search():
    cmd = ['./vast', 'search', 'offers', '--limit', '65535', 'verified=any', '--raw']
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = result.stdout
        return json.loads(output)
    except Exception as e:
        print(f"Error running vast search: {e}")
        return []

def get_unverified_offers(offers):
    verified_machine_ids = set()
    for offer in offers:
        if offer.get('verification') == 'verified':
            verified_machine_ids.add(offer.get('machine_id'))

    unverified_offers = [
        offer for offer in offers
        if offer.get('verification') == 'unverified' and offer.get('machine_id') not in verified_machine_ids
    ]
    return unverified_offers

def get_best_offers(offers):
    best_offers = {}
    for offer in offers:
        machine_id = offer.get('machine_id')
        dlperf = offer.get('dlperf', 0)
        if machine_id not in best_offers or dlperf > best_offers[machine_id].get('dlperf', 0):
            best_offers[machine_id] = offer
    return best_offers

def test_machine(machine_id):
    cmd = ['./vast.py', 'self-test', 'machine', str(machine_id), '--raw']
    retries = 3
    
    for attempt in range(retries):
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout.strip()
            
            # Check for 429 in the stderr output
            if "429" in result.stderr:
                if attempt < retries - 1:
                    print(f"429 Too Many Requests for machine {machine_id}. Retrying in 1 second... (Attempt {attempt + 1}/{retries})")
                    time.sleep(1)
                    continue
                else:
                    return (machine_id, 'failure', "Too Many Requests: 429 error after 3 retries")

            # Parse JSON output
            data = json.loads(output)
            if data.get('success'):
                return (machine_id, 'success', '')
            else:
                reason = data.get('reason', 'Unknown reason')
                return (machine_id, 'failure', reason)
        
        except json.JSONDecodeError:
            error_message = result.stderr.strip() or output
            return (machine_id, 'failure', f"Invalid JSON output or error message: {error_message}")
        
        except Exception as e:
            return (machine_id, 'failure', f"Exception occurred: {e}")
    
    # If it exhausts retries without success
    return (machine_id, 'failure', "Request failed after 3 retries")

def process_machine_ids(machine_ids):
    successes = []
    failures = []
    total_machines = len(machine_ids)
    counter = {'processed': 0, 'passed': 0, 'failed': 0}
    lock = threading.Lock()
    
    print(f"Starting self-tests on {total_machines} machines...")
    
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = {executor.submit(test_machine, mid): mid for mid in machine_ids}
        for future in as_completed(futures):
            machine_id, status, reason = future.result()
            with lock:
                counter['processed'] += 1
                remaining = total_machines - counter['processed']
                if status == 'success':
                    successes.append(machine_id)
                    counter['passed'] += 1
                else:
                    failures.append((machine_id, reason))
                    counter['failed'] += 1
                print('\033[2K\033[1G', end='')  # Clear the entire line and move the cursor to the beginning
                print(f"Processed {counter['processed']}/{total_machines} - Passed: {counter['passed']}, Failed: {counter['failed']}, Remaining: {remaining}", end='\r')
    print()  # Move to the next line after progress updates
    return successes, failures

def save_results(successes, failures):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save passed machines
    with open('passed_machines.txt', 'w') as f:
        f.write(f"{current_time}\n")  # Add the date and time
        f.write(','.join(str(mid) for mid in successes) + "\n")  # Comma-separated machine IDs

    # Save failed machines
    with open('failed_machines.txt', 'w') as f:
        f.write(f"{current_time}\n")  # Add the date and time
        for mid, reason in failures:
            f.write(f"{mid}: {reason}\n")  # Machine ID and reason per line

def main():
    offers = run_vast_search()
    if not offers:
        print("No offers found.")
        return
    unverified_offers = get_unverified_offers(offers)
    best_offers = get_best_offers(unverified_offers)
    machine_ids = list(best_offers.keys())

    print(f"Found {len(machine_ids)} unverified machine IDs to test.")

    if not machine_ids:
        print("No unverified machines to test.")
        return

    successes, failures = process_machine_ids(machine_ids)
    save_results(successes, failures)

    print("\nPassed Machine IDs:")
    for mid in successes:
        print(mid)

    print("\nFailed Machine IDs and Reasons:")
    for mid, reason in failures:
        print(f"{mid}: {reason}")

    print(f"\nResults saved to 'passed_machines.txt' and 'failed_machines.txt'.")

if __name__ == '__main__':
    main()
