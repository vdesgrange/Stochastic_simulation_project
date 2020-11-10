import numpy as np
import chaospy
from subprocess import Popen, PIPE


def latin_square_chaos(w, h, n):
    samples = chaospy.create_latin_hypercube_samples(order=n, dim=2).round(4)
    return samples[0] * w, samples[1] * h  

def latin_square_custom(w, h, n):
    """
    Performance is not good at the moment...
    Although, I think there are some obvious improvements to be made
    """
    # we subdivide both axis into n chunks
    x_chunks = np.linspace(0, w, num=n)
    y_chunks = np.linspace(0, h, num=n)

    # storing our results
    x_samples = np.zeros(n)
    y_samples = np.zeros(n)

    """
    Use a binary grid to keep track of which rows and columns have been filled
    In practice, the grid is too large for memory
    grid = np.empty((n, n), dtype = 'int8')
    Instead, lets just store the co-ordinates of 'filled' grid squares as a list of tuples 
    """
    filled_squares = []

    """
    Iterate over each column
    first, generate an x value in the given column
    then, generate a y value. Check if the y value falls within
    a chunk for which we already have a sample, if it does,
    then repeat the process until we get a y value which does
    not fall in a chunk for which there is already a value
    """
    for j in range(x_chunks.shape[0] - 1):
        # track whether we have obtain a y value which meets our criteria
        track = False
        while(track != True):
            # generate an x value in the current chunk
            x_val = np.random.uniform(x_chunks[j], x_chunks[j + 1])
            # now take a sample from entire range of h
            y_val = np.random.uniform(0, h)
            # get y chunk index in which the value falls
            y_ind = np.where(y_chunks == np.max(y_chunks[y_chunks < y_val]))
            # check if a value has already been generated for this row
            if (j, y_ind) not in filled_squares:
                track = True
                # store our column and row index so that we don't
                # generate another value in this 'cell'
                filled_squares.append((j, y_ind))
                x_samples[j] = x_val
                y_samples[j] = y_val

    return (x_samples, y_samples)


def halton_sequence(w, h, n):
    """
    halton sequence sampling
    """
    distribution = chaospy.J(chaospy.Uniform(0, w), chaospy.Uniform(0, h))
    samples = distribution.sample(n, rule="halton")
    return samples[0], samples[1]


def orthogonal(w, h, n):
    """
    orthogonal sampling for fixed w, h, n
    sampling properties are set in the compiled c file. Yet to
    figure out how to pass arguments, this is the next step ..
    """
    x_samples = []
    y_samples = []
    with Popen(['./ortho'], stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            vals = line.split()
            x_samples.append(float(vals[0]))
            y_samples.append(float(vals[1]))

    return np.array(x_samples), np.array(y_samples)


def pure_random(w, h, n):
    return np.random.uniform(0, w, n), np.random.uniform(0, h, n)
