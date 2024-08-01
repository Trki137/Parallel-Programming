import time
from util import csv_results

PI_25_DEC = 3.141592653589793238462643

if __name__ == "__main__":
    N = int(2 ** 30)
    h = 1.0 / N
    total_sum = 0.0
    start_time = time.time()
    for i in range(N):
        x = h * (i - 0.5)
        total_sum += 4.0 / (1.0 + x ** 2)
    end_time = time.time()
    elapsed_time = end_time - start_time

    pi = h * total_sum
    print(pi)
    print(f"Difference -> {abs(PI_25_DEC - pi)}")
    data = {
        'N': N,
        'time': elapsed_time,
        'L': None,
        'M': None
    }
    csv_results("results.csv", data)
