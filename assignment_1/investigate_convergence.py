import numpy as np

import mandelbrot
import graphic_utils
from monte_carlo import monte_carlo_integration


def estimate_error( width, height, re, im, s, i):
    """
    :param s: Number of samples
    :param i: Maximal number of iteration
    :param width: width of the plan
    :param height: height of the plan
    :param re: tuple of (minimal, maximal) coordinates of real axis
    :param im: tuple of (minimal, maximal) coordinates of imaginary axis.
    """
    # Area of the complex plane
    a = (re[1] - re[0]) * (im[1] - im[0])

    # Estimation of the area surface of Mandelbrot set for i iterations and s samples.
    _, _, details = monte_carlo_integration(width=width, height=height, re=re, im=im, s=s, i=i)

    # Estimated error for range of iterations between 0 and i.
    x = range(i + 1)
    y = []

    # Compute error
    a_is = details[-1]  # Estimation of the area of the Mandelbrot set for i iteration and s samples.
    for j in x:  # For each number of iteration until max_i
        # Get number of samples which converge for j iteration
        count = np.sum((details >= j).astype(int))
        a_js = (count / s) * a  # Estimation of the area of the Mandelbrot set for j iteration and s samples.
        y.append(abs(a_js - a_is))  # Error

    return x, y


def study_difference():
    """
    Get difference between A_js and A_is.
    Get abs(A_js - A_is) for all j < i, then plot the results.
    """
    w, h = mandelbrot.WIDTH, mandelbrot.HEIGHT
    re = (mandelbrot.RE_MIN, mandelbrot.RE_MAX)
    im = (mandelbrot.IM_MIN, mandelbrot.IM_MAX)
    x, y = estimate_error(width=w, height=h, re=re, im=im, s=100000, i=1000)
    graphic_utils.difference_plot(x, y)


def convergence(c, i):
    print('c = ', c)
    fz = mandelbrot.mandelbrot_detailed(c, i)
    re = [z.real for z in fz]
    im = [z.imag for z in fz]
    graphic_utils.complex_plan_plot(re, im)


def study_convergence():
    """
    Study convergence of points in complex plane.
    Get a list of complex number supposed to converge, and plot evolution of the function f_c(z)
    """
    max_i = 7000
    w, h = mandelbrot.WIDTH, mandelbrot.HEIGHT
    re = (mandelbrot.RE_MIN, mandelbrot.RE_MAX)
    im = (mandelbrot.IM_MIN, mandelbrot.IM_MAX)

    # Get sample of complex numbers and the number of iteration where they converge in mandelbrot set.
    _, complex_sample, details = monte_carlo_integration(width=w, height=h, re=re, im=im, s=100, i=max_i)

    # Index of a sample of complex number which converge for at least max_i iterations.
    idx = np.random.choice(np.argwhere(details == max_i)[:, 0], 10)

    # Sample of complex numbers which converge for at least max_i iterations.
    sample = np.array(complex_sample)[idx]

    for val in sample:
        convergence(val, max_i)


if __name__ == '__main__':
    # study_difference()
    study_convergence()