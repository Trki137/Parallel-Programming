import numpy as np
import pyopencl as cl

jacoby_step_kernel_code = """
__kernel void jacobi_step(__global float *psinew, __global float *psi, int m, int n) {
    int i = get_global_id(0) + 1;
    int j = get_global_id(1) + 1;

    if (i <= m && j <= n) {
        psinew[i * (n + 2) + j] = 0.25f * (psi[(i - 1) * (n + 2) + j] + 
                                           psi[(i + 1) * (n + 2) + j] + 
                                           psi[i * (n + 2) + j - 1] + 
                                           psi[i * (n + 2) + j + 1]); 
    } 
}
"""
platform = cl.get_platforms()[0]
device = platform.get_devices()[0]
context = cl.Context([device])
queue = cl.CommandQueue(context)

program = cl.Program(context, jacoby_step_kernel_code).build()
jacobi_step_kernel = program.jacobi_step


def jacobi_step_opencl(psi_new, psi, m, n):
    mf = cl.mem_flags
    psi_buf = cl.Buffer(context, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=psi)
    psi_new_buf = cl.Buffer(context, mf.WRITE_ONLY, psi_new.nbytes)

    global_size = (m, n)
    local_size = None
    jacobi_step_kernel(queue, global_size, local_size, psi_new_buf, psi_buf, np.int32(m), np.int32(n))
    queue.finish()
    cl.enqueue_copy(queue, psi_new, psi_new_buf).wait()


def jacobi_step(psi_new, psi, m, n):
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            psi_new[i, j] = 0.25 * (psi[i - 1, j] + psi[i + 1, j] + psi[i, j - 1] + psi[i, j + 1])


def delta_sq(new_arr, old_arr, m, n):
    dsq = 0.0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            tmp = new_arr[i, j] - old_arr[i, j]
            dsq += tmp * tmp
    return dsq
