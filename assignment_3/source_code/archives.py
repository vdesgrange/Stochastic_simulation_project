import numpy as np
import stats
import graphics
import utils


def load_initial_temperature_t0_archive():
    file_paths = [
        './archives/initial_temperature_t0_1608250365.npy',
        './archives/initial_temperature_t0_1608250438.npy',
        './archives/initial_temperature_t0_1608250548.npy']

    for path in file_paths:
        with open(path, 'rb') as f:
            x_means = np.load(f)
            y_means = np.load(f)
            labels = np.load(f)
            x_diff_means = np.load(f)
            y_diff_means = np.load(f)
            diff_labels = np.load(f)

        graphics.simple_plotter(x_means, y_means, labels, 'Evolution of mean acceptance rate', 'Steps', 'Mean acceptance rate')
        graphics.simple_plotter(x_diff_means, y_diff_means, diff_labels, 'Evolution of mean cost difference', 'Steps', 'Mean cost difference')


def load_cooling_schedule_archive():
    exp_costs, log_costs = [], []
    xs_mean, ys_mean = [], []

    with open('./archives/cooling_schedule_1607790992.npy', 'rb') as f:
        for i in range(4):
            exp_costs.append(np.load(f))

    with open('./archives/logarithmic_cooling_schedule_1607964535.npy', 'rb') as f:
        log_costs.append(np.load(f))

    log_costs = [list(np.array(log_costs)[0, :, 0:400])]  # Adjust size of array with exponential costs
    total_costs = exp_costs + log_costs

    for idx, cost in enumerate(total_costs):
        xs = [range(len(c)) for c in cost]
        graphics.simple_scatter(xs, cost, 'Convergence to optimal solution', 'Steps', 'Minimal path distance')
        stats.statistical_analysis_convergence(cost)

        ys_mean.append(np.mean(np.array(cost), axis=0))
        xs_mean.append(np.array(range(1, len(ys_mean[-1]) + 1)))

    labels = [
        r'$T_n = T_0 \times 0.975^n$',
        r'$T_n = T_0 \times 0.95^n$',
        r'$T_n = T_0 \times 0.9^n$',
        r'$T_n = T_0 \times 0.75^n$',
        r'$T_n = \frac{T_0}{log(1 + n)}$']  # In our code index start at 0 so log(k + 2) instead of theory log(k + 1).
    graphics.simple_plotter(xs_mean, ys_mean, labels, 'Convergence to optimal solution', 'Steps', 'Minimal path distance')


def load_cooling_schedule_archive_2():
    total_costs = []
    xs_mean, ys_mean = [], []

    with open('./archives/plateau_cooling_schedule_1608202283.npy', 'rb') as f:
        for i in range(5):
            total_costs.append(np.load(f))

    for idx, cost in enumerate(total_costs):
        xs = [range(len(c)) for c in cost]
        graphics.simple_scatter(xs, cost, 'Convergence to optimal solution', 'Steps', 'Minimal path distance')
        stats.statistical_analysis_convergence(cost)

        ys_mean.append(np.mean(np.array(cost), axis=0))
        xs_mean.append(np.array(range(1, len(ys_mean[-1]) + 1)))

    labels = [
        r'$T_n = T_0 \times 0.975^n$',
        r'$T_n = T_0 \times 0.95^n$',
        r'$T_n = T_0 \times 0.9^n$',
        r'$T_n = T_0 \times 0.75^n$',
        r'$T_n = \frac{T_0}{log(1 + n)}$']  # In our code index start at 0 so log(k + 2) instead of theory log(k + 1).
    graphics.simple_plotter(xs_mean, ys_mean, labels, 'Convergence to optimal solution', 'Steps', 'Minimal path distance')


def load_cooling_schedule_archive_3():
    total_costs = []
    xs_mean, ys_mean = [], []

    with open('./archives/cooling_schedule_1607790992.npy', 'rb') as f:
        for i in range(4):
            total_costs.append(np.load(f))

    with open('./archives/lower_bound_cooling_schedule_1608313212.npy', 'rb') as f:
        for i in range(2):
            total_costs.append(np.load(f))

    with open('./archives/lower_bound_cooling_schedule_1608311396.npy', 'rb') as f:
        for i in range(3):
            total_costs.append(np.load(f))

    for idx, cost in enumerate(total_costs):
        stats.statistical_analysis_convergence(cost)
        ys_mean.append(np.mean(np.array(cost), axis=0))
        xs_mean.append(np.array(range(1, len(ys_mean[-1]) + 1)))

    labels = [
        r'$T_n = T_0 \times 0.975^n$',
        r'$T_n = T_0 \times 0.95^n$',
        r'$T_n = T_0 \times 0.9^n$',
        r'$T_n = T_0 \times 0.75^n$',
        r'$T_n = T_0 \times 0.40^n$',
        r'$T_n = T_0 \times 0.30^n$',
        r'$T_n = T_0 \times 0.20^n$',
        r'$T_n = T_0 \times 0.10^n$',
        r'$T_n = T_0 \times 0.05^n$']
    graphics.simple_plotter(xs_mean, ys_mean, labels, 'Convergence to optimal solution', 'Steps', 'Minimal path distance')


