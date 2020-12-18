import math
import numpy as np
from collections import namedtuple
import geometry
import utils
import graphics
import stats

CoolingSchedule = namedtuple('CoolingSchedule', ['T', 'steps', 'lowering_method', 'annealing_condition'])

default = CoolingSchedule(
	T=80,
	steps=80,
	lowering_method=(lambda t: .9 * t),
	annealing_condition=(lambda i: i < 50),
)

# Global statistics
Rates = []
Cost_difference = []


def simulated_annealing(initial_order, nodes, cooling_schedule=default, distance_matrix=np.array([])):
	order = initial_order
	T = cooling_schedule.T
	steps = cooling_schedule.steps

	costs = []

	global Rates, Cost_difference
	Rates = []
	Cost_difference = []

	j = 0
	while j < steps:
		# Reduce temperature on each iteration of the outer loop
		T = cooling_schedule.lowering_method(T)

		## Inner loop
		i = 0
		k = 0
		acceptance_rate = 0
		cost_difference = 0
		while cooling_schedule.annealing_condition(i):  #(i < chain_size):
			new_order = order.copy()
			# select a random start and end in the current path
			start, end = np.sort(np.random.randint(0, len(order), size=2))  # - 1
			# flip coin to decide between reverse and transport 
			# 0 = reverse
			# 1  = transport 
			bin = np.random.choice([0, 1])
			if bin == 0:
				# Reverse the sublist
				new_order[start:end] = reversed(new_order[start:end])
			else:
				# Transport
				sublist = new_order[start:end]
				del new_order[start:end]
				# random position to splice sub-list
				splice = np.random.randint(0, len(new_order))  # - 1
				new_order = new_order[:splice] + sublist + new_order[splice:]

			if distance_matrix.size != 0:	
				dist_orig = geometry.total_distance_precalc(nodes, order, distance_matrix)
				dist_new = geometry.total_distance_precalc(nodes, new_order, distance_matrix)
			else:
				dist_orig = geometry.total_distance(nodes, order)
				dist_new = geometry.total_distance(nodes, new_order)

			cost_diff = dist_new - dist_orig

			if cost_diff < 0:
				order = new_order.copy()
				costs.append(dist_new)
			else:
				p = math.exp((-1 * cost_diff) / T)
				u = np.random.uniform(0.0, 1.0)
				k += 1
				cost_difference += cost_diff
				if u < p:
					order = new_order.copy()
					costs.append(dist_new)
					acceptance_rate += 1
				else:
					costs.append(dist_orig)

			i += 1

		Rates.append(acceptance_rate / k)
		Cost_difference.append(cost_difference / k)
		j += 1

	return order, costs


def simulated_annealing_relative(initial_order, nodes, cooling_schedule=default, distance_matrix=np.array([])):
	order = initial_order
	T = cooling_schedule.T
	steps = cooling_schedule.steps

	global Rates, Cost_difference
	Rates = []
	Cost_difference = []
	Costs = []

	j = 0
	while j < steps:
		# Reduce temperature on each iteration of the outer loop
		T = cooling_schedule.lowering_method(T, j)

		## Inner loop
		i = 0
		k = 1
		acceptance_rate = 0
		cost_difference = 0
		cost = 0
		while cooling_schedule.annealing_condition(i):  #(i < chain_size):
			new_order = order.copy()
			# select a random start and end in the current path
			start, end = np.sort(np.random.randint(0, len(order), size=2))  # - 1
			# flip coin to decide between reverse and transport
			# 0 = reverse
			# 1  = transport
			bin = np.random.choice([0, 1])
			if bin == 0:
				# Reverse the sublist
				new_order[start:end] = reversed(new_order[start:end])
			else:
				# Transport
				sublist = new_order[start:end]
				del new_order[start:end]
				# random position to splice sub-list
				splice = np.random.randint(0, len(new_order))  # - 1
				new_order = new_order[:splice] + sublist + new_order[splice:]

			if distance_matrix.size != 0:
				dist_orig = geometry.total_distance_precalc(nodes, order, distance_matrix)
				dist_new = geometry.total_distance_precalc(nodes, new_order, distance_matrix)
			else:
				dist_orig = geometry.total_distance(nodes, order)
				dist_new = geometry.total_distance(nodes, new_order)

			cost_diff = (dist_new - dist_orig) / dist_orig
			cost_difference += cost_diff

			if cost_diff < 0:
				order = new_order.copy()
				cost += dist_new
			else:
				p = math.exp((-1 * cost_diff) / T)
				u = np.random.uniform(0.0, 1.0)
				k += 1
				if u < p:
					order = new_order.copy()
					cost += dist_new
					acceptance_rate += 1
				else:
					cost += dist_orig

			i += 1

		Costs.append(cost / i)
		Rates.append(acceptance_rate / k)
		Cost_difference.append(cost_difference / i)
		j += 1

	return order, Costs


def random_permutation(initial_order, chain_size, nodes, distance_matrix=np.array([])):
	order = initial_order
	i = 0
	cost_difference = []

	while i < chain_size:
		new_order = order.copy()
		start, end = np.sort(np.random.randint(0, len(order), size=2))  # - 1
		bin = np.random.choice([0, 1])
		if bin == 0:
			# Reverse the sublist
			new_order[start:end] = reversed(new_order[start:end])
		else:
			# Transport
			sublist = new_order[start:end]
			del new_order[start:end]
			# random position to splice sub-list
			splice = np.random.randint(0, len(new_order))  # - 1
			new_order = new_order[:splice] + sublist + new_order[splice:]

		if distance_matrix.size != 0:
			dist_orig = geometry.total_distance_precalc(nodes, order, distance_matrix)
			dist_new = geometry.total_distance_precalc(nodes, new_order, distance_matrix)
		else:
			dist_orig = geometry.total_distance(nodes, order)
			dist_new = geometry.total_distance(nodes, new_order)

		cost_diff = abs(dist_new - dist_orig) / dist_orig
		cost_difference.append(cost_diff)
		order = new_order.copy()
		i += 1

	return cost_difference


if __name__ == '__main__':

	# Case eil51
	nodes = utils.tsp_reader('../../Documents/TSP-Configurations/eil51.tsp.txt')
	traveling_list = utils.initial_perm(nodes)
	graphics.node_graph(nodes, traveling_list)

	print('Total distance of initial random order: ', geometry.total_distance(nodes, traveling_list))

	cooling_schedule = CoolingSchedule(
		T=80,
		steps=100,
		lowering_method=(lambda t: .9 * t),
		annealing_condition=(lambda i: i < 250),
	)

	optimized_traveling_list, _ = simulated_annealing(traveling_list, nodes, cooling_schedule)
	print('Final order', optimized_traveling_list)
	print('Total distance of final order: ', geometry.total_distance(nodes, optimized_traveling_list))
	graphics.node_graph(nodes, optimized_traveling_list)
