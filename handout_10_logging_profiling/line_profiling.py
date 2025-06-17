"""

To run:
python -m kernprof -lv line_profiling.py

"""

from line_profiler import profile
import numpy as np
 
@profile
def func():
    L = [i for i in range(1000)]
    L = []
    for i in range(1_000):
        L.append(i)
    for i in range(10_000):
        x = np.eye(3) @ np.ones((3,))
    del x
 
func()