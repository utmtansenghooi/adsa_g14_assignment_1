from datetime import datetime
import time

def log_operation(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")  # prints to console
    with open("customer_log.txt", "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def timed_operation(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    duration = end - start
    return result, duration