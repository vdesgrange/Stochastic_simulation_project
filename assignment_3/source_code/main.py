import numpy as np
import time
import graphics
import geometry
import annealing
import utils
import convergence
import stats
import archives
import statistics
import itertools
import matplotlib.pyplot as plt
from tabulate import tabulate


def question_initial_temperature():
	data = ['./tsp_data/eil51.tsp.txt', './tsp_data/a280.tsp.txt', './tsp_data/pcb442.tsp.txt']
	T_0s = [
		[1*10**-1, 5*10**-2, 3*10**-2, 1*10**-2],
		[1*10**-2, 7*10**-3, 4*10**-3, 1*10**-3, 7*10**-4],
		[1*10**-1, 1*10**-2, 6*10**-3, 4*10**-3, 1*10**-3],
	]

	for idx, path in enumerate(data):
		print("=== File {0} ===".format(path))

		nodes = utils.tsp_reader(path)
		distance_matrix = geometry.distance_matrix(nodes)

		x_means, y_means, labels = [], [], []
		x_diff_means, y_diff_means, diff_labels = [], [], []
		for T_0 in T_0s[idx]:
			print("=== Initial temperature {0} ===".format(path))

			# Experiment with geometric cooling schedule
			cooling_schedule = annealing.CoolingSchedule(
				T=T_0,
				steps=15,
				lowering_method=(lambda t, i: .9 * t),
				annealing_condition=(lambda i: i < 200),
			)
			_ = convergence.simulations(nodes, 20, cooling_schedule, distance_matrix, True)

			rates = np.array(convergence.Simulation_rates)  # rates length will be the same for each simulation in this case
			y_mean = np.mean(rates, axis=0)
			y_means.append(y_mean)
			x_means.append(range(len(y_mean)))
			labels.append(r'$T_0$ = {:.1e}'.format(T_0))
			print(tabulate([[y_mean]], headers=["Sample mean - acceptance rate"]))

			diff = np.array(convergence.Simulation_differences)
			y_diff_mean = np.mean(diff, axis=0)
			y_diff_means.append(y_diff_mean)
			x_diff_means.append(range(len(y_diff_mean)))
			diff_labels.append(r'$T_0$ = {:.1e}'.format(T_0))
			print(tabulate([[y_diff_mean]], headers=["Sample mean - cost difference"]))

		path = 'archives/initial_temperature_t0_{0}.npy'.format(int(time.time()))
		with open(path, 'ab') as f:
			np.save(f, x_means)
			np.save(f, y_means)
			np.save(f, labels)
			np.save(f, x_diff_means)
			np.save(f, y_diff_means)
			np.save(f, diff_labels)

		graphics.simple_plotter(x_means, y_means, labels, 'Evolution of mean acceptance rate', 'Steps', 'Mean acceptance rate')
		graphics.simple_plotter(x_diff_means, y_diff_means, diff_labels, 'Evolution of mean cost difference', 'Steps', 'Mean cost difference')


def question_initial_temperature_2():
	nodes = utils.tsp_reader('./tsp_data/eil51.tsp.txt')
	distance_matrix = geometry.distance_matrix(nodes)
	traveling_list = utils.initial_perm(nodes)
	eil51 = annealing.random_permutation(traveling_list, 1000, nodes, distance_matrix)

	nodes = utils.tsp_reader('./tsp_data/a280.tsp.txt')
	distance_matrix = geometry.distance_matrix(nodes)
	traveling_list = utils.initial_perm(nodes)
	a280 = annealing.random_permutation(traveling_list, 1000, nodes, distance_matrix)

	nodes = utils.tsp_reader('./tsp_data/pcb442.tsp.txt')
	distance_matrix = geometry.distance_matrix(nodes)
	traveling_list = utils.initial_perm(nodes)
	pcb442 = annealing.random_permutation(traveling_list, 1000, nodes, distance_matrix)

	data = [
		['eil51', np.mean(eil51), np.var(np.array(eil51)), stats.mean_confidence_interval(eil51)],
		['a280', np.mean(a280), np.var(np.array(a280)), stats.mean_confidence_interval(a280)],
		['pcb442', np.mean(pcb442), np.var(np.array(pcb442)), stats.mean_confidence_interval(pcb442)],
	]

	print(tabulate(data, headers=["Problem", "Mean c", "Variance c", "Confidence interval (0.95)"]))
	graphics.box_plot([eil51, a280, pcb442], ['eil51', 'a280', 'pcb442'], 'Average cost difference', r'E($\Lambda$ c)')


