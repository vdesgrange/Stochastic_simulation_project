import numpy as np
from scipy.stats import norm


def recursive_sample_mean(xj, xj_, j):
    """
    Compute next value of sample mean
    :param xj: latest output result at j
    :param xj_: sample mean of j first output data
    :param j: length of j first data
    :return: sample mean for j+1 values
    """
    return xj_ + ((xj - xj_) / (j + 1))


def recursive_sample_variance(s2_, xj_1, xj_, j):
    """
    Compute next value of sample variance.
    :param s2_: latest sample variance computed at j
    :param xj_1: sample mean for j+1 first output data
    :param xj_: sample mean for j first output data
    :param j: length of j first data
    :return: sample variance for j+1 values
    """
    if j < 2:
        return 0

    return (1 - (1 / j)) * s2_ + (j + 1) * (xj_1 - xj_)**2


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


"""
Why are we using the inverse survival function here? 
"""
def confidence_interval_isf(x_, s_, alpha, n):
    """
    Compute confidence interval estimate of theta, the expected population value.
    :param x_: sample mean
    :param s_: sample standard deviation
    :param alpha: probability of being outside confidence interval
    :return: min/max/length of confidence interval estimate range
    """
    z = norm.isf(alpha / 2., 0, 1)

    min = x_ - z * (s_ / np.sqrt(n))
    max = x_ + z * (s_ / np.sqrt(n))
    len = 2 * z * (s_ / np.sqrt(n))

    return min, max, len

## James' implementation
def confidence_interval_ppf(x_, s_, alpha, n):

    p = 1 - alpha
    z = norm.ppf((p + 1) / 2.)

    min = x_ - z * (s_ / np.sqrt(n))
    max = x_ + z * (s_ / np.sqrt(n))
    len = 2 * z * (s_ / np.sqrt(n))

    return min, max, len
