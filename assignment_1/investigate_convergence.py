import numpy as np

import mandelbrot
import graphic_utils
import curve_utils
from monte_carlo import monte_carlo_integration
from sampling_method import halton_sequence, latin_square_chaos, orthogonal, pure_random

RE = (mandelbrot.RE_MIN, mandelbrot.RE_MAX)
IM = (mandelbrot.IM_MIN, mandelbrot.IM_MAX)
WIDTH = mandelbrot.WIDTH
HEIGHT = mandelbrot.HEIGHT


def estimate_error_by_iteration(re, im, w, h, s, i, sampling_method):
    """
    :param s: Number of samples
    :param i: Maximal number of iteration
    :param w: width of the plan
    :param h: height of the plan
    :param re: tuple of (minimal, maximal) coordinates of real axis
    :param im: tuple of (minimal, maximal) coordinates of imaginary axis.
    """
    # Area of the complex plane
    a = (re[1] - re[0]) * (im[1] - im[0])

    # Estimation of the area surface of Mandelbrot set for i iterations and s samples.
    est, _, details = monte_carlo_integration(re, im, w, h, s, i, sampling_method=sampling_method)

    # Estimated error for range of iterations between 0 and i.
    x = range(i + 1)
    y = []

    # Compute error
    a_is = est  # Estimation of the area of the Mandelbrot set for i iteration and s samples.
    for j in x:  # For each number of iteration until max_i
        # Get number of samples which converge for j iteration
        count = np.sum((details >= j).astype(int))
        a_js = (count / s) * a  # Estimation of the area of the Mandelbrot set for j iteration and s samples.
        y.append(abs(a_js - a_is))  # Error

    return x, y


def estimate_error_by_sampling(re, im, w, h, s, i, sampling_method):
    """
    :param re: tuple of (minimal, maximal) coordinates of real axis
    :param im: tuple of (minimal, maximal) coordinates of imaginary axis.
    :param w: width of the plan
    :param h: height of the plan
    :param s: Maximal number of samples
    :param i: Number of iteration
    """
    # Area of the complex plane
    a = (re[1] - re[0]) * (im[1] - im[0])

    # Estimation of the area surface of Mandelbrot set for i iterations and s samples.
    est, _, details = monte_carlo_integration(re, im, w, h, s, i, sampling_method=sampling_method)

    # Estimated error for range of iterations between 0 and i.
    x = range(1, s + 1)
    y = []

    # Compute error
    a_is = est  # Estimation of the area of the Mandelbrot set for i iteration and s samples.
    for t in x:  # For an increasing number of sample j until s.
        count = np.sum((details[:t+1] == i).astype(int))
        a_it = (count / t) * a  # Estimation of the area of the Mandelbrot set for i iteration and t samples.
        y.append(abs(a_it - a_is))  # Error
    return x, y


def estimate_error_by_sampling_method(re, im, w, h, s, i):
    """
    :param re: tuple of (minimal, maximal) coordinates of real axis
    :param im: tuple of (minimal, maximal) coordinates of imaginary axis.
    :param w: width of the plan
    :param h: height of the plan
    :param s: Maximum number of samples
    :param i: Number of iteration (should be minimum  with which we have reasonable convergence)
    """
    # Area of the complex plane
    a = (re[1] - re[0]) * (im[1] - im[0])

    # Estimation of the area surface of Mandelbrot set for i iterations and s samples.
    a_is_rand, _, details_rand = monte_carlo_integration(re, im, w, h, s, i, sampling_method=pure_random)
    a_is_halton, _, details_halton = monte_carlo_integration(re, im, w, h, s, i, sampling_method=halton_sequence)
    a_is_lhs, _, details_lhs = monte_carlo_integration(re, im, w, h, s, i, sampling_method=latin_square_chaos)

    # Estimated error for range of iterations between 0 and i.
    x_rand = x_halton = x_lhs = range(1, s + 1)
    y_rand, y_halton, y_lhs = [], [], []

    # Compute error for random
    for t in x_rand:  # For an increasing number of sample j until s.
        # Get number of samples which converge for j iteration
        count = np.sum((details_rand[:t+1] == i).astype(int))
        a_it = (count / t) * a  # Estimation of the area of the Mandelbrot set for j iteration and s samples.
        y_rand.append(abs(a_it - a_is_rand))  # Error

    # Compute error for halton
    for t in x_halton:  # For an increasing number of sample j until s.
        # Get number of samples which converge for j iteration
        count = np.sum((details_halton[:t+1] == i).astype(int))
        a_it = (count / t) * a  # Estimation of the area of the Mandelbrot set for j iteration and s samples.
        y_halton.append(abs(a_it - a_is_halton))  # Error

    # Compute error for Latin hypercube sampling
    for t in x_lhs:  # For an increasing number of sample j until s.
        # Get number of samples which converge for j iteration
        count = np.sum((details_lhs[:t+1] == i).astype(int))
        a_it = (count / t) * a  # Estimation of the area of the Mandelbrot set for j iteration and s samples.
        y_lhs.append(abs(a_it - a_is_lhs))  # Error

    # Compute error for random
    # for t in x_orth:  # For an increasing number of sample j until s.
    #     # Get number of samples which converge for j iteration
    #     count = np.sum((details_orth[:t+1] == i).astype(int))
    #     a_it = (count / t) * a  # Estimation of the area of the Mandelbrot set for j iteration and s samples.
    #     y_orth.append(abs(a_it - a_is_orth))  # Error

    return x_rand, y_rand, x_halton, y_halton, x_lhs, y_lhs