def question_cooling_schedule():
	# Case a280
	nodes = utils.tsp_reader('./tsp_data/a280.tsp.txt')
	distance = geometry.distance_matrix(nodes)

	cooling_schedule_1 = annealing.CoolingSchedule(
		T=4*10**-3,
		steps=400,
		lowering_method=(lambda t: .975 * t),
		annealing_condition=(lambda i: i < 250),
	)

	cooling_schedule_2 = annealing.CoolingSchedule(
		T=4*10**-3,
		steps=400,
		lowering_method=(lambda t: .95 * t),
		annealing_condition=(lambda i: i < 250),
	)

	cooling_schedule_3 = annealing.CoolingSchedule(
		T=4*10**-3,
		steps=400,
		lowering_method=(lambda t: .90 * t),
		annealing_condition=(lambda i: i < 250),
	)

	cooling_schedule_4 = annealing.CoolingSchedule(
		T=4*10**-3,
		steps=400,
		lowering_method=(lambda t: .75 * t),
		annealing_condition=(lambda i: i < 250),
	)

	cooling_schedules = [cooling_schedule_1, cooling_schedule_2, cooling_schedule_3, cooling_schedule_4]
	xs_mean = []
	ys_mean = []
	path = 'archives/cooling_schedule_{0}.npy'.format(int(time.time()))

	for idx, schedule in enumerate(cooling_schedules):
		print("=== Cooling schedule {0} ===".format(idx + 1))
		costs = convergence.simulations(nodes, 30, schedule, distance, True)
		xs = [range(len(c)) for c in costs]
		graphics.simple_scatter(xs, costs, 'Convergence to optimal solution', 'Steps', 'Minimal path distance')
		stats.statistical_analysis_convergence(costs)

		rates = np.array(convergence.Simulation_rates)  # rates length will be the same for each simulation in this case
		y_mean = np.mean(rates, axis=0)
		print(tabulate([[y_mean]], headers=["Sample mean - acceptance rate"]))
		ys_mean.append(np.mean(np.array(costs), axis=0))
		xs_mean.append(np.array(range(1, len(ys_mean[-1]) + 1)))

		with open(path, 'ab') as f:
			np.save(f, costs)

	labels = [r'$T_n = T_0 \times 0.975^n$', r'$T_n = T_0 \times 0.95^n$', r'$T_n = T_0 \times 0.9^n$', r'$T_n = T_0 \times 0.75^n$']
	graphics.simple_plotter(xs_mean, ys_mean, labels, 'Convergence to optimal solution', 'Steps', 'Minimal path distance')


def question_cooling_schedule_2():
	# Case a280
	nodes = utils.tsp_reader('./tsp_data/a280.tsp.txt')
	distance = geometry.distance_matrix(nodes)

	cooling_schedule_1 = annealing.CoolingSchedule(
		T=4*10**-3,
		steps=500,
		lowering_method=(lambda t, i: 4*10**-3 / np.log10(i + 2)),
		annealing_condition=(lambda i: i < 50),
	)

	cooling_schedules = [cooling_schedule_1]
	xs_mean = []
	ys_mean = []
	path = 'archives/logarithmic_cooling_schedule_{0}.npy'.format(int(time.time()))

	for idx, schedule in enumerate(cooling_schedules):

		print("=== Logarithmic cooling schedule {0} ===".format(idx + 1))
		costs = convergence.simulations(nodes, 30, schedule, distance, True)
		xs = [range(len(c)) for c in costs]
		graphics.simple_scatter(xs, costs, 'Convergence to optimal solution', 'Steps', 'Minimal path distance')
		stats.statistical_analysis_convergence(costs)

		rates = np.array(convergence.Simulation_rates)  # rates length will be the same for each simulation in this case
		y_mean = np.mean(rates, axis=0)
		print(tabulate([[y_mean]], headers=["Sample mean - acceptance rate"]))
		ys_mean.append(np.mean(np.array(costs), axis=0))
		xs_mean.append(np.array(range(1, len(ys_mean[-1]) + 1)))

		with open(path, 'ab') as f:
			np.save(f, costs)

	labels = [r'$T_n = \frac{T_0}{log(n + 1)}$']
	graphics.simple_plotter(xs_mean, ys_mean, labels, 'Convergence to optimal solution', 'Steps', 'Minimal path distance')


