import numpy as np
from scipy.stats import norm


def sample_mean(x):
    """
    Compute sample mean X: arithmetic average of the n data values (output)
    :param x: output data, independent random variables.
    :return: sample mean, float64
    """
    return np.mean(x, dtype=np.float64)


def sample_variance(x):
    """
    Compute sample variance S^2, estimator of population variance.
    :param x: output data, independent random variables.
    :return: sample variance, float64
    """
    x_ = sample_mean(x)
    n = np.shape(x)[0]
    return np.true_divide(np.sum(np.power((x - x_), 2)), n - 1)


def sample_standard_deviation(x):
    """
    Compute sample standard deviation S, estimator of sigma.
    :param x: output data, independent random variables.
    :return: sample standard deviation, float64
    """
    return np.sqrt(sample_variance(x))


def confidence_interval(x, alpha):
    """
    Compute confidence interval estimate of theta, the expected population value.
    :param x: output data, independent random variables.
    :param alpha: probability of being outside confidence interval
    :return: min/max/length of confidence interval estimate range
    """
    n = np.shape(x)[0]
    x_ = sample_mean(x)
    s = sample_standard_deviation(x)
    z = norm.isf(alpha / 2., 0, 1)

    min = x_ - z * (s / np.sqrt(n))
    max = x_ + z * (s / np.sqrt(n))
    len = 2 * z * (s / np.sqrt(n))

    return min, max, len