def load_global_minimum_archive():
    total_costs = [[], [], []]

    with open('./archives/local_optim_stats_eil51_1608306723.npy', 'rb') as f:
        total_costs[0].append(np.load(f))

    with open('./archives/local_optim_stats_a280_1608307188.npy', 'rb') as f:
        total_costs[1].append(np.load(f))

    with open('./archives/local_optim_stats_pcb442_1608308470.npy', 'rb') as f:
        total_costs[2].append(np.load(f))

    print("=== Summary Statistics - eil51 ===")
    stats.summary_stats(total_costs[0][0])
    print("=== Summary Statistics - a280 ===")
    stats.summary_stats(total_costs[1][0])
    print("===  Summary Statistics - pcb442 ===")
    stats.summary_stats(total_costs[2][0])

def global_minimum_diagrams():

    nodes = [utils.tsp_reader('./tsp_data/eil51.tsp.txt'),
             utils.tsp_reader('./tsp_data/a280.tsp.txt'),
             utils.tsp_reader('./tsp_data/pcb442.tsp.txt')]

    orders = []

    with open('./archives/optim_order_eil51.npy', 'rb') as f:
        orders.append(np.load(f))

    with open('./archives/optim_order_a280.npy', 'rb') as f:
        orders.append(np.load(f))

    with open('./archives/optim_order_pcb442.npy', 'rb') as f:
        orders.append(np.load(f))

    graphics.node_graph(nodes[0], orders[0].tolist(), 'Optimised Path - 51 City Problem')
    graphics.node_graph(nodes[1], orders[1].tolist(), 'Optimised Path - 280 City Problem')
    graphics.node_graph(nodes[2], orders[2].tolist(), 'Optimised Path - 442 City Problem')

def load_chain_length_archive():
    chains = [50, 250, 500, 1000]
    costs = []
    x_vals = []

    for i in range(0, len(chains)):
        x_vals.append(np.linspace(0, 400, chains[i] * 400))
        with open('./archives/chain_length_{0}.npy'.format(chains[i]), 'rb') as f:
            costs.append(np.load(f))

    graphics.chain_length_plot(x_vals, costs, chains, 'Effect of Chain Length on Convergence', 'Minimum Path Distance', 'Steps')

    trunc_x_vals = []
    trunc_cost = []
    for c in range(0, len(chains)):
        total_points = chains[c] * 400
        cut = int(total_points / 2)
        trunc_x_vals.append(x_vals[c][-cut:])
        trunc_cost.append(costs[c][-cut:])
    graphics.chain_length_plot(trunc_x_vals, trunc_cost, chains, 'Effect of Chain Length on Convergence', 'Minimum Path Distance', 'Steps')

def load_chain_length_heatmaps():
    # chain values to try
    chains = [10, 25, 50, 100, 250, 500, 750][::-1]
    # max steps to try
    steps = [10, 25, 50, 100, 250, 500, 750]

    res = [[], []]
    with open('./archives/heat_map_eil51_1608295487.npy', 'rb') as f:
        res[0] = np.load(f)
    graphics.heat_map(res[0], steps, chains, 'Effect of Chain Length and Maximum Steps - eil51', 'Chain Length', 'Steps')
    
    with open('./archives/heat_map_a280_1608297281.npy', 'rb') as f:
        res[1] = np.load(f)
    graphics.heat_map(res[1], steps, chains, 'Effect of Chain Length and Maximum Steps - a280', 'Chain Length', 'Steps')

def chain_length_conv_table():
    chains = [250, 500, 1000]
    with open('./archives/chain_length_conv_table_1608300033.npy', 'rb') as f:
        res = np.load(f)

    for r in range(0, len(res)):
        print("=== Chain Length = {0} ===".format(chains[r]))   
        stats.summary_stats(res[r])

if __name__ == '__main__':
    load_cooling_schedule_archive()
    load_cooling_schedule_archive_2()
    chain_length_heatmaps()
    chain_length_conv_table()