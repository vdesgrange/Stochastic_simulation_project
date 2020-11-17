import numpy as np
import mandelbrot
import graphic_utils
from statistical_analysis_utils import sample_variance, sample_mean
from monte_carlo import monte_carlo_integration
from sampling_method import halton_sequence, latin_square_chaos, orthogonal_native, pure_random

RE = (mandelbrot.RE_MIN, mandelbrot.RE_MAX)
IM = (mandelbrot.IM_MIN, mandelbrot.IM_MAX)
WIDTH = mandelbrot.WIDTH
HEIGHT = mandelbrot.HEIGHT


def estimate_iteration_area_per_method(re, im, w, h, s, i):
    """
    Compute an approximation of mandelbrot set area by maximal number of iteration
    for 4 sampling methods: pure random, halton sequence, latin square, orthogonal
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
    a_is_orth, _, details_orth = monte_carlo_integration(re, im, w, h, s, i, sampling_method=orthogonal_native)

    # Estimated error for range of iterations between 0 and i.
    i_range = range(i + 1)
    y_rand, y_halton, y_lhs, y_orth = [], [], [], []

    # Compute error by samples for random, halton sequence and latin hypercube
    for j in i_range:
        # Get number of samples which converge for j iteration
        count_rand = np.sum((details_rand >= j).astype(int))
        count_halton = np.sum((details_halton >= j).astype(int))
        count_lhs = np.sum((details_lhs >= j).astype(int))
        count_orth = np.sum((details_orth >= j).astype(int))

        a_rand_js = (count_rand / s) * a
        a_halton_js = (count_halton / s) * a
        a_lhs_js = (count_lhs / s) * a
        a_orth_js = (count_orth / s) * a

        y_rand.append(a_rand_js)
        y_halton.append(a_halton_js)
        y_lhs.append(a_lhs_js)
        y_orth.append(a_orth_js)

    return i_range, y_rand, y_halton, y_lhs, y_orth


def estimate_samples_area_per_method(re, im, w, h, s, i):
    """
    Compute an approximation of mandelbrot set area by number of samples in complex plan
    for 4 sampling methods: pure random, halton sequence, latin square, orthogonal
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
    a_is_orth, _, details_orth = monte_carlo_integration(re, im, w, h, s, i, sampling_method=orthogonal_native)

    # Estimated error for range of iterations between 0 and i.
    s_range = range(1, s + 1)
    y_rand, y_halton, y_lhs, y_orth = [], [], [], []

    # Compute error by samples for random, halton sequence and latin hypercube
    for t in s_range:
        count_rand = np.sum((details_rand[:t+1] == i).astype(int))
        count_halton = np.sum((details_halton[:t+1] == i).astype(int))
        count_lhs = np.sum((details_lhs[:t+1] == i).astype(int))
        count_orth = np.sum((details_orth[:t+1] == i).astype(int))


        a_rand_it = (count_rand / t) * a
        a_halton_it = (count_halton / t) * a
        a_lhs_it = (count_lhs / t) * a
        a_orth_it = (count_orth / t) * a

        y_rand.append(a_rand_it)
        y_halton.append(a_halton_it)
        y_lhs.append(a_lhs_it)
        y_orth.append(a_orth_it)

    return s_range, y_rand, y_halton, y_lhs, y_orth


def study_iteration_convergence(s, i, re=RE, im=IM, w=WIDTH, h=HEIGHT):
    """
    Examine which sampling method requires fewer samples to converge.
    Get abs(A_js - A_is) for all j < i, then plot the results.
    Study area, variance and maximal difference.
    """
    nb_try = 50
    area_stack = np.zeros((4, nb_try, i + 1))

    print("Estimating area...")
    for t in range(nb_try):
        x_range, y_rand, y_halton, y_lhs, y_orth = estimate_iteration_area_per_method(re, im, w, h, s, i)
        area_stack[0][t] = np.array(y_rand)
        area_stack[1][t] = np.array(y_halton)
        area_stack[2][t] = np.array(y_lhs)
        area_stack[3][t] = np.array(y_orth)

    print("Computing variance ...")
    x_diff_range = range(0, i + 1, 10)
    variance_stack = [[], [], [], []]
    for j in x_diff_range:
        variance_stack[0].append(sample_variance(area_stack[0, :, j]))
        variance_stack[1].append(sample_variance(area_stack[1, :, j]))
        variance_stack[2].append(sample_variance(area_stack[2, :, j]))
        variance_stack[3].append(sample_variance(area_stack[3, :, j]))

    print("Computing maximal difference...")
    x_diff_range = range(0, i + 1, 10)
    max_diff_stack = [[], [], [], []]
    for j in x_diff_range:
        d_r, d_h, d_l, d_o = 0, 0, 0, 0

        for t in range(nb_try):
            for u in range(t + 1, nb_try):
                d_r = max(d_r, abs(area_stack[0][t][j] - area_stack[0][u][j]) / abs(area_stack[0][t][j] + area_stack[0][u][j]))
                d_h = max(d_h, abs(area_stack[1][t][j] - area_stack[1][u][j]) / abs(area_stack[1][t][j] + area_stack[1][u][j]))
                d_l = max(d_l, abs(area_stack[2][t][j] - area_stack[2][u][j]) / abs(area_stack[2][t][j] + area_stack[2][u][j]))
                d_o = max(d_o, abs(area_stack[3][t][j] - area_stack[3][u][j]) / abs(area_stack[3][t][j] + area_stack[3][u][j]))

        max_diff_stack[0].append(d_r)
        max_diff_stack[1].append(d_h)
        max_diff_stack[2].append(d_l)
        max_diff_stack[3].append(d_o)

    graphic_utils.plot_convergence(np.array(x_range), area_stack, 'Number of iteration i')
    graphic_utils.plot_convergence_difference(np.array(x_diff_range), max_diff_stack, 'Number of iteration i')
    graphic_utils.plot_convergence_variance(np.array(x_diff_range), variance_stack, 'Number of iteration i')


