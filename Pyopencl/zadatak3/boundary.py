import numpy as np


def boundary_psi(psi, m, n, b, h, w):
    for i in range(b + 1, b + w):
        psi[i, 0] = float(i - b)

    for i in range(b + w, m + 1):
        psi[i, 0] = float(w)

    # BCS on RHS
    for j in range(1, h + 1):
        psi[m + 1, j] = float(w)

    for j in range(h + 1, h + w):
        psi[m + 1, j] = float(w - j + h)

