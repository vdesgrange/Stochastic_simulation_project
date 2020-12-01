import matplotlib.pyplot as plt


def simple_plotter(xs, ys, labels, title, x_axis, y_axis):
    fig, ax = plt.subplots(dpi=150)

    for i in range(len(xs)):
        x, y, label = xs[i], ys[i], labels[i]
        ax.plot(x, y, label=label)

    plt.ylabel(y_axis, fontsize=13)
    plt.xlabel(x_axis, fontsize=13)
    plt.title(title, fontsize=13)
    plt.legend(fontsize=13)
    plt.tick_params(labelsize=13)
    plt.show()


def y_log_plotter(xs, ys, labels, title, x_axis, y_axis):
    fig, ax = plt.subplots(dpi=150)

    for i in range(len(xs)):
        x, y, label = xs[i], ys[i], labels[i]
        ax.plot(x, y, label=label)

    plt.yscale(r'log')
    plt.ylabel(y_axis, fontsize=13)
    plt.xlabel(x_axis, fontsize=13)
    plt.title(title, fontsize=13)
    plt.legend(fontsize=13)
    plt.tick_params(labelsize=13)
    plt.show()


def kde_plotter(xs, ys, labels, title):
    fig, ax = plt.subplots(dpi=150)

    for i in range(len(ys)):
        x, y, label = xs[i], ys[i], labels[i]
        ax.plot(x, y, lw=2, label=label)

    plt.xlim(-2, 8)
    plt.legend(loc='best')
    plt.xlabel(r'$E_1(W)$', fontsize=13)
    plt.ylabel('Density', fontsize=13)
    plt.title(title, fontsize=13)
    plt.tick_params(labelsize=13)
    plt.show()


def box_plot(data, labels, title, ylabel):
    fig, ax = plt.subplots(dpi=150)
    red_square = dict(markerfacecolor='r', marker='s')
    ax.set_title(title, fontsize=13)
    ax.boxplot(data, flierprops=red_square, notch = True, labels = labels)
    plt.tick_params(labelsize=13)
    plt.ylabel(ylabel, fontsize=13)
    plt.show()


def sample_stat_rho(rho, xs, line_labels, x_label, y_label, title, scale):
    fig, ax = plt.subplots(dpi=150)

    for j in range(len(xs)):
        plt.plot(rho, xs[j], label=line_labels[j])

    plt.ylabel(y_label, fontsize=13)
    plt.xlabel(x_label, fontsize=13)
    plt.yscale(scale)
    plt.title(title, fontsize=13)
    plt.legend(fontsize=13)
    plt.tick_params(labelsize=13)
    plt.show()