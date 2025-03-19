import numpy as np

samples = 1000000
x = np.random.rand(samples)*2 - 1
y = np.random.rand(samples)*2 - 1

r = np.sqrt(x**2 + y**2)
pi = 4*np.sum(r<1)/samples

print(f'{samples=} gives {pi=} (error {np.pi - pi})')