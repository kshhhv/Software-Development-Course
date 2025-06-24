import numpy as np
import ctypes
import numpy.ctypeslib as npct

from logistic_map_original import logistic_map as logistic_map_py

import time

# Load C library
lib = ctypes.CDLL('./logistic_map.so')

lib.logistic_map.argtypes = [
    npct.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS,WRITEABLE'),
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_int
]
lib.logistic_map.restype = None

# Python wrapper for C version
def logistic_map_c(x0: float, r: float, n: int) -> np.ndarray:
    out = np.empty(n, dtype=np.float64)
    lib.logistic_map(out, x0, r, n)
    return out

# Common parameters
n = 100
size = 100

x_values = np.random.uniform(0, 1, size)
r_values = np.linspace(0, 4, size)

# Benchmark C version
start_c = time.perf_counter()
xks_c = np.empty((size, size, n), dtype=np.float64)
for i, x0 in enumerate(x_values):
    for j, r in enumerate(r_values):
        xks_c[i, j, :] = logistic_map_c(x0, r, n)
end_c = time.perf_counter()

# Benchmark python version
start_py = time.perf_counter()
xks_py = np.empty((size, size, n), dtype=np.float64)
for i, x0 in enumerate(x_values):
    for j, r in enumerate(r_values):
        xks_py[i, j, :] = logistic_map_py(x0, r, n)
end_py = time.perf_counter()

print(f"C version time     : {end_c - start_c:.4f} s")

print(f"Python version time: {end_py - start_py:.4f} s")
