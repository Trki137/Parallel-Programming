import pyopencl as cl
import numpy as np
import time

from util import csv_results

kernel_code = """
__kernel void calculate_pi(__global float *partial_sums, int n) {
    int gid = get_global_id(0);
    int num_work_items = get_global_size(0);

    float h = 1.0f / (float)n;
    float sum = 0.0f;
    float x;

    for (int i = gid + 1; i <= n; i += num_work_items) {
        x = h * ((float)i - 0.5f);
        sum += 4.0f / (1.0f + x * x);
    }

    partial_sums[gid] = sum * h;
}
"""

platform = cl.get_platforms()[0]
device = platform.get_devices()[0]
context = cl.Context([device])
queue = cl.CommandQueue(context, device)

program = cl.Program(context, kernel_code).build()
kernel = program.calculate_pi


def calculate_pi_opencl(n, gs, ls):
    partial_sums = np.zeros(gs, dtype=np.float32)
    partial_sums_buf = cl.Buffer(context, cl.mem_flags.WRITE_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=partial_sums)

    kernel.set_args(partial_sums_buf, np.int32(n))

    cl.enqueue_nd_range_kernel(queue, kernel, (gs,), (ls,))
    queue.finish()

    cl.enqueue_copy(queue, partial_sums, partial_sums_buf).wait()
    return np.sum(partial_sums)


if __name__ == '__main__':
    N = int(2 ** 27)
    global_sizes = [2 ** 6, 2 ** 7, 2 ** 8, 2 ** 9, 2 ** 10, 2 ** 11, 2 ** 12, 2 ** 13, 2 ** 14]
    local_sizes = [2 ** 3, 2 ** 4, 2 ** 5, 2 ** 6]

    results = []

    for global_size in global_sizes:
        for local_size in local_sizes:
            if global_size % local_size == 0:
                start_time = time.time()
                calculate_pi_opencl(N, global_size, local_size)
                elapsed_time = time.time() - start_time
                data = {
                    'N': N,
                    'time': elapsed_time,
                    'L': local_size,
                    'M': global_size
                }
                csv_results("results.csv", data)
