import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def estimate(x, y):
    def func(x, a, b, c):
        return a*x**2 + b*x + c

    popt, pcov = curve_fit(func, x, y)
    print("=== Parameters ===")
    print(popt)
    print("=== Cov ===")
    print(pcov)

    plt.figure()
    plt.loglog(x, func(x, *popt), 'r-', label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
    plt.legend()
    plt.show()

    # First derivative
    fd = np.gradient(func(x, *popt))
    plt.figure()
    plt.loglog(x, fd, 'b-')
    plt.show()