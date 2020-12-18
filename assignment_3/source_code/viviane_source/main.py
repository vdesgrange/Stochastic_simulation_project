import numpy as np
from copy import deepcopy
from utils import TravelingMap, tsp_reader
import graphic_tools


def simulated_annealing(map):
    T = 80
    steps = 10 * T

    for i in range(0, steps):
        markov_chain_length = 30
        j = 0
        while j < markov_chain_length:
            j += 1
            current_cost = map.get_length()
            new_map = deepcopy(map)
            idx1, idx2 = np.sort(np.random.randint(0, len(new_map.traveling_map), 2))

            bin = np.random.choice([0, 1])
            if bin == 0:  # Reverse
                new_map.traveling_map[idx1:idx2] = reversed(new_map.traveling_map[idx1:idx2])

            else:  # Transport
                city1, city2 = new_map.traveling_map[idx1], new_map.traveling_map[idx2]
                edge = new_map.remove_edge(city1, city2)
                new_idx = np.random.randint(0, len(new_map.traveling_map))
                new_city = new_map.traveling_map[new_idx]

                new_map.insert_edge(new_city, edge)

            new_cost = new_map.get_length()
            diff_cost = new_cost - current_cost

            if diff_cost < 0:
                map = deepcopy(new_map)
            else:
                v = np.exp(- diff_cost / T)
                u = np.random.uniform(low=0.0, high=1.0)
                if v > u:
                    map = deepcopy(new_map)
        T *= 0.9

    return map


if __name__ == '__main__':
    traveling_map = tsp_reader('../../documents/TSP-Configurations/a280.tsp.txt')
    traveling_map.generate_distance_map()
    traveling_map.random_initialization()
    graphic_tools.traveling_map_plotter(traveling_map)
    print("Cost initial map : ", traveling_map.get_length())
    new_map = simulated_annealing(traveling_map)
    graphic_tools.traveling_map_plotter(new_map)
    print("Cost optimized map : ", new_map.get_length())
