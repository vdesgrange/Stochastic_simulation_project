import numpy as np
import utils
import graphics
import annealing
import geometry

Simulation_rates = []
Simulation_differences = []


def simulations(nodes, n, cooling_schedule, distance_matrix=np.array([]), relative=False):

    simulation_costs = []
    global Simulation_rates, Simulation_differences
    Simulation_rates = []
    Simulation_differences = []

    simulated_annealing_func = annealing.simulated_annealing
    if relative == True:
        simulated_annealing_func = annealing.simulated_annealing_relative

    for i in range(n):
        traveling_list = utils.initial_perm(nodes)
        optimized_list, costs = simulated_annealing_func(traveling_list, nodes, cooling_schedule, distance_matrix)
        simulation_costs.append(costs)
        Simulation_rates.append(annealing.Rates.copy())
        Simulation_differences.append(annealing.Cost_difference.copy())

    return simulation_costs


def distance_solutions(nodes, costs, solution):
    global_solution_cost = geometry.total_distance(nodes, solution)
    xs, ys = [], []
    for c in costs:  # Number of loop can differ between each simulations
        xs.append(range(len(c)))
        ys.append(np.array(c) - global_solution_cost)

    graphics.simple_scatter(xs, ys, 'Convergence to optimal solution', 'Number of operations', 'Cost difference with optimal solution')


if __name__ == '__main__':

    # Case eil51
    nodes = utils.tsp_reader('./tsp_data/eil51.tsp.txt')
    traveling_list = utils.initial_perm(nodes)
    solution = utils.tsp_solution_reader('./tsp_data/eil51.opt.tour.txt')
    cooling_schedule = annealing.CoolingSchedule(
        T=80,
        steps=100,
        lowering_method=(lambda t: .9 * t),
        annealing_condition=(lambda i: i < 25),
    )

    costs = simulations(nodes, 10, cooling_schedule)
    distance_solutions(nodes, costs, solution)
