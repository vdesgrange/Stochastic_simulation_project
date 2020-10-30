import numpy as np


def monte_carlo_integration(grid, width, height, re, im):
    """
    Monte-carlo integration algorithm.
    Estimates the surface value of a complex plan.
    :param grid: Numpy array(h, w) of values i in (0, 1). Within the surface is 1, outside the surface is 0.
    :param width: width of the plan
    :param height: height of the plan
    :param re: tuple of minimal and maximal coordinates of real axis
    :param im: tuple of minimal and maximal coordinates of imaginary axis.
    :return: Estimation of the surface in complex units.
    """
    # Get grid wight and height
    w, h = width, height
    # Get real and imaginary minimal and maximal axis coordinates.
    re_min, re_max = re[0], re[1]
    im_min, im_max = im[0], im[1]

    # Get information about amount of possible values (0, 1) and number of them.
    unique, counts = np.unique(grid, return_counts=True)  # If we have this information, what's the purpose of Monte-Carlo ???
    print(dict(zip(unique, counts)))

    # Choose n random grid points to sample
    n, count = 100000, 0
    y_samp = np.random.randint(0, h, n)
    x_samp = np.random.randint(0, w, n)
    # y_samp = [int(round(y)) for y in np.random.uniform(0, h - 1, n).tolist()]  # Use np.random.randint instead ?
    # x_samp = [int(round(x)) for x in np.random.uniform(0, w - 1, n).tolist()]

    for j in range(0, n):
        if grid[y_samp[j], x_samp[j]] == 1:
            count += 1

    # Proportion of sample points within the set
    prop = count / n

    # Area of the complex plane
    a = (re_max - re_min) * (im_max - im_min)
    # a = (abs(re_min) + abs(re_max)) * (abs(im_min) + abs(im_max))  # (RE_MAX - RE_MIN) * (IM_MAX - IM_MIN)

    # Scale proportion to the size of our complex plane
    est = prop * a

    print('Estimation of area is %f' % (est))

    return est
