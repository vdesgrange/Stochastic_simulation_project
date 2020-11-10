import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy.polynomial import Polynomial

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

def estimate_polyfit(x, y, labels):
    ## x is a list of numpy arrays
    ## y is a list of numpy arrays
    ## labels is a list of strings
    fig, ax = plt.subplots(dpi=150)
    ax.set_xlabel('Number of Samples')
    ax.set_ylabel(r'$|A_{it} - A_{is}|$')
    plt.title('Polynomial Fit of Convergence')
    for i in range(0, len(labels)):  
        p = Polynomial.fit(x[i], y[i], 5)
        plt.plot(*p.linspace(), label=labels[i])

    plt.legend()
    plt.show()