def study_samples_convergence(s, i, re=RE, im=IM, w=WIDTH, h=HEIGHT):
    """
    Examine which sampling method requires fewer samples to converge.
    Get abs(A_it - A_is) for all t < s, then plot the results.
    Study area, variance and maximal difference.
    """
    nb_try = 100
    area_stack = np.zeros((4, nb_try, s))


    print("Estimating area...")
    for t in range(nb_try):
        x_range, y_rand, y_halton, y_lhs, y_orth = estimate_samples_area_per_method(re, im, w, h, s, i)
        area_stack[0][t] = np.array(y_rand)
        area_stack[1][t] = np.array(y_halton)
        area_stack[2][t] = np.array(y_lhs)
        area_stack[3][t] = np.array(y_orth)

    print("Computing variance...")
    x_diff_range = range(0, s, 50)
    variance_stack = [[], [], [], []]
    for j in x_diff_range:
        variance_stack[0].append(sample_variance(area_stack[0, :, j]))
        variance_stack[1].append(sample_variance(area_stack[1, :, j]))
        variance_stack[2].append(sample_variance(area_stack[2, :, j]))
        variance_stack[3].append(sample_variance(area_stack[3, :, j]))

    print("Computing maximal difference...")
    x_diff_range = range(0, s, 50)
    max_diff_stack = [[], [], [], []]
    for j in x_diff_range:
        d_r, d_l, d_h, d_o = 0, 0, 0, 0
        for t in range(nb_try):
            for u in range(t + 1, nb_try):
                d_r = max(d_r, abs(area_stack[0][t][j] - area_stack[0][u][j]) / abs(area_stack[0][t][j] + area_stack[0][u][j]))
                d_l = max(d_l, abs(area_stack[1][t][j] - area_stack[1][u][j]) / abs(area_stack[1][t][j] + area_stack[1][u][j]))
                d_h = max(d_h, abs(area_stack[2][t][j] - area_stack[2][u][j]) / abs(area_stack[2][t][j] + area_stack[2][u][j]))
                d_o = max(d_o, abs(area_stack[3][t][j] - area_stack[3][u][j]) / abs(area_stack[3][t][j] + area_stack[3][u][j]))

        max_diff_stack[0].append(d_r)
        max_diff_stack[1].append(d_l)
        max_diff_stack[2].append(d_h)
        max_diff_stack[3].append(d_o)

    graphic_utils.plot_convergence(np.array(x_range), area_stack, 'Number of sample s')
    graphic_utils.plot_convergence_difference(np.array(x_diff_range), max_diff_stack, 'Number of sample s')
    graphic_utils.plot_convergence_variance(np.array(x_diff_range), variance_stack, 'Number of sample s')


def study_iteration_convergence_single_method(s, i, re=RE, im=IM, w=WIDTH, h=HEIGHT):
    """
    Get difference between A_js and A_is
    Examing which sampling method requires fewer samples to converge
    Get abs(A_js - A_is) for all j < i, then plot the results.
    """
    nb_try = 50
    area_stack = np.zeros((nb_try, i + 1))

    print("Estimating area...")
    for t in range(nb_try):
        a = (re[1] - re[0]) * (im[1] - im[0])
        a_is_rand, _, details_rand = monte_carlo_integration(re, im, w, h, s, i, sampling_method=pure_random)
        i_range = range(i + 1)
        y_rand = []
        for j in i_range:
            count_rand = np.sum((details_rand >= j).astype(int))
            a_rand_js = (count_rand / s) * a
            y_rand.append(a_rand_js)

        area_stack[t] = np.array(y_rand)

    graphic_utils.plot_convergence_single_method(np.array(i_range), area_stack, 'Maximal number of iterations i')


def study_samples_convergence_single_method(s, i, re=RE, im=IM, w=WIDTH, h=HEIGHT):
    """
    Get difference between A_js and A_is
    Examing which sampling method requires fewer samples to converge
    Get abs(A_js - A_is) for all j < i, then plot the results.
    """
    nb_try = 50
    area_stack = np.zeros((nb_try, s))
    a = (re[1] - re[0]) * (im[1] - im[0])

    print("Estimating area...")
    for tr in range(nb_try):
        a_is_rand, _, details_rand = monte_carlo_integration(re, im, w, h, s, i, sampling_method=pure_random)
        s_range = range(1, s + 1)
        y_rand = []
        for t in s_range:
            count_rand = np.sum((details_rand[:t+1] == i).astype(int))
            a_rand_it = (count_rand / t) * a
            y_rand.append(a_rand_it)

        area_stack[tr] = np.array(y_rand)

    graphic_utils.plot_convergence_single_method(np.array(s_range), area_stack, 'Number of samples s')


if __name__ == '__main__':
    # Experiment with only pure random sampling
    study_iteration_convergence_single_method(1000, 1000)  # Maximal number of iterations
    study_samples_convergence_single_method(1000, 1000)  # Number of samples

    # Experiment with  4 methods
    study_iteration_convergence(1000, 1000)  # Maximal number of iterations
    study_samples_convergence(1000, 1000)  # Number of samples