def question_cooling_schedule_3():
	# Case a280
	nodes = utils.tsp_reader('./tsp_data/a280.tsp.txt')
	distance = geometry.distance_matrix(nodes)

	cooling_schedule_1 = annealing.CoolingSchedule(
		T=8*10**-3,
		steps=400,
		lowering_method=(lambda t, _: .975 * t),
		annealing_condition=(lambda i: i < 250),
	)

	cooling_schedule_2 = annealing.CoolingSchedule(
		T=8*10**-3,
		steps=400,
		lowering_method=(lambda t, _: .95 * t),
		annealing_condition=(lambda i: i < 250),
	)

	cooling_schedule_3 = annealing.CoolingSchedule(
		T=8*10**-3,
		steps=400,
		lowering_method=(lambda t, _: .90 * t),
		annealing_condition=(lambda i: i < 250),
	)

	cooling_schedule_4 = annealing.CoolingSchedule(
		T=8*10**-3,
		steps=400,
		lowering_method=(lambda t, _: .75 * t),
		annealing_condition=(lambda i: i < 250),
	)

	log_cooling_schedule = annealing.CoolingSchedule(
		T=8*10**-3,
		steps=400,
		lowering_method=(lambda t, i: 8*10**-3 / np.log10(i + 2)),
		annealing_condition=(lambda i: i < 250),
	)

	cooling_schedules = [cooling_schedule_1, cooling_schedule_2, cooling_schedule_3, cooling_schedule_4, log_cooling_schedule]
	xs_mean, ys_mean = [], []
	path = 'archives/plateau_cooling_schedule_{0}.npy'.format(int(time.time()))

	for idx, schedule in enumerate(cooling_schedules):
		print("=== Cooling schedule {0} ===".format(idx + 1))
		costs = convergence.simulations(nodes, 30, schedule, distance, True)
		xs = [range(len(c)) for c in costs]
		graphics.simple_scatter(xs, costs, 'Convergence to optimal solution', 'Steps', 'Minimal path distance')
		stats.statistical_analysis_convergence(costs)

		rates = np.array(convergence.Simulation_rates)  # rates length will be the same for each simulation in this case
		y_mean = np.mean(rates, axis=0)
		print(tabulate([[y_mean]], headers=["Sample mean - acceptance rate"]))
		ys_mean.append(np.mean(np.array(costs), axis=0))
		xs_mean.append(np.array(range(1, len(ys_mean[-1]) + 1)))

		with open(path, 'ab') as f:
			np.save(f, costs)

	labels = [
		r'$T_n = T_0 \times 0.975^n$',
		r'$T_n = T_0 \times 0.95^n$',
		r'$T_n = T_0 \times 0.9^n$',
		r'$T_n = T_0 \times 0.75^n$',
		r'$T_n = \frac{T_0}{log(n + 1)}$'
	]
	graphics.simple_plotter(xs_mean, ys_mean, labels, 'Convergence to optimal solution', 'Steps', 'Minimal path distance')


def question_cooling_schedule_4():
	# Case a280
	nodes = utils.tsp_reader('./tsp_data/a280.tsp.txt')
	distance = geometry.distance_matrix(nodes)

	cooling_schedule_1 = annealing.CoolingSchedule(
		T=4*10**-3,
		steps=400,
		lowering_method=(lambda t, _: .4 * t),
		annealing_condition=(lambda i: i < 150),
	)

	cooling_schedule_2 = annealing.CoolingSchedule(
		T=4*10**-3,
		steps=400,
		lowering_method=(lambda t, _: .3 * t),
		annealing_condition=(lambda i: i < 150),
	)

	cooling_schedule_3 = annealing.CoolingSchedule(
		T=4*10**-3,
		steps=400,
		lowering_method=(lambda t, _: .2 * t),
		annealing_condition=(lambda i: i < 150),
	)

	cooling_schedule_4 = annealing.CoolingSchedule(
		T=4*10**-3,
		steps=400,
		lowering_method=(lambda t, _: .1 * t),
		annealing_condition=(lambda i: i < 150),
	)

	cooling_schedule_5 = annealing.CoolingSchedule(
		T=4*10**-3,
		steps=400,
		lowering_method=(lambda t, _: .05 * t),
		annealing_condition=(lambda i: i < 150),
	)

	cooling_schedules = [cooling_schedule_1, cooling_schedule_2, cooling_schedule_3, cooling_schedule_4, cooling_schedule_5]
	xs_mean, ys_mean = [], []
	path = 'archives/lower_bound_cooling_schedule_{0}.npy'.format(int(time.time()))

	for idx, schedule in enumerate(cooling_schedules):
		print("=== Cooling schedule {0} ===".format(idx + 1))
		costs = convergence.simulations(nodes, 30, schedule, distance, True)
		xs = [range(len(c)) for c in costs]
		graphics.simple_scatter(xs, costs, 'Convergence to optimal solution', 'Steps', 'Minimal path distance')
		stats.statistical_analysis_convergence(costs)

		rates = np.array(convergence.Simulation_rates)  # rates length will be the same for each simulation in this case
		y_mean = np.mean(rates, axis=0)
		print(tabulate([[y_mean]], headers=["Sample mean - acceptance rate"]))
		ys_mean.append(np.mean(np.array(costs), axis=0))
		xs_mean.append(np.array(range(1, len(ys_mean[-1]) + 1)))

		with open(path, 'ab') as f:
			np.save(f, costs)

	labels = [
		r'$T_n = T_0 \times 0.4^n$',
		r'$T_n = T_0 \times 0.3^n$',
		r'$T_n = T_0 \times 0.2^n$',
		r'$T_n = T_0 \times 0.1^n$',
		r'$T_n = T_0 \times 0.05^n$',
	]
	graphics.simple_plotter(xs_mean, ys_mean, labels, 'Convergence to optimal solution', 'Steps', 'Minimal path distance')


