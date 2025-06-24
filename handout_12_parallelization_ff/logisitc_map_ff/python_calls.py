import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ctypes
import numpy.ctypeslib as npct
import logging
import time

# Setup logger
logging.basicConfig(filename='logistic_map.log', level=logging.DEBUG)
logger = logging.getLogger("my_logger")

# Load C shared library
lib = ctypes.CDLL('./logistic_map.so')

# Define argtypes and restype for the C function
lib.logistic_map.argtypes = [
    npct.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS,WRITEABLE'),
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_int
]
lib.logistic_map.restype = None

# Wrapper function
def logistic_map(x0: float, r: float, n: int) -> np.ndarray:
    out = np.empty(n, dtype=np.float64)
    lib.logistic_map(out, x0, r, n)
    return out

# Plotting function remains unchanged
def plot_animate(xks, r_values, x_values):
    fig, ax = plt.subplots()

    def update(n):
        ax.clear()
        ax.set_title(f"N: {n}")
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 1)
        ax.set_xlabel('r')
        ax.set_ylabel('xₙ')

        for x_index, x in enumerate(x_values):
            ax.plot(r_values, xks[x_index, :, n], linewidth=0.2, color='k')

    anim = animation.FuncAnimation(fig, update, frames=xks.shape[2], interval=100)
    plt.show()

# Main computation
if __name__ == "__main__":
    start_time = time.time()

    n = 100  # number of iterations
    x_values = np.random.uniform(0, 1, n)
    r_values = np.linspace(0, 4, n)
    xks = np.empty((n, n, n), dtype=np.float64)

    for x_index, x in enumerate(x_values):
        for r_index, r in enumerate(r_values):
            try:
                xs = logistic_map(x, r, n)
                xks[x_index, r_index, :] = xs

                # test warning (unused, just for logging test)
                check = 1 / (x_index * r_index)
            except ZeroDivisionError as e:
                logger.warning(f"ZeroDivisionError at {x_index}, {r_index}: {e}")

    print(f'Time to calculate: {time.time()-start_time:.4f}s')
    
    plot_animate(xks, r_values, x_values)
