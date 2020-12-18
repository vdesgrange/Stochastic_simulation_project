import numpy as np


def initial_perm(nodes):
	return np.random.permutation(nodes.shape[1]).tolist()


def tsp_reader(file_path):
	with open(file_path, 'r') as file:
		x = [l.rstrip('\n') for l in file]

	print("=== Loading TSP file... ===")
	name = x[0]
	print("Name : ", name)
	print("Comment : ", x[1])
	print("Type : ", x[2])
	print("Number of cities : ", x[3])
	print("Distance type : ", x[4])

	# remove header information
	x = x[6:-1]

	#if name == 'a280':
		#del x[170]  # remove duplicate node

	nodes = np.zeros((2, len(x)))
	for i in range(0, len(x)):
		split = x[i].rstrip().split()
		nodes[0, i] = float(split[1])
		nodes[1, i] = float(split[2])

	return nodes


def tsp_solution_reader(solution_path):
	with open(solution_path, 'r') as file:
		x = [l.rstrip('\n') for l in file]

	name = x[0]
	# remove header information
	x = x[5:-2]

	#if name == './TSPLIB/a280.tsp.optbc.tour':
		#del x[109]  # remove duplicate node

	solutions = []
	for i in range(len(x)):
		solutions.append(int(x[i]) - 1)

	return solutions