def question_local_minimum():
	nodes = [utils.tsp_reader('./tsp_data/eil51.tsp.txt'),
			 utils.tsp_reader('./tsp_data/a280.tsp.txt'),
			 utils.tsp_reader('./tsp_data/pcb442.tsp.txt')]

	sols = [utils.tsp_solution_reader('./tsp_data/eil51.opt.tour.txt'),
			utils.tsp_solution_reader('./tsp_data/a280.opt.tour.txt'),
			utils.tsp_solution_reader('./tsp_data/pcb442.opt.tour.txt')]

	dist = [geometry.distance_matrix(nodes[0]),
			geometry.distance_matrix(nodes[1]),
			geometry.distance_matrix(nodes[2])]

	# reduced steps and chain length so that the simulation finishes before christmas
	cooling_schedule_reduced = annealing.CoolingSchedule(
		T=30,
		steps=1000,
		lowering_method=(lambda t: .9 * t),
		annealing_condition=(lambda i: i < 1000),
	)

	print("=== Statistics table - eil51 ===")
	path = 'archives/local_optim_stats_eil51_{0}.npy'.format(int(time.time()))
	costs = convergence.simulations(nodes[0], 5, cooling_schedule_reduced, dist[0])
	convergence.distance_solutions(nodes[0], costs, sols[0])
	dist_sols = [c[-1] for c in costs]
	with open(path, 'ab') as f:
		np.save(f, dist_sols)
	stats.summary_stats(dist_sols)

	print("=== Statistics table - a280 ===")
	path = 'archives/local_optim_stats_a280_{0}.npy'.format(int(time.time()))
	costs = convergence.simulations(nodes[1], 5, cooling_schedule_reduced, dist[1])
	convergence.distance_solutions(nodes[1], costs, sols[1])
	dist_sols = [c[-1] for c in costs]
	with open(path, 'ab') as f:
		np.save(f, dist_sols)
	stats.summary_stats(dist_sols)

	print("=== Statistics table - pcb442 ===")
	path = 'archives/local_optim_stats_pcb442_{0}.npy'.format(int(time.time()))
	costs = convergence.simulations(nodes[2], 5, cooling_schedule_reduced, dist[2])
	convergence.distance_solutions(nodes[2], costs, sols[2])
	dist_sols = [c[-1] for c in costs]
	with open(path, 'ab') as f:
		np.save(f, dist_sols)
	stats.summary_stats(dist_sols)


