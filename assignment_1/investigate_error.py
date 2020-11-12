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


def estimate_iteration_error(re, im, w, h, s, i):
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
    i_range = range(i + 1)
    x_rand = x_halton = x_lhs = i_range
    y_rand, y_halton, y_lhs = [], [], []

    # Compute error by samples for random, halton sequence and latin hypercube
    for j in i_range:
        # Get number of samples which converge for j iteration
        count_rand = np.sum((details_rand >= j).astype(int))
        count_halton = np.sum((details_halton >= j).astype(int))
        count_lhs = np.sum((details_lhs >= j).astype(int))

        a_rand_js = (count_rand / s) * a
        a_halton_js = (count_halton / s) * a
        a_lhs_js = (count_lhs / s) * a

        y_rand.append(abs(a_rand_js - a_is_rand))
        y_halton.append(abs(a_halton_js - a_is_halton))
        y_lhs.append(abs(a_lhs_js - a_is_lhs))

    return x_rand, y_rand, x_halton, y_halton, x_lhs, y_lhs


def estimate_samples_error(re, im, w, h, s, i):
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
    s_range = range(1, s + 1)
    x_rand = x_halton = x_lhs = s_range
    y_rand, y_halton, y_lhs = [], [], []

    # Compute error by samples for random, halton sequence and latin hypercube
    for t in s_range:
        count_rand = np.sum((details_rand[:t+1] == i).astype(int))
        count_halton = np.sum((details_halton[:t+1] == i).astype(int))
        count_lhs = np.sum((details_lhs[:t+1] == i).astype(int))

        a_rand_it = (count_rand / t) * a
        a_halton_it = (count_halton / t) * a
        a_lhs_it = (count_lhs / t) * a

        y_rand.append(abs(a_rand_it - a_is_rand))
        y_halton.append(abs(a_halton_it - a_is_halton))
        y_lhs.append(abs(a_lhs_it - a_is_lhs))

    # # Compute error for random
    # for t in x_rand:  # For an increasing number of sample j until s.
    #     # Get number of samples which converge for j iteration
    #     count = np.sum((details_rand[:t+1] == i).astype(int))
    #     a_it = (count / t) * a  # Estimation of the area of the Mandelbrot set for j iteration and s samples.
    #     y_rand.append(abs(a_it - a_is_rand))  # Error
    #
    # # Compute error for halton
    # for t in x_halton:  # For an increasing number of sample j until s.
    #     # Get number of samples which converge for j iteration
    #     count = np.sum((details_halton[:t+1] == i).astype(int))
    #     a_it = (count / t) * a  # Estimation of the area of the Mandelbrot set for j iteration and s samples.
    #     y_halton.append(abs(a_it - a_is_halton))  # Error
    #
    # # Compute error for Latin hypercube sampling
    # for t in x_lhs:  # For an increasing number of sample j until s.
    #     # Get number of samples which converge for j iteration
    #     count = np.sum((details_lhs[:t+1] == i).astype(int))
    #     a_it = (count / t) * a  # Estimation of the area of the Mandelbrot set for j iteration and s samples.
    #     y_lhs.append(abs(a_it - a_is_lhs))  # Error

    # Compute error for random
    # for t in x_orth:  # For an increasing number of sample j until s.
    #     # Get number of samples which converge for j iteration
    #     count = np.sum((details_orth[:t+1] == i).astype(int))
    #     a_it = (count / t) * a  # Estimation of the area of the Mandelbrot set for j iteration and s samples.
    #     y_orth.append(abs(a_it - a_is_orth))  # Error

    return x_rand, y_rand, x_halton, y_halton, x_lhs, y_lhs


def study_iteration_error(s, i, re=RE, im=IM, w=WIDTH, h=HEIGHT):
    """
    Get difference between A_js and A_is
    Examing which sampling method requires fewer samples to converge
    Get abs(A_js - A_is) for all j < i, then plot the results.
    """
    x_rand, y_rand, x_halton, y_halton, x_lhs, y_lhs = estimate_iteration_error(re, im, w, h, s, i)
    graphic_utils.convergence_plot_by_sampling_method(x_rand, y_rand, x_halton, y_halton, x_lhs, y_lhs)


def study_samples_error(s, i, re=RE, im=IM, w=WIDTH, h=HEIGHT):
    """
    Get difference between A_it and A_is with different sampling method
    pure random, halton, latin hypercube, etc.
    Examine which sampling method requires fewer samples to converge
    Get abs(A_it - A_is) for all t < s, then plot the results.
    """
    x_rand, y_rand, x_halton, y_halton, x_lhs, y_lhs = estimate_samples_error(re, im, w, h, s, i)
    graphic_utils.convergence_plot_by_sampling_method(x_rand, y_rand, x_halton, y_halton, x_lhs, y_lhs)


if __name__ == '__main__':
    study_iteration_error(1000, 1500)
    #study_iteration_error(10000, 1500)
    #study_iteration_error(10000, 1500)

    study_samples_error(2000, 1000)
    #study_samples_error(10000, 500)
   # study_samples_error(10000, 1000)

