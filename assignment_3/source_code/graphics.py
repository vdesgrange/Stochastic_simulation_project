import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns 

def node_graph(nodes, path=None, title="Traveling Salesman Map"):
	x = nodes[0, :]
	y = nodes[1, :]

	fig, ax = plt.subplots(dpi=150)
	ax.set_title(title, fontsize=13)
	ax.scatter(x, y, s = 1)
	if path:
		for i in range(0, len(path) - 1):
			ax.plot([x[path[i]], x[path[i+1]]], [y[path[i]], y[path[i+1]]], linewidth=1)
		ax.plot([x[path[-1]], x[path[0]]], [y[path[-1]], y[path[0]]], linewidth=1)
	plt.ylabel('Y Coordinate', fontsize=13)
	plt.xlabel('X Coordinate', fontsize=13)
	plt.tick_params(labelsize=13)
	plt.show()


def simple_scatter(xs, ys, title, x_axis, y_axis):
	fig, ax = plt.subplots(dpi=150)
	nb_simulation = len(xs)

	for i in range(nb_simulation):
		ax.scatter(xs[i], ys[i], s=0.5)

	plt.ylabel(y_axis, fontsize=13)
	plt.xlabel(x_axis, fontsize=13)
	plt.title(title, fontsize=13)
	plt.tick_params(labelsize=13)
	plt.show()

def heat_map(data, xtick, ytick, title, ylabel, xlabel):
	sns.set_theme()
	plt.Figure()
	ax = sns.heatmap(data, xticklabels=xtick, yticklabels=ytick)
	plt.title(title, fontsize=13)
	plt.ylabel(ylabel, fontsize=13)
	plt.xlabel(xlabel, fontsize=13)
	plt.tick_params(labelsize=13)
	plt.show()

def chain_length_plot(x, data, leg_labels, title, ylabel, xlabel):
	sns.set_theme()
	plt.Figure()

	for i in range(0, len(data)):
		plt.plot(x[i], data[i], label='Chain length = {}'.format(leg_labels[i]))
	
	plt.title(title, fontsize=13)
	plt.ylabel(ylabel, fontsize=13)
	plt.xlabel(xlabel, fontsize=13)
	plt.tick_params(labelsize=13)
	plt.legend(fontsize=13)
	plt.show()

def simple_plotter(xs, ys, labels, title, x_axis, y_axis):
	sns.set_theme()
	fig, ax = plt.subplots(dpi=150)
	nb_simulation = len(xs)

	for i in range(nb_simulation):
		ax.plot(xs[i], ys[i], linewidth=1, label=labels[i])

	plt.ylabel(y_axis, fontsize=13)
	plt.xlabel(x_axis, fontsize=13)
	plt.title(title, fontsize=13)
	plt.tick_params(labelsize=13)
	plt.legend()
	plt.grid(True)
	plt.show()


def box_plot(data, labels, title, ylabel):
	fig, ax = plt.subplots(dpi=150)
	red_square = dict(markerfacecolor='r', marker='s')
	ax.set_title(title, fontsize=13)
	ax.boxplot(data, flierprops=red_square, notch = True, labels = labels)
	plt.tick_params(labelsize=13)
	plt.ylabel(ylabel, fontsize=13)
	plt.show()

def total_cost_intro(costs):
	sns.set_theme()
	fig, ax = plt.subplots(dpi=150)
	plt.plot(list(range(0, len(costs))), costs)
	plt.ylabel('Costs', fontsize=13)
	plt.xlabel('Tour Number', fontsize=13)
	plt.title('Tour Permutations and Costs', fontsize=13)
	plt.tick_params(labelsize=13)
	plt.show()


