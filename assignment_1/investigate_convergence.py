import numpy as np
import matplotlib.pyplot as plt

import mandelbrot
import graphic_utils
from monte_carlo import monte_carlo_integration


def estimate_error(s, i, width, height, re, im):
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
    est, hist, c = monte_carlo_integration(
        width=width,
        height=height,
        re=re,
        im=im,
        n=s,
        max_i=i)

    # Estimated error for range of iterations between 0 and i.
    x = range(i + 1)
    y = []

    # Compute error
    a_is = hist[-1]  # Estimation of the area of the Mandelbrot set for i iteration and s samples.
    for j in x:  # For each number of iteration until max_i
        # Get number of samples which converge for j iteration
        count = np.sum((hist >= j).astype(int))
        a_js = (count / s) * a  # Estimation of the area of the Mandelbrot set for j iteration and s samples.
        y.append(abs(a_js - a_is))  # Error

    return x, y, c


def study_difference():
    """
    Simple experiment
    """
    x, y, _ = estimate_error(
        s=100000, i=1000,
        width=mandelbrot.WIDTH, height=mandelbrot.HEIGHT,
        re=(mandelbrot.RE_MIN, mandelbrot.RE_MAX), im=(mandelbrot.IM_MIN, mandelbrot.IM_MAX))

    graphic_utils.difference_plot(x, y)


def study_convergence():
    """
    Study convergence of points in complex plane.
    Get a list of complex number supposed to converge, and plot evolution of the function f_c(z)
    """
    max_i = 7000
    _, hist, complex_sample = monte_carlo_integration(
        width=mandelbrot.WIDTH,
        height=mandelbrot.HEIGHT,
        re=(mandelbrot.RE_MIN, mandelbrot.RE_MAX), im=(mandelbrot.IM_MIN, mandelbrot.IM_MAX),
        n=100, max_i=max_i)

    # Index of a sample of complex number which converge for at least max_i iterations.
    idx = np.random.choice(np.argwhere(hist == max_i)[:, 0], 10)
    # Sample o complex number which converge for at least max_i iterations.
    sample = np.array(complex_sample)[idx]
    for val in sample:
        print('c = {:f} + {:f}i'.format(val.real, val.imag))
        fz = mandelbrot.mandelbrot_detailed(val, max_i)
        re = [z.real for z in fz]
        im = [z.imag for z in fz]
        graphic_utils.complex_plan_plot(re, im)



if __name__ == '__main__':
    # study_difference()
    study_convergence()