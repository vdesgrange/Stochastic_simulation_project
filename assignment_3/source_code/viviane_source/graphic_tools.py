import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


def traveling_map_plotter(map):
    fig, ax = plt.subplots(dpi=150)
    x = [t[0] for t in map.city_list]
    y = [t[1] for t in map.city_list]

    edges = LineCollection(map.get_map(), linewidths=1)

    ax.scatter(x, y, s=0.5, c='g')
    ax.add_collection(edges)
    ax.set_title("Travelling salesman map")

    plt.show()