def optimum_path_diagrams():

	# reduced steps and chain length so that the simulation finishes before christmas
	cooling_schedule = annealing.CoolingSchedule(
		T=30,
		steps=750,
		lowering_method=(lambda t: .9 * t),
		annealing_condition=(lambda i: i < 750),
	)

	nodes = [utils.tsp_reader('./tsp_data/eil51.tsp.txt'),
			 utils.tsp_reader('./tsp_data/a280.tsp.txt'),
			 utils.tsp_reader('./tsp_data/pcb442.tsp.txt')]

	dist = [geometry.distance_matrix(nodes[0]),
			geometry.distance_matrix(nodes[1]),
			geometry.distance_matrix(nodes[2])]

	traveling_list = utils.initial_perm(nodes[0])
	optimized_traveling_list = annealing.simulated_annealing(traveling_list, nodes[0], cooling_schedule, dist[0])
	path = 'archives/optim_order_eil51.npy'
	with open(path, 'ab') as f:
		np.save(f, optimized_traveling_list[0])
	graphics.node_graph(nodes[0], optimized_traveling_list[0], 'Optimised Path - 51 City Problem')

	traveling_list = utils.initial_perm(nodes[1])
	optimized_traveling_list = annealing.simulated_annealing(traveling_list, nodes[1], cooling_schedule, dist[1])
	path = 'archives/optim_order_a280.npy'
	with open(path, 'ab') as f:
		np.save(f, optimized_traveling_list[0])
	graphics.node_graph(nodes[1], optimized_traveling_list[0], 'Optimised Path - 280 City Problem')

	traveling_list = utils.initial_perm(nodes[2])
	optimized_traveling_list = annealing.simulated_annealing(traveling_list, nodes[2], cooling_schedule, dist[2])
	path = 'archives/optim_order_pcb442.npy'
	with open(path, 'ab') as f:
		np.save(f, optimized_traveling_list[0])
	graphics.node_graph(nodes[2], optimized_traveling_list[0], 'Optimised Path - 442 City Problem')


def chain_length_diagrams():
	# set up for the a280 problem
	nodes = utils.tsp_reader('./tsp_data/a280.tsp.txt')
	solution = utils.tsp_solution_reader('./tsp_data/a280.opt.tour.txt')
	dist = geometry.distance_matrix(nodes)
	print("=== Convergence by Chain Length -- 0-400 ===")	# nodes = utils.tsp_reader('./tsp_data/a280.tsp.txt')	
	# chain values to try
	chains = [50, 250, 500, 1000]
	# minimum path length values at each step setting
	minimums = []
	x_vals = []
	for c in chains:
		settings = annealing.CoolingSchedule(
			T=80,
			steps=400,
			lowering_method=(lambda t: .9 * t),
			annealing_condition=(lambda i: i < c),
		)
		costs = convergence.simulations(nodes, 1, settings, dist)
		x_vals.append(np.linspace(0, 400, c * 400))
		minimums.append(costs[0])
		path = 'archives/chain_length_{0}.npy'.format(c)
		with open(path, 'ab') as f:
			np.save(f, costs[0])

	graphics.chain_length_plot(x_vals, minimums, chains, 'Effect of Chain Length on Convergence', 'Minimum Path Distance', 'Steps')

	print("=== Convergence by Chain Length -- 200-400 ===")	
	# chain values to try
	chains = [50, 250, 500, 1000]
	# minimum path length values at each step setting
	minimums = []
	x_vals = []
	for c in chains:
		settings = annealing.CoolingSchedule(
			T=80,
			steps=400,
			lowering_method=(lambda t: .9 * t),
			annealing_condition=(lambda i: i < c),
		)
		costs = convergence.simulations(nodes, 1, settings, dist) 
		total_points = c * 400
		x = np.linspace(0, 400, total_points)
		# only take the final quarter 
		cut = int(total_points / 2)
		x_vals.append(x[-cut:])
		minimums.append(costs[0][-cut:])
	
	graphics.chain_length_plot(x_vals, minimums, chains, 'Effect of Chain Length on Convergence', 'Minimum Path Distance', 'Steps')


