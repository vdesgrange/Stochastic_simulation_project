import numpy as np

import mandelbrot
from statistical_analysis_utils import recursive_sample_mean, recursive_sample_variance, confidence_interval
from monte_carlo import monte_carlo_integration
from sampling_method import pure_random


def confidence_interval_estimate(l=0.02, k=100, s=1000, i=800):
    """
    Compute mandelbrot set area sample mean, variance and confidence interval (assuming central limit theorem).
    :param l:
    :param k: Minimal number of simulation to run
    :return: sample mean, sample variance and confidence interval
    """
    x = []
    s2_ = x0_ = x1_ = 0
    interval = 1

    while k > 0 or interval >= l:
        a, _, _ = monte_carlo_integration(
            width=mandelbrot.WIDTH,
            height=mandelbrot.HEIGHT,
            re=(mandelbrot.RE_MIN, mandelbrot.RE_MAX),
            im=(mandelbrot.IM_MIN, mandelbrot.IM_MAX),
            s=s,
            i=i,
            sampling_method=pure_random)
        x.append(a)

        x1_ = recursive_sample_mean(a, x0_, len(x) - 1)
        s2_ = recursive_sample_variance(s2_, x1_, x0_, len(x) - 1)
        x0_ = x1_
        min, max, interval = confidence_interval(x1_, np.sqrt(s2_), 0.05, len(x))
        k -= 1

    return x1_, s2_, min, max


if __name__ == '__main__':
    print("Determine confidence interval...")
    x_, s2_, min, max = confidence_interval_estimate(l=0.02, k=100)
    print("Sample mean x_ =", x_)
    print("Sample variance s2_ =", s2_)
    print("Confidence interval, min={:5f}, max ={:5f} ".format(min, max))
    print("Done.")