import numpy as np
from subprocess import Popen, PIPE
import math
import time
import mandelbrot
import chaospy
import matplotlib.pyplot as plt

def pure_random(w, h, n):
	return (np.random.uniform(0, w, n), np.random.uniform(0, h, n))    

"""
orthogonal sampling for fixed w, h, n
sampling properties are set in the compiled c file. Yet to 
figure out how to pass arguments, this is the next step .. 
"""
def orthogonal():
	x_samples = []
	y_samples = []
	with Popen(['./ortho'], stdout=PIPE, bufsize=1, universal_newlines=True) as p:
		for line in p.stdout:
			vals = line.split()
			x_samples.append(float(vals[0]))
			y_samples.append(float(vals[1]))
	return (np.array(x_samples), np.array(y_samples))

"""
Performance is not good at the moment...
Although, I think there are some obvious improvements to be made

"""
def latin_square(w, h, n):
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
	distribution = chaospy.J(chaospy.Uniform(0, w), chaospy.Uniform(0, h))
	samples = distribution.sample(n, rule="halton")
	return (samples[0], samples[1])

def monte_carlo_integration(width, height, re, im, s=100000, i=mandelbrot.MAX_ITER, method='pure_random'):
	"""
	Monte-carlo integration algorithm.
	Estimates the surface value of a complex plan.
	:param grid: Numpy array(h, w) of values i in (0, 1). Within the surface is 1, outside the surface is 0.
	:param width: width of the plan
	:param height: height of the plan
	:param re: tuple of minimal and maximal coordinates of real axis
	:param im: tuple of minimal and maximal coordinates of imaginary axis.
	:return: Array of estimation of the surface in complex units.
	"""
	# Get grid wight and height
	w, h = width, height
	# Get real and imaginary minimal and maximal axis coordinates.
	re_min, re_max = re[0], re[1]
	im_min, im_max = im[0], im[1]
	# Area of the complex plane
	a = (re_max - re_min) * (im_max - im_min)

	# Choose n random grid points to sample
	n, count = s, 0

	# choose sampling method based on kwarg
	if(method == 'halton'):
		x_samp, y_samp = halton_sequence(w, h, n)
	elif(method == 'latin_square'):
		x_samp, y_samp = latin_square(w, h, n)
	elif(method == 'orthogonal'):
		x_samp, y_samp = orthogonal()
	else:
		x_samp, y_samp = pure_random(w, h, n)
	
	# Running time
	start_time = time.time()

	# Convert euclidian coordinates sample to complex
	samples = list(map(lambda x, y: mandelbrot.grid_map(x, y, (re_min, re_max), (im_min, im_max)), x_samp, y_samp))

	details = np.zeros(s)  # Keep track of number of iterations per sample
	for idx, c in enumerate(samples):
		res = mandelbrot.mandelbrot(c, i)
		count += int(res == i)
		details[idx] = res  # Store number of iteration reach for each complex number

	# Proportion of sample points within the set scaled to size of complex plane
	estimate = (count / s) * a

	print("--- %s seconds ---" % (time.time() - start_time))
	print('Estimation of mandelbrot surface is %f' % (estimate))

	return estimate, samples, details


if __name__ == '__main__':
	monte_carlo_integration(
		width=mandelbrot.WIDTH,
		height=mandelbrot.HEIGHT,
		re=(mandelbrot.RE_MIN, mandelbrot.RE_MAX),
		im=(mandelbrot.IM_MIN, mandelbrot.IM_MAX),
		s=100000,
		i=1000)