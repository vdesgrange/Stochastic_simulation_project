import numpy as np
import matplotlib.pyplot as plt
import sampling_method as sm

# Hexadecimal colour scheme for mandelbrot visualisation
# https://coolors.co
palette = ['#060A0F', '#0B141E', '#111E2D', '#16283C', '#1C324A', '#213C59', '#274668', '#2C5077', '#325A86',
           '#376495', '#3D6EA4', '#4279B3', '#4C83BD', '#5B8DC2', '#6A97C8', '#6D9AC9', '#88ACD3', '#97B7D8',
           '#A6C1DE', '#B5CBE3', '#C3D6E9', '#D2E0EE', '#E1E4F4', '#F0F5F9', '#FFFFFF']


def difference_plot_by_iteration(x, y, y_expected=None):
    """
    Visualize the convergence of a sampling method.
    We plot the relative error (in percent) of mandelbrot set area value computed against
    the more accurate estimation, based on the maximal number of iterations.
    :param x: Maximal number of iteration set to estimate mandelbrot set area
    :param y: Relative error in percent: 100 * |A_js - Ais|/|A_is|
    :param y_expected:  Expected convergence: (1 / N) for pure random
    """
    fig, ax = plt.subplots(dpi=150)
    ax.set_xlabel('Maximal number of iterations j')
    ax.set_ylabel(r'$100 \cdot \frac{|A_{js} - A_{is}|}{|A_{is}|}$')
    ax.set_title('Evolution of relative error (%)')
    ax.loglog(x, y, color='coral', linewidth='.5', label='Relative error')
    if y_expected is not None:
        ax.loglog(x, y_expected, color='black', linestyle='dashed', linewidth='.5', label='Expected')
    plt.legend()
    plt.show()


def difference_plot_by_sampling(x, y, y_expected=None):
    """
    Visualize the convergence of a sampling method.
    We plot the relative error (in percent) of mandelbrot set area value computed against
    the more accurate estimation, based on the number of samples used.
    :param x: Number of samples used to estimate mandelbrot set area
    :param y: Relative error in percent: 100 * |A_it - Ais|/|A_is|
    :param y_expected:  Expected convergence: 1 / sqrt(N) for pure random; 1/N for halton sequence
    """
    fig, ax = plt.subplots(dpi=150)
    ax.set_xlabel('Number of sampling t')
    ax.set_ylabel(r'$100 \cdot \frac{|A_{it} - A_{is}|}{|A_{is}|}$')
    ax.set_title(r'Evolution of relative error (%)')
    ax.loglog(x, y, color='coral', linewidth='.5', label='Relative error')
    if y_expected is not None:
        ax.loglog(x, y_expected, color='black', linestyle='dashed', linewidth='.5', label='Expected')

    plt.legend()
    plt.show()


def difference_plot_by_sampling_q4(x1, y1, x2, y2):
    """
    Visualize the convergence of two sampling method: pure random and halton sequence sampling.
    We plot the relative errors (in percent) of mandelbrot set area value computed against
    the more accurate estimation, based on the number of samples used.
    :param x1: Number of samples used for pure random
    :param y1: Relative error in percent for pure random
    :param x2: Number of samples used for halton sequence
    :param y2: Relative error in percent for halton sequence
    """
    fig, ax = plt.subplots(dpi=150, sharex=True, squeeze=True)

    ax.set_xlabel('Number of sampling t')
    ax.set_ylabel(r'$100 \cdot \frac{|A_{it} - A_{is}|}{|A_{is}|}$')
    ax.set_title('Evolution of relative error (%)')

    ax.loglog(x1, y1, color='seagreen', linewidth='.5', label='Random MC')
    ax.loglog(x1, np.true_divide(100, np.sqrt(x1)), color='black', linestyle='dashed', linewidth='.5')

    ax.loglog(x2, y2, color='coral', linewidth='.5',label='Randomised Quasi-MC')
    ax.loglog(x2, np.true_divide(100, x2), color='black', linestyle='dashed', linewidth='.5')

    plt.legend()
    plt.show()


def complex_plan_plot(re, im):
    """
    Plot the convergence of a value in the complex plan.
    :param re: array of real part
    :param im: array of imaginary part
    """
    fig, ax = plt.subplots(dpi=150)
    ax.set_xlabel('Re')
    ax.set_ylabel('Im')
    ax.set_title(r'Convergence of complex number $c \approx {:3f} + ({:3f})i$'.format(re[0], im[0]))
    ax.plot(re, im, color='lightskyblue', marker='o', linewidth='.5')
    plt.show()


