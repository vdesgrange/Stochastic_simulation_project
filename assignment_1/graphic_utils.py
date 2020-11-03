import matplotlib.pyplot as plt


def difference_plot_by_iteration(x, y):
    fig, ax = plt.subplots(dpi=300)
    ax.set_xlabel('Number of iterations j')
    ax.set_ylabel(r'$|A_{js} - A_{is}|$')
    ax.set_title(r'Evolution of $|A_{js} - A_{is}|,\ \forall j < i$')
    ax.loglog(x, y, color='coral', linewidth='.5')
    plt.show()


def difference_plot_by_sampling(x, y):
    fig, ax = plt.subplots(dpi=300)
    ax.set_xlabel('Number of sampling t')
    ax.set_ylabel(r'$|A_{it} - A_{is}|$')
    ax.set_title(r'Evolution of $|A_{it} - A_{is}|,\ \forall t < s$')
    ax.loglog(x, y, color='coral', linewidth='.5')
    plt.show()

def convergence_plot_by_sampling_method(x_rand, y_rand, x_halton, y_halton):
    fig, ax = plt.subplots(dpi=200)
    ax.set_xlabel('Number of sampling t')
    ax.set_ylabel(r'$|A_{it} - A_{is}|$')
    ax.set_title(r'Convergence Behaviour of Pure Random vs Halton Sampling')
    ax.plot(x_rand[::500], y_rand[::500], color='coral', linewidth='.5', label='Random')
    ax.plot(x_halton[::500], y_halton[::500], color='red', linewidth='.5', label='Halton')
    plt.yscale('log')
    plt.legend()
    plt.show()

def complex_plan_plot(re, im):
    fig, ax = plt.subplots(dpi=300)
    ax.set_xlabel('Re(A[n])')
    ax.set_ylabel('Im(A[n])')
    ax.set_title(r'Convergence of complex number $c \approx {:3f} + ({:3f})i$'.format(re[0], im[0]))
    ax.plot(re, im, color='lightskyblue', marker='o', linewidth='.5')
    plt.show()

def sampling_scatter_plot(x_samples, y_samples):
    fig, ax = plt.subplots(dpi=300)
    ax.scatter(x_samples, x_samples, color='coral', s = 0.5)
    plt.title('Sampling Scatter')
    ax.set_xlabel('X Sample')
    ax.set_ylabel('Y Sample')
    plt.show()