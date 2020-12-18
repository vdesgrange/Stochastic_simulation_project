import math
import graphic_tools
import numpy as np


class TravelingMap(object):
    def __init__(self, name, comment, type, dimension, edge_weight_type):
        self.name = name
        self.comment = comment
        self.type = type
        self.dimension = int(dimension)
        self.edge_weight_type = edge_weight_type
        self.city_list = list()
        self.traveling_map = list()
        self.distance_map = np.zeros((self.dimension, self.dimension))

    def insert_city_coordinates(self, city, x, y):
        self.city_list.insert(city - 1, (x, y))

    def get_city_coordinates(self, city):
        return self.city_list[city - 1]  # List starts at index 0 while city name starts at index 1

    def generate_distance_map(self):
        for node_1 in range(self.dimension):
            for node_2 in range(self.dimension):
                from_coord, to_coord = self.city_list[node_1], self.city_list[node_2]
                distance = math.sqrt((to_coord[0] - from_coord[0])**2 + (to_coord[1] - from_coord[1])**2)
                self.distance_map[node_1][node_2] = distance

    def insert_city(self, to_city):
        self.traveling_map.append(to_city)

    def remove_city(self, city):
        self.traveling_map.remove(city)

    def insert_edge(self, from_city, edge):
        from_idx = self.traveling_map.index(from_city)
        self.traveling_map = self.traveling_map[:from_idx] + edge + self.traveling_map[from_idx:]

    def remove_edge(self, from_city, to_city):
        from_idx, to_idx = self.traveling_map.index(from_city), self.traveling_map.index(to_city)
        edge = self.traveling_map[from_idx:to_idx]
        del self.traveling_map[from_idx:to_idx]
        return edge

    def get_length(self):
        distance = 0
        a = self.traveling_map[0]
        for b in self.traveling_map[1:]:
            distance += self.distance_map[a - 1][b - 1]
            a = b

        distance += self.distance_map[a - 1][self.traveling_map[0] - 1]
        return distance

    def get_next(self, city):
        idx = self.traveling_map.index(city)
        if idx + 1 == len(self.traveling_map):
            return self.traveling_map[0]
        else:
            return self.traveling_map[idx + 1]

    def get_prev(self, city):
        idx = self.traveling_map.index(city)
        return self.traveling_map[idx - 1]

    def get_map(self):
        map = []
        for city in self.traveling_map:
            map.append([self.get_city_coordinates(city), self.get_city_coordinates(self.get_next(city))])
        return map

    def random_initialization(self):
        list_available_city = list(range(1, self.dimension + 1, 1))

        while len(list_available_city) > 0:
            idx = np.random.randint(0, len(list_available_city))
            city = list_available_city[idx]
            self.insert_city(city)
            list_available_city.remove(city)

    def print(self):
        for city in self.traveling_map:
            next_city = self.get_next(city)
            distance = self.distance_map[city][next_city]
            print('City {:d} -- {:f} --> City {:d}'.format(city, distance, next_city))


    # def insert_edge(self, from_city, to_city):
    #     from_coord, to_coord = self.city_list[from_city - 1], self.city_list[to_city - 1]
    #     distance = math.sqrt((to_coord[0] - from_coord[0])**2 + (to_coord[1] - from_coord[1])**2)
    #     self.traveling_map[from_city] = (to_city, distance)

    # def get_length(self):
    #     length = 0
    #     for (_, d) in self.traveling_map.values():
    #         length += d
    #
    #     return length


def tsp_reader(file_path):
    with open(file_path, 'r') as f:
        name = f.readline().strip().split(':')[1]  # NAME
        comment = f.readline().strip().split(':')[1]  # COMMENT
        type = f.readline().strip().split(':')[1]  # TYPE
        dimension = f.readline().strip().split(':')[1]  # DIMENSION
        edge_weight_type = f.readline().strip().split(':')[1]  # EDGE WEIGHT TYPE
        f.readline()
        traveling_map = TravelingMap(name, comment, type, dimension, edge_weight_type)

        n = int(dimension)
        for i in range(0, n):
            x, y = f.readline().split()[1:]
            traveling_map.insert_city_coordinates(i + 1, float(x), float(y))
            # traveling_map.insert_edge(i, i + 1)

        # traveling_map.insert_edge(n, 1)

    return traveling_map


if __name__ == '__main__':
    traveling_map = tsp_reader('../documents/TSP-Configurations/a280.tsp.txt')
    traveling_map.generate_distance_map()
    traveling_map.random_initialization()
    graphic_tools.traveling_map_plotter(traveling_map)
    print(traveling_map.get_length())
