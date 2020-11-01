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


def complex_plan_plot(re, im):
    fig, ax = plt.subplots(dpi=300)
    ax.set_xlabel('Re(A[n])')
    ax.set_ylabel('Im(A[n])')
    ax.set_title(r'Convergence of complex number $c \approx {:3f} + ({:3f})i$'.format(re[0], im[0]))
    ax.plot(re, im, color='lightskyblue', marker='o', linewidth='.5')
    plt.show()