def study_difference_by_iteration(s, i, re=RE, im=IM, w=WIDTH, h=HEIGHT, sampling_method=pure_random):
    """
    Get difference between A_js and A_is : number of iteration
    Get abs(A_js - A_is) for all j < i, then plot the results.
    """
    x, y = estimate_error_by_iteration(re, im, w, h, s, i, sampling_method)
    graphic_utils.difference_plot_by_iteration(x, y)
    return x, y


def study_difference_by_sampling(s, i, re=RE, im=IM, w=WIDTH, h=HEIGHT, sampling_method=pure_random):
    """
    Get difference between A_it and A_is : number of samples
    Get abs(A_it - A_is) for all t < i, then plot the results.
    """
    x, y = estimate_error_by_sampling(re, im, w, h, s, i, sampling_method)
    graphic_utils.difference_plot_by_sampling(x, y)
    return x, y


def study_convergence_by_sampling_method(s, i, re=RE, im=IM, w=WIDTH, h=HEIGHT):
    """
    Get difference between A_it and A_is : pure random sampling vs Halton
    Examing which sampling method requires fewer samples to converge
    Get abs(A_js - A_is) for all j < i, then plot the results.
    """
    x_rand, y_rand, x_halton, y_halton, x_lhs, y_lhs = estimate_error_by_sampling_method(re, im, w, h, s, i)
    graphic_utils.convergence_plot_by_sampling_method(x_rand, y_rand, x_halton, y_halton, x_lhs, y_lhs)


def convergence(c, i):
    print('c = ', c)
    fz = mandelbrot.mandelbrot_detailed(c, i)
    re = [z.real for z in fz]
    im = [z.imag for z in fz]
    graphic_utils.complex_plan_plot(re, im)


def study_convergence_mandelbrot(re=RE, im=IM, w=WIDTH, h=HEIGHT):
    """
    Study convergence of points in complex plane.
    Get a list of complex number supposed to converge, and plot evolution of the function f_c(z)
    """
    max_i = 1000

    # Get sample of complex numbers and the number of iteration where they converge in mandelbrot set.
    _, complex_sample, details = monte_carlo_integration(re, im, w, h, 200, max_i)

    # Index of a sample of complex number which converge for at least max_i iterations.
    idx = np.random.choice(np.argwhere(details == max_i)[:, 0], 5)

    # Sample of complex numbers which converge for at least max_i iterations.
    sample = np.array(complex_sample)[idx]

    for val in sample:
        convergence(val, max_i)


if __name__ == '__main__':
    # Study difference by number of iteration
    # study_difference_by_iteration(1000, 1000)
    study_difference_by_iteration(10000, 1000)
    study_difference_by_iteration(100000, 1000)
    #
    # # Study difference by number of samples
    # study_difference_by_sampling(10000, 500)
    # study_difference_by_sampling(10000, 800)
    # study_difference_by_sampling(10000, 1000)

    # 1000, 800 ?
    # study_convergence_by_sampling_method(100000, 100)
    # study_convergence_by_sampling_method(10000, 800)

    # study_convergence_mandelbrot()