def heat_maps():
	nodes = [utils.tsp_reader('./tsp_data/eil51.tsp.txt'),
		 utils.tsp_reader('./tsp_data/a280.tsp.txt')]

	sols = [utils.tsp_solution_reader('./tsp_data/eil51.opt.tour.txt'),
			utils.tsp_solution_reader('./tsp_data/a280.opt.tour.txt')]

	dist = [geometry.distance_matrix(nodes[0]),
			geometry.distance_matrix(nodes[1])]

	print("=== Convergence by Chain Length Heat Map -  eil51 ===")	
	# chain values to try
	chains = [10, 25, 50, 100, 250, 500, 750][::-1]
	# max steps to try
	steps = [10, 25, 50, 100, 250, 500, 750]
	# minimum path length values at each step setting
	res = np.zeros((len(chains), len(steps)))
	for c in range(0, len(chains)):
		for s in range(0, len(steps)):
			settings = annealing.CoolingSchedule(
				T=80,
				steps=steps[s],
				lowering_method=(lambda t: .9 * t),
				annealing_condition=(lambda i: i < chains[c]),
			)
			costs = convergence.simulations(nodes[0], 1, settings, dist[0])
			res[c,s] = [c[-1] for c in costs][0]
	path = 'archives/heat_map_eil51_{0}.npy'.format(int(time.time()))
	with open(path, 'ab') as f:
		np.save(f, res)
	graphics.heat_map(res, steps, chains, 'Effect of Chain Length and Maximum Steps', 'Chain Length', 'Steps')

	print("=== Convergence by Chain Length Heat Map -  a280 ===")	
	# chain values to try
	chains = [10, 25, 50, 100, 250, 500, 750][::-1]
	# max steps to try
	steps = [10, 25, 50, 100, 250, 500, 750]
	# minimum path length values at each step setting
	res = np.zeros((len(chains), len(steps)))
	for c in range(0, len(chains)):
		for s in range(0, len(steps)):
			settings = annealing.CoolingSchedule(
				T=80,
				steps=steps[s],
				lowering_method=(lambda t: .9 * t),
				annealing_condition=(lambda i: i < chains[c]),
			)
			costs = convergence.simulations(nodes[1], 1, settings, dist[1])
			res[c,s] = [c[-1] for c in costs][0]
	path = 'archives/heat_map_a280_{0}.npy'.format(int(time.time()))
	with open(path, 'ab') as f:
		np.save(f, res)
	graphics.heat_map(res, steps, chains, 'Effect of Chain Length and Maximum Steps', 'Chain Length', 'Steps')


def chain_length_table():
	nodes = utils.tsp_reader('./tsp_data/a280.tsp.txt')
	sols = utils.tsp_solution_reader('./tsp_data/a280.opt.tour.txt')
	dist = geometry.distance_matrix(nodes)

	print("=== Varying Chain Length Table / Hypo Test - A280 ===")	
	chains = [250, 500, 1000]
	repeats = 25
	res = []
	for c in range(0, len(chains)):
		settings = annealing.CoolingSchedule(
			T=70,
			steps=400,
			lowering_method=(lambda t: .75 * t),
			annealing_condition=(lambda i: i < chains[c]),
		)
		costs = convergence.simulations(nodes, repeats, settings, dist)
		res.append([c[-1] for c in costs])

	path = 'archives/chain_length_conv_table_{0}.npy'.format(int(time.time()))
	with open(path, 'ab') as f:
		np.save(f, res)
	
	for r in range(0, len(res)):
		print("=== Chain Length = {0} ===".format(chains[r]))	
		stats.summary_stats(res[r])


def generate_total_cost_intro():
	nodes = utils.tsp_reader('./tsp_data/eil51.tsp.txt')
	nodes = np.array([nodes[0][:6], nodes[1][:6]])
	dist = geometry.distance_matrix(nodes)
	traveling_list = utils.initial_perm(nodes)
	perms = list(itertools.permutations(traveling_list))
	total_cost = []
	for order in perms:
		total_cost.append(geometry.total_distance_precalc(nodes, order, dist))
	graphics.total_cost_intro(total_cost)


if __name__ == '__main__':
	print("=== Assignment 3 - Traveling Salesman Problem")
	print("Given that the algorithms used to obtains results in this assignment are taking a long time,")
	print("we give you the choice to read pre-saved results or to run real-time algorithm.")
	choice = input("=== Do you want to load pre-saved results (Y/N) ? ")

	if choice.upper() == "Y":
		generate_total_cost_intro()
		# Archived data
		archives.load_global_minimum_archive()
		archives.global_minimum_diagrams()

		archives.load_initial_temperature_t0_archive()
		question_initial_temperature_2()
		archives.load_cooling_schedule_archive()
		archives.load_cooling_schedule_archive_2()
		archives.load_cooling_schedule_archive_3()

		archives.load_chain_length_archive()
		archives.load_chain_length_heatmaps()
		archives.chain_length_conv_table()
	else:
		# Real-time
		generate_total_cost_intro()
		question_initial_temperature()
		question_cooling_schedule()
		question_cooling_schedule_2()
		question_cooling_schedule_3()
		question_cooling_schedule_4()
		question_local_minimum()
		optimum_path_diagrams()
		chain_length_diagrams()
		heat_maps()
		chain_length_table()





