import numpy as np

import mandelbrot
from statistical_analysis_utils import recursive_sample_mean, recursive_sample_variance, confidence_interval
from monte_carlo import monte_carlo_integration
from sampling_method import pure_random, halton_sequence


def confidence_interval_estimate(l, k, s, i, re, im, w, h, sampling_method=pure_random):
    """
    Compute mandelbrot set area sample mean, variance and confidence interval (assuming central limit theorem).
    :param l:
    :param k: Minimal number of simulation to run
    :param s: Number of samples for Monte carlo
    :param i: Maximal number of iteration
    :param sampling_method: sampling method used
    :return: sample mean, sample variance and confidence interval
    """
    x = []
    s2_ = x0_ = x1_ = 0
    interval = 1
    it = 0

    while it < k or interval >= l:
        a, _, _ = monte_carlo_integration(re, im, w, h, s, i, sampling_method)
        x.append(a)

        x1_ = recursive_sample_mean(a, x0_, len(x) - 1)
        s2_ = recursive_sample_variance(s2_, x1_, x0_, len(x) - 1)
        x0_ = x1_
        min, max, interval = confidence_interval(x1_, np.sqrt(s2_), 0.05, len(x))
        it += 1

    print("Number of simulation :", it)
    return x1_, s2_, min, max


if __name__ == '__main__':
    print("Determine confidence interval...")
    x_, s2_, min, max = confidence_interval_estimate(
        l=0.02,
        k=100,
        s=1000,
        i=800,
        re=(mandelbrot.RE_MIN, mandelbrot.RE_MAX),
        im=(mandelbrot.IM_MIN, mandelbrot.IM_MAX),
        w=mandelbrot.WIDTH,
        h=mandelbrot.HEIGHT,
        sampling_method=pure_random)
    print("Sample mean x_ =", x_)
    print("Sample variance s2_ =", s2_)
    print("Confidence interval, min={:5f}, max ={:5f} ".format(min, max))
    print("Done.")