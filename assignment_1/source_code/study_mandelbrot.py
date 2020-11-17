import numpy as np
import mandelbrot
import graphic_utils
from monte_carlo import monte_carlo_integration

RE = (mandelbrot.RE_MIN, mandelbrot.RE_MAX)
IM = (mandelbrot.IM_MIN, mandelbrot.IM_MAX)
WIDTH = mandelbrot.WIDTH
HEIGHT = mandelbrot.HEIGHT


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
    idx = np.random.choice(np.argwhere(details == max_i)[:, 0], 20)

    # Sample of complex numbers which converge for at least max_i iterations.
    sample = np.array(complex_sample)[idx]

    for val in sample:
        convergence(val, max_i)


def example_convergence():
    c1 = complex(-0.075255, -0.223533)
    convergence(c1, 1000)

    c2 = complex(0.328161, -0.310280)
    convergence(c2, 1000)

    c3 = complex(-0.695456, -0.287956)
    convergence(c3, 1000)


if __name__ == '__main__':
    study_convergence_mandelbrot()
    example_convergence()
