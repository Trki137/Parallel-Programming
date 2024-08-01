import time

import numpy as np

from util import csv_results_task_3
from zadatak3.array_allocation import array_malloc_2d
from zadatak3.boundary import boundary_psi
from zadatak3.jacoby import jacobi_step, delta_sq, jacobi_step_opencl


def main():
    print_freq = 100
    tolerance = 0.0
    check_err = tolerance > 0
    scale_factor = 64
    num_iter = 1000

    if not check_err:
        print(f"Scale Factor = {scale_factor}, iterations = {num_iter}")
    else:
        print(f"Scale Factor = {scale_factor}, iterations = {num_iter}, tolerance= {tolerance}")

    print("Irrotational flow")

    b_base, h_base, w_base, m_base, n_base = 10, 15, 5, 32, 32
    b = b_base * scale_factor
    h = h_base * scale_factor
    w = w_base * scale_factor
    m = m_base * scale_factor
    n = n_base * scale_factor

    print(f"Running CFD on {m} x {n} grid in serial")

    psi = array_malloc_2d(m + 2, n + 2)
    psitmp = array_malloc_2d(m + 2, n + 2)

    psi_cl = array_malloc_2d(m + 2, n + 2)
    psitmp_cl = array_malloc_2d(m + 2, n + 2)

    boundary_psi(psi, m, n, b, h, w)
    boundary_psi(psi_cl, m, n, b, h, w)

    b_norm = np.sqrt(np.sum(psi ** 2))

    print("\nStarting main loop...\n")
    start_time = time.time()

    for iter in range(1, num_iter + 1):
        # jacobi_step(psitmp, psi, m, n)
        jacobi_step_opencl(psitmp_cl, psi_cl, m, n)

        # indices_2d = np.where(psitmp != psitmp_cl)

        # Convert the indices to a list of coordinate tuples
        # diff_coords = list(zip(*indices_2d))

        # Print the coordinate tuples and the differences
        # print("Coordinate tuples with different elements (2D array):", diff_coords)
        # for coord in diff_coords:
        #    print(f"At index {coord}, CPU value = {psitmp[coord]}, GPU value = {psitmp_cl[coord]}")

        # print("CPU result:\n", psitmp)
        # print("GPU result:\n", psitmp_cl)

        # if checkerr or iter == numiter:
        #     error = np.sqrt(delta_sq(psitmp, psi, m, n)) / bnorm

        if check_err or iter == num_iter:
            error = np.sqrt(delta_sq(psitmp_cl, psi_cl, m, n)) / b_norm

        if check_err and error < tolerance:
            print(f"Converged on iteration {iter}")
            break

        # psi[1:m + 1, 1:n + 1] = psitmp[1:m + 1, 1:n + 1]
        psi_cl[1:m + 1, 1:n + 1] = psitmp_cl[1:m + 1, 1:n + 1]

        if iter % print_freq == 0:
            if not check_err:
                print(f"Completed iteration {iter}")
            else:
                print(f"Completed iteration {iter}, error = {error}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    one_iter_time = elapsed_time / iter

    print("\n... finished")
    print(f"After {iter} iterations, the error is {error}")
    print(f"Time for {iter} iterations was {elapsed_time} seconds")
    print(f"Each iteration took {one_iter_time} seconds")
    print("... finished")
    data = {
        "error": error,
        "time": elapsed_time,
        "iter_time": one_iter_time
    }
    csv_results_task_3("results.csv", data)


if __name__ == "__main__":
    main()