def plot_convergence_single_method(x, y, x_label):
    """
    Plot estimation of Mandelbrot set area from a set of simulations for 1 method at log scale.
    Based on the number of samples or maximal number of iterations.
    :param x: Number of samples or maximal number of iteration
    :param y: Array of area estimated for a number of sample/iterations.
    :param x_label: Label associated to x axis
    """
    fig, ax = plt.subplots(1, 1, dpi=150)

    nb_simulation, nb_area = np.shape(y)
    
    for t in range(nb_simulation):
        rand_idx = np.random.randint(low=0, high=nb_area, size=50)
        ax.scatter(x[rand_idx], y[t][rand_idx], s=0.5)

    ax.set_title('Pure random sampling')
    ax.set_xlabel(x_label)
    ax.set_ylabel('Area of Mandelbrot set')
    ax.set_ylim(1, 2)
    plt.show()


def plot_convergence(x, y, x_label):
    """
    Plot estimation of Mandelbrot set area from a set of simulations for 4 different methods at log scale.
    Based on the number of samples or maximal number of iterations.
    Pure random, Latin Square, Orthogonal, Halton sequence
    :param x: Number of samples or maximal number of iteration
    :param y: Array of area estimated for a number of sample/iterations for each methods.
    :param x_label: Label associated to x axis
    """
    area_stack_rand, area_stack_halton, area_stack_lhs, area_stack_orth  = y[0], y[1], y[2], y[3]
    nb_simulation, nb_area = np.shape(area_stack_rand)

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, dpi=150)

    for t in range(nb_simulation):
        rand_idx = np.random.randint(low=0, high=nb_area, size=50)
        ax1.scatter(x[rand_idx], area_stack_rand[t][rand_idx], s=0.5)
        ax2.scatter(x[rand_idx], area_stack_halton[t][rand_idx], s=0.5)
        ax3.scatter(x[rand_idx], area_stack_lhs[t][rand_idx], s=0.5)
        ax4.scatter(x[rand_idx], area_stack_orth[t][rand_idx], s=0.5)

    ax1.set_title('Pure random')
    ax2.set_title('Halton sequence')
    ax3.set_title('Latin hypercube')
    ax4.set_title('Orthogonal')

    ax2.set_xlabel(x_label)
    ax1.set_ylabel('Area of Mandelbrot set')

    ax1.set_ylim(1, 2)
    ax2.set_ylim(1, 2)
    ax3.set_ylim(1, 2)
    ax4.set_ylim(1, 2)

    plt.show()


def plot_convergence_difference(x, y, xlabel):
    """
    Plot relative difference between min/max of simulation set for 3 different methods at log scale.
    :param x: values considered for variance
    :param y: maximal difference between minimal and maximal estimated area among simulations
    :param xlabel: Title associated to x axis
    """
    max_d_r, max_d_h, max_d_l, max_d_o = y[0], y[1], y[2], y[3]

    fig, ax = plt.subplots(dpi=150)

    ax.set_title('Maximum difference within simulation results')
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Maximum difference within a set of simulation')

    ax.plot(x, max_d_r, linewidth=0.5, label='Pure random')
    ax.plot(x, max_d_h, linewidth=0.5, label='Halton sequence')
    ax.plot(x, max_d_l, linewidth=0.5, label='Latin Hypercube')
    ax.plot(x, max_d_o, linewidth=0.5, label='Orthogonal')

    plt.legend()
    plt.show()


def plot_convergence_variance(x, y, xlabel):
    """
    Plot variance of simulation set for 3 different methods at log scale.
    :param x: values considered for variance
    :param y: variance
    :param xlabel: Title associated to x axis
    """
    max_d_r, max_d_h, max_d_l, max_d_o = y[0], y[1], y[2], y[3]

    fig, ax = plt.subplots(dpi=150)

    ax.set_title('Variance of simulation results')
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Variance')

    ax.loglog(x, max_d_r, linewidth=0.5, label='Pure random')
    ax.loglog(x, max_d_h, linewidth=0.5, label='Halton sequence')
    ax.loglog(x, max_d_l, linewidth=0.5, label='Latin hypercube')
    ax.loglog(x, max_d_o, linewidth=0.5, label='Orthogonal')

    plt.legend()
    plt.show()


def example_sample():
    """
    Plot distribution of sampling methods (pure random, halton sequence sampling) in a grid.
    """
    x_rand, y_rand = sm.pure_random(600, 400, 1000)
    x_hal, y_hal = sm.halton_sequence(600, 400, 1000)

    fig, ax = plt.subplots(dpi=130)
    ax.set_xlabel('Grid Width', fontsize=15)
    ax.set_ylabel('Grid Height', fontsize=15)
    ax.set_title('Pure Random Sampling', fontsize=15)
    plt.scatter(x_rand, y_rand, color='coral', s = 1)
    plt.show()

    fig, ax = plt.subplots(dpi=130)
    ax.set_xlabel('Grid Width', fontsize=15)
    ax.set_ylabel('Grid Height', fontsize=15)
    ax.set_title('Quasi-Random Halton Sampling', fontsize=15)
    plt.scatter(x_hal, y_hal, color='coral', s = 1)
    plt.show()


