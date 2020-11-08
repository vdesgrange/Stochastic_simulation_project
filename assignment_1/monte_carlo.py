import numpy as np
import time
import mandelbrot

from sampling_method import halton_sequence, latin_square, orthogonal, pure_random


def monte_carlo_integration(width, height, re, im, s=100000, i=mandelbrot.MAX_ITER, sampling_method=pure_random):
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
	x_samp, y_samp = sampling_method(w, h, n)

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

	# print("--- %s seconds ---" % (time.time() - start_time))
	# print('Estimation of mandelbrot surface is %f' % (estimate))

	return estimate, samples, details


if __name__ == '__main__':
	monte_carlo_integration(
		width=mandelbrot.WIDTH,
		height=mandelbrot.HEIGHT,
		re=(mandelbrot.RE_MIN, mandelbrot.RE_MAX),
		im=(mandelbrot.IM_MIN, mandelbrot.IM_MAX),
		s=100000,
		i=1000,
		sampling_method=halton_sequence)