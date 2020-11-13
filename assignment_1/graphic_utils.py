import matplotlib.pyplot as plt
from curve_utils import estimate_polyfit
from numpy.polynomial import Polynomial
from numpy.polynomial.polynomial import polyval

# Hexadecimal colour scheme for mandelbrot visualisation
# https://coolors.co
palette = ['#060A0F', '#0B141E', '#111E2D', '#16283C', '#1C324A', '#213C59', '#274668', '#2C5077', '#325A86',
           '#376495', '#3D6EA4', '#4279B3', '#4C83BD', '#5B8DC2', '#6A97C8', '#6D9AC9', '#88ACD3', '#97B7D8',
           '#A6C1DE', '#B5CBE3', '#C3D6E9', '#D2E0EE', '#E1E4F4', '#F0F5F9', '#FFFFFF']


def difference_plot_by_iteration(x, y):
    fig, ax = plt.subplots(dpi=150)
    ax.set_xlabel('Number of iterations j')
    ax.set_ylabel(r'$|A_{js} - A_{is}|$')
    ax.set_title(r'Evolution of $|A_{js} - A_{is}|,\ \forall j < i$')
    ax.loglog(x, y, color='coral', linewidth='.5')
    plt.show()

def difference_plot_by_iteration_q3(x_rand, y_rand, x_lhs, y_lhs, x_orth, y_orth):
    fig, ax = plt.subplots(dpi=130)
    ax.set_xlabel('Number of iterations j', fontsize=15)
    ax.set_ylabel(r'$|A_{js} - A_{is}|$', fontsize=17)
    ax.set_title(r'Evolution of $|A_{js} - A_{is}|,\ \forall j < i$', fontsize=15)
    ax.plot(x_rand, y_rand, color='coral', label='Pure Random')
    ax.plot(x_lhs, y_lhs, color='seagreen', label='LHS')
    ax.plot(x_orth, y_orth, color='hotpink', label='Orthogonal')
    plt.yscale('log')
    plt.legend(fontsize=15)
    plt.tick_params(labelsize=15)
    plt.show()

def difference_plot_by_sampling(x, y):
    fig, ax = plt.subplots(dpi=150)
    ax.set_xlabel('Number of sampling t')
    ax.set_ylabel(r'$|A_{it} - A_{is}|$')
    ax.set_title(r'Evolution of $|A_{it} - A_{is}|,\ \forall t < s$')
    ax.loglog(x, y, color='coral', linewidth='.5')
    plt.show()


def convergence_plot_by_sampling_method(x_rand, y_rand, x_halton, y_halton, x_lhs, y_lhs):
    fig, ax = plt.subplots(dpi=150)
    ax.set_xlabel('Number of sampling t')
    ax.set_ylabel(r'$|A_{it} - A_{is}|$')
    ax.set_title(r'Convergence Behaviour by sampling method')
    ax.scatter(x_rand, y_rand, color='coral', label='Random', s=0.5)  # x_rand[::500], y_rand[::500]
    #ax.scatter(x_halton, y_halton, color='orchid', label='Halton', s=0.5)  # x_halton[::500], y_halton[::500]
    #ax.scatter(x_lhs, y_lhs, color='lightskyblue', label='LHS', s=0.5)  # x_lhs[::500], y_lhs[::500]
    # ax.plot(x_orth, y_orth, color='lightskyblue', linewidth='.5', label='Orthogonal')

    #x = [x_rand, x_halton, x_lhs]
    #y = [y_rand, y_halton, y_lhs]
    #labels=['Poly Pure Random', 'Poly Halton Sampling', 'POly Latin HyperSquare']
    x = [x_rand]
    y = [y_rand]
    labels=['Poly Pure Random']

    ## x is a list of numpy arrays
    ## y is a list of numpy arrays
    ## labels is a list of strings
    plt.title('Polynomial Fit of Convergence')
    for i in range(0, len(labels)):  
        p = Polynomial.fit(x[i], y[i], 15)
        plt.plot(*p.linspace(), label=labels[i])
        # print('Slope of ', labels[i], ' at 100 ', slope(p, 100))
    plt.legend()
    plt.show()

    # estimate_polyfit([x_rand, x_halton, x_lhs, x_orth], [y_rand, y_halton, y_lhs, y_orth], labels=['Pure Random', 'Halton Sampling', 'Latin HyperSquare', 'Orthogonal'])
    # estimate_polyfit([x_rand, x_halton, x_lhs], [y_rand, y_halton, y_lhs], labels=['Pure Random', 'Halton Sampling', 'Latin HyperSquare'])

def complex_plan_plot(re, im):
    fig, ax = plt.subplots(dpi=150)
    ax.set_xlabel('Re')
    ax.set_ylabel('Im')
    ax.set_title(r'Convergence of complex number $c \approx {:3f} + ({:3f})i$'.format(re[0], im[0]))
    ax.plot(re, im, color='lightskyblue', marker='o', linewidth='.5')
    plt.show()


def sampling_scatter_plot(x_samples, y_samples):
    fig, ax = plt.subplots(dpi=150)
    ax.scatter(x_samples, x_samples, color='coral', s=0.5)
    plt.title('Sampling Scatter')
    ax.set_xlabel('X Sample')
    ax.set_ylabel('Y Sample')
    plt.show()
