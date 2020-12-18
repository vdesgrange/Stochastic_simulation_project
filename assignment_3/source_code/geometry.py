import math
import numpy as np


def total_distance(nodes, order):
	total = 0
	x = nodes[0, :]
	y = nodes[1, :]
	for i in range(0, len(order) - 1):
		total += euclidean_distance((x[order[i]], y[order[i]]), (x[order[i + 1]], y[order[i + 1]]))
	total += euclidean_distance((x[order[-1]], y[order[-1]]), (x[order[0]], y[order[0]]))
	return total

# uses precalculated distance matrix to compute total path length, significant speed increase
def total_distance_precalc(nodes, order, dist):
	total = 0
	for i in range(0, len(order) - 1):
		total += dist[order[i], order[i + 1]] 
	total += dist[order[-1], order[0]]
	return total

def euclidean_distance(node0, node1):
	x0, y0 = node0
	x1, y1 = node1
	x_diff = x1-x0
	y_diff = y1-y0
	return math.sqrt(x_diff**2 + y_diff**2)

def distance_matrix(nodes):
	dist = np.zeros((nodes.shape[1], nodes.shape[1]))
	for i in range(0, nodes.shape[1]):
		for j in range(0, nodes.shape[1]):
			dist[i, j] = euclidean_distance((nodes[0, i], nodes[1, i]), (nodes[0, j], nodes[1, j]))

	return dist