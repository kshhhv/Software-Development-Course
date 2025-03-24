import numpy as np
import time
 
np.random.seed(12345)
x = np.random.randn(3, 10_000).T.tolist()
M = np.eye(3).T.tolist()
 
repeats = 1_000
 
t0 = time.time()
 
# do work a lot!
for ri in range(repeats):
    out = []  # calculate the matrix multiplication and sum
    for ind in range(10_000):
        x1, x2, x3 = x[ind]
        y = [
            x1 * M[0][dim] + x2 * M[1][dim] + x3 * M[2][dim]
            for dim in range(3)
        ]
        out.append(sum(y))