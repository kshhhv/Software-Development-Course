The code does some curve fitting for 1-deg latitude/longitude bins over the entire map.

By profiling it's seen that most time is taken by scipy curve_fit.

Since each fitting is independent of each other, it can be easily parallelized.

The entire code initially took 26.43 seconds
After paralellization (using mpi) it took 18.84 seconds