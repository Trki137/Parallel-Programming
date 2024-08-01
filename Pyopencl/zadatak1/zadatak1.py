import pyopencl as cl
import numpy as np
import time
import csv

kernel_code = """
__kernel void count_primes(__global int *data, __global int *count, int n) {
    int gid = get_global_id(0);
    int local_count = 0;

    for (int i = gid; i < n; i += get_global_size(0)) {
        int num = data[i];
        if (num <= 1) continue;
        int prime = 1;
        for (int j = 2; j * j <= num; j++) {
            if (num % j == 0) {
                prime = 0;
                break;
            }
        }
        if (prime) local_count++;
    }

    atomic_add(count, local_count);
}
"""

kernel_code_non_atomic = """
__kernel void count_primes(__global int *data, __global int *count, int n) {
    int gid = get_global_id(0);
    int local_count = 0;

    for (int i = gid; i < n; i += get_global_size(0)) {
        int num = data[i];
        if (num <= 1) continue;
        int prime = 1;
        for (int j = 2; j * j <= num; j++) {
            if (num % j == 0) {
                prime = 0;
                break;
            }
        }
        if (prime) local_count++;
    }

    count[0] += local_count;
}
"""


def create_array(size, random=False):
    if random:
        return np.random.randint(1, 100000, size).astype(np.int32)
    else:
        return np.arange(1, size + 1).astype(np.int32)


# Main program
def main():
    platform = cl.get_platforms()[0]
    device = platform.get_devices()[0]
    context = cl.Context([device])
    queue = cl.CommandQueue(context)

    N = 2 ** 20
    data = create_array(N, random=True)

    mf = cl.mem_flags
    data_buf = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data)
    count_buf = cl.Buffer(context, mf.WRITE_ONLY, 4)

    program = cl.Program(context, kernel_code).build()
    kernel = program.count_primes

    G_values = [2 ** x for x in range(12, 21)]
    L_values = [2 ** x for x in range(0, 8)]

    max_work_group_size = kernel.get_work_group_info(cl.kernel_work_group_info.WORK_GROUP_SIZE, device)
    print(f"Max work group size: {max_work_group_size}")

    best_time = float('inf')
    best_G, best_L = None, None

    with open('proba.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["G", "L", "Time (s)", "Primes"])

        for G in G_values:
            for L in L_values:
                if G % L != 0 or L > max_work_group_size:
                    continue

                try:
                    count = np.zeros(1, dtype=np.int32)
                    cl.enqueue_copy(queue, count_buf, count)

                    kernel.set_args(data_buf, count_buf, np.int32(N))
                    start_time = time.time()
                    cl.enqueue_nd_range_kernel(queue, kernel, (G,), (L,))
                    queue.finish()
                    end_time = time.time()

                    cl.enqueue_copy(queue, count, count_buf)
                    queue.finish()
                    elapsed_time = end_time - start_time

                    if elapsed_time < best_time:
                        best_time = elapsed_time
                        best_G, best_L = G, L

                    print(f"G: {G}, L: {L}, Time: {elapsed_time:.6f} seconds, Primes: {count[0]}")
                    # writer.writerow([G, L, elapsed_time, count[0]])
                except cl.RuntimeError as e:
                    print(f"Failed for G: {G}, L: {L} with error: {e}")

    print(f"Best configuration: G={best_G}, L={best_L}, Time={best_time:.6f} seconds")


if __name__ == "__main__":
    main()
