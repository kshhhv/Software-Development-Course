// logistic_map.c
#include <stdio.h>

void logistic_map(double* out, double x0, double r, int n) {
    out[0] = x0;

    for (int i = 1; i < n; ++i) {
        out[i] = r * out[i - 1] * (1.0 - out[i - 1]);
    }
}
