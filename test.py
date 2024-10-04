import threading
import time
import math
from concurrent.futures import ThreadPoolExecutor, as_completed

def exec_with_threads(f, args, nt, max_retries=5):
    def worker(sub_args):
        for arg in sub_args:
            retries = 0
            while retries <= max_retries:
                try:
                    result = f(*arg)
                    if result:  # Assuming a truthy return value means success
                        break
                except Exception as e:
                    pass
                retries += 1
                time.sleep(0.2 * 1.5 ** retries)  # Exponential backoff

    # Split args into nt sublists
    args_per_thread = math.ceil(len(args) / nt)
    sublists = [args[i:i + args_per_thread] for i in range(0, len(args), args_per_thread)]

    with ThreadPoolExecutor(max_workers=nt) as executor:
        executor.map(worker, sublists)

# Example usage
if __name__ == "__main__":
    def sample_function(x, y):
        if x + y > 5:
            return True
        else:
            raise ValueError("Sum must be greater than 5")
        
    args = [(1, 2), (3, 4), (5, 6), (7, 8)]
    exec_with_threads(sample_function, args, 2)
