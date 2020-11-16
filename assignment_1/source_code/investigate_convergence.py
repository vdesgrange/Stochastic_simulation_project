import numpy as np
import mandelbrot
import graphic_utils
from statistical_analysis_utils import sample_mean, recursive_sample_mean
from monte_carlo import monte_carlo_integration
from sampling_method import halton_sequence, latin_square_chaos, orthogonal, pure_random
import random

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
    a_is, _, details = monte_carlo_integration(re, im, w, h, s, i, sampling_method=sampling_method)

    # Estimated error for range of iterations between 1 and i.
    x = range(1, i + 1)
    y = []

    # Compute error
    for j in x:  # For each number of iteration until max_i
        # Get number of samples which converge for j iteration
        count = np.sum((details >= j).astype(int))
        a_js = (count / s) * a  # Estimation of the area of the Mandelbrot set for j iteration and s samples.
        err = 100 * (abs(a_js - a_is) / abs(a_is))  # Relative error in percent
        y.append(err)

    return x, y, a_is


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
    a_is, _, details = monte_carlo_integration(re, im, w, h, s, i, sampling_method=sampling_method)

    # Estimated error for range of iterations between 0 and s.
    x = range(1, s + 1)
    y = []

    # Compute error
    for t in x:  # For an increasing number of sample j until s.
        count = np.sum((details[:t+1] == i).astype(int))
        a_it = (count / t) * a  # Estimation of the area of the Mandelbrot set for i iteration and t samples.
        err = 100 * (abs(a_it - a_is) / abs(a_is))   # Relative error in percent
        y.append(err)  # Error
    return x, y


def study_difference_by_iteration_q3(s, i, re=RE, im=IM, w=WIDTH, h=HEIGHT):
    """
    Get difference between A_js and A_is : number of iteration
    Get abs(A_js - A_is) for all j < i, then plot the results.
    params:
    i: max iterations to be tested
    """

    x_rand, y_rand, _ = estimate_error_by_iteration(re, im, w, h, s, i, sampling_method=pure_random)
    x_lhs, y_lhs, _ = estimate_error_by_iteration(re, im, w, h, s, i, sampling_method=latin_square_chaos)
    x_orth, y_orth, _ = estimate_error_by_iteration(re, im, w, h, s, i, sampling_method=orthogonal)
    graphic_utils.difference_plot_by_iteration_q3(x_rand, y_rand, x_lhs, y_lhs, x_orth, y_orth)

    return x_rand, y_rand, x_lhs, y_lhs, x_orth, y_orth


def study_difference_by_iteration(s, i, re=RE, im=IM, w=WIDTH, h=HEIGHT, sampling_method=pure_random):
    """
    Get difference between A_js and A_is : number of iteration
    Get abs(A_js - A_is) for all j < i, then plot the results.
    params:
    i: max iterations to be tested
    """
    nb_try = 50
    a_is = 0
    relative_error_stack = np.zeros((nb_try, i))
    for t in range(nb_try):
        x, y, a = estimate_error_by_iteration(re, im, w, h, s, i, sampling_method)
        relative_error_stack[t] = y
        a_is = recursive_sample_mean(a, a_is, t)

    i_range = range(0, i)
    sample_mean_error = []
    for j in i_range:
        sample_mean_error.append(sample_mean(relative_error_stack[:, j]))

    print("Mandelbrot set average estimated area : ", a_is)
    graphic_utils.difference_plot_by_iteration(i_range, sample_mean_error)
    return i_range, sample_mean_error


def study_difference_by_sampling(s, i, re=RE, im=IM, w=WIDTH, h=HEIGHT, sampling_method=pure_random):
    """
    Get difference between A_it and A_is : number of samples
    Get abs(A_it - A_is) for all t < i, then plot the results.
    """
    nb_try = 100
    relative_error_stack = np.zeros((nb_try, s))
    for t in range(nb_try):
        x, y = estimate_error_by_sampling(re, im, w, h, s, i, sampling_method)
        relative_error_stack[t] = y

    s_range = range(0, s, 50)
    sample_mean_error = []
    for j in s_range:
        sample_mean_error.append(sample_mean(relative_error_stack[:, j]))

    graphic_utils.difference_plot_by_sampling(s_range, sample_mean_error)
    return s_range, sample_mean_error


def study_convergence_iteration_qausi_normal(s, i, re=RE, im=IM, w=WIDTH, h=HEIGHT):
    x_lhs, y_lhs, _ = estimate_error_by_iteration(re, im, w, h, s, i, sampling_method=latin_square_chaos)
    x_hal, y_hal, _ = estimate_error_by_iteration(re, im, w, h, s, i, sampling_method=halton_sequence)

    graphic_utils.difference_plot_by_iteration_q4(x_lhs, y_lhs, x_hal, y_hal)
    return x_lhs, y_lhs, x_hal, y_hal


def study_convergence_samples_qausi_normal(s, i, re=RE, im=IM, w=WIDTH, h=HEIGHT):
    x_lhs, y_lhs = estimate_error_by_sampling(re, im, w, h, s, i, sampling_method=latin_square_chaos)
    x_hal, y_hal = estimate_error_by_sampling(re, im, w, h, s, i, sampling_method=halton_sequence)

    graphic_utils.difference_plot_by_sampling_q4(x_lhs, y_lhs, x_hal, y_hal)
    return x_lhs, y_lhs, x_hal, y_hal


if __name__ == '__main__':
    # Q2
    # study_difference_by_iteration(5000, 20000)
    study_difference_by_sampling(1000, 1000)

    # study_difference_by_sampling(10000, 500)
    # study_difference_by_sampling(10000, 800)
    # study_difference_by_sampling(10000, 1000)

    # Study difference by number of iteration
    # study_difference_by_iteration_q3(10000, 5000)

    # study_convergence_by_sampling_method(100000, 100)
    # study_convergence_by_sampling_method(10000, 800)
    # study_convergence_mandelbrot()
    
    ### Q4 Randomised Quasi-MC vs MC Graphs
    #study_convergence_iteration_qausi_normal(10000, 3000)
    # study_convergence_samples_qausi_normal(10000, 3000)
