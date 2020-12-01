import random
import statistics
import numpy as np
import scipy.stats as stats

from fifo_servers import ServerFIFO
from priority_servers import ServerPriority
import graphic_tools
import distributions

def question_2_1():
    print('===========\n')
    print('Write a DES program to verify this for n=1, n=2 and n=4. Make sure that your result has a high and known statistical significance. \n')
    print('===========\n')

    SIMS = 50
    LAMB_DA = 0.9
    NB_JOBS = 10000

    stop_cond = (lambda idx: idx <= NB_JOBS)

    # waiting_times[0] is the
    waiting_times = [[], [], []]

    print("Simulation starting...")

    for j in range(0, SIMS):
        random.seed(random.random())
        server_fifo_1 = ServerFIFO(1, 1, 1 * LAMB_DA, random.expovariate, random.expovariate, stop_cond)
        server_fifo_1.env.run()

        random.seed(random.random())
        server_fifo_2 = ServerFIFO(1, 2, 2 * LAMB_DA, random.expovariate, random.expovariate, stop_cond)
        server_fifo_2.env.run()

        random.seed(random.random())
        server_fifo_3 = ServerFIFO(1, 4, 4 * LAMB_DA, random.expovariate, random.expovariate, stop_cond)
        server_fifo_3.env.run()

        waiting_times[0].append(statistics.mean(server_fifo_1.waiting_times))
        waiting_times[1].append(statistics.mean(server_fifo_2.waiting_times))
        waiting_times[2].append(statistics.mean(server_fifo_3.waiting_times))

    print("Simulation done.")

    single_slot_wait_time = np.array(waiting_times[0])
    double_slot_wait_time = np.array(waiting_times[1])
    quad_slot_wait_time = np.array(waiting_times[2])

    print('Average wait time, Single slot', single_slot_wait_time.mean())
    print('Average wait time, Double slot', double_slot_wait_time.mean())
    print('Average wait time, Quad slot', quad_slot_wait_time.mean())

    print('Sample Variance, Single slot', np.var(single_slot_wait_time))
    print('Sample Variance, Double slot', np.var(double_slot_wait_time))
    print('Sample Variance, Quad slot', np.var(quad_slot_wait_time))

    # 2 sided, 1 sample t tests
    print('Single slot T test', stats.ttest_1samp(single_slot_wait_time, 9.0))
    # 4.36 is the expected wait time with c = 2
    print('Double slot T test', stats.ttest_1samp(double_slot_wait_time, 4.26))
    # 1.96 is the expected wait time with c = 4
    print('Quad slot T test', stats.ttest_1samp(quad_slot_wait_time, 1.96))


def question_2_2():
    print('===========\n')
    print('How does the sample variance of our E(W) depend on ρ? \n')
    print('How does the sample variance of our E(W) depend on the number of customers per simulation? \n')
    print('===========\n')

    lambdas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    def repeat_until_significant(nb_jobs):
        # simulations required for significance for each value of RHO
        samp_var = np.zeros(len(lambdas))

        print("Simulation starting...")
        for i in range(len(lambdas)):
            nb_simulations = 30
            count = 0
            mean_waiting_times = []

            while count < nb_simulations:
                random.seed(random.random())
                server_fifo = ServerFIFO(1, 1, lambdas[i], random.expovariate, random.expovariate, lambda idx: idx <= nb_jobs)
                server_fifo.env.run()

                mean_waiting_times.append(statistics.mean(server_fifo.waiting_times))
                count += 1

            samp_var[i] = np.var(mean_waiting_times)

        print("Simulation done.")

        return samp_var

    xs = [lambdas, lambdas, lambdas]
    ys = [repeat_until_significant(1000), repeat_until_significant(5000), repeat_until_significant(10000)]
    labels = ['1,000 customers', '5,000 customers', '10,000 customers']
    graphic_tools.y_log_plotter(xs, ys, labels, r'$\rho$ Influence Over Sample Variance', r'$\rho$', r'$S^2$')


def question_2_3():
    print('===========\n')
    print('Mean Waiting Time pdf -- Multiple Customer Values \n')
    print('===========\n')

    # Test for a range of RHO values
    cus = [10, 100, 1000]
    RHO = 0.25
    xs, ys = [], []

    for i in range(len(cus)):
        random.seed(random.random())
        server_fifo = ServerFIFO(1, 1, RHO, random.expovariate, random.expovariate, lambda idx: idx <= cus[i])
        server_fifo.env.run()
        t_range = np.linspace(-20, 20, 200)
        kde = stats.gaussian_kde(server_fifo.waiting_times)
        xs.append(t_range)
        ys.append(kde(t_range))

    labels = ['10 Customers', '100 Customers', '1000 Customers']
    graphic_tools.kde_plotter(xs, ys, labels, r'PDF of E(W), $\rho = 0.25$')

        # Test for a range of RHO values
    cus = [10, 100, 1000]
    RHO = 0.75
    xs, ys = [], []

    for i in range(len(cus)):
        random.seed(random.random())
        server_fifo = ServerFIFO(1, 1, RHO, random.expovariate, random.expovariate, lambda idx: idx <= cus[i])
        server_fifo.env.run()
        t_range = np.linspace(-20, 20, 200)
        kde = stats.gaussian_kde(server_fifo.waiting_times)
        xs.append(t_range)
        ys.append(kde(t_range))

    labels = ['10 Customers', '100 Customers', '1000 Customers']
    graphic_tools.kde_plotter(xs, ys, labels, r'PDF of E(W), $\rho = 0.75$')




def question_3_1():
    print('===========\n')
    print('Write a DES program to verify this for n=1, n=2 and n=4. Make sure that your result has a high and known statistical significance. \n')
    print('===========\n')

    SIMS = 50
    RHO = 0.9
    NB_JOBS = 10000

    stop_cond = (lambda idx: idx <= NB_JOBS)

    # waiting_times[0] is the
    waiting_times = [[], [], []]

    print("Simulation starting...")

    for j in range(0, SIMS):
        random.seed(random.random())
        server_priority_1 = ServerPriority(1, 1, 1 * RHO, random.expovariate, random.expovariate, stop_cond)
        server_priority_1.env.run()

        random.seed(random.random())
        server_priority_2 = ServerPriority(1, 2, 2 * RHO, random.expovariate, random.expovariate, stop_cond)
        server_priority_2.env.run()

        random.seed(random.random())
        server_priority_3 = ServerPriority(1, 4, 4 * RHO, random.expovariate, random.expovariate, stop_cond)
        server_priority_3.env.run()

        waiting_times[0].append(statistics.mean(server_priority_1.waiting_times))
        waiting_times[1].append(statistics.mean(server_priority_2.waiting_times))
        waiting_times[2].append(statistics.mean(server_priority_3.waiting_times))

    print("Simulation done.")

    single_slot_wait_time = np.array(waiting_times[0])
    double_slot_wait_time = np.array(waiting_times[1])
    quad_slot_wait_time = np.array(waiting_times[2])

    print('Average wait time, Single slot', single_slot_wait_time.mean())
    print('Average wait time, Double slot', double_slot_wait_time.mean())
    print('Average wait time, Quad slot', quad_slot_wait_time.mean())

    print('Sample Variance, Single slot', np.var(single_slot_wait_time))
    print('Sample Variance, Double slot', np.var(double_slot_wait_time))
    print('Sample Variance, Quad slot', np.var(quad_slot_wait_time))

    # 2 sided, 1 sample t tests
    print('Single slot T test', stats.ttest_1samp(single_slot_wait_time, 9.0))
    # 4.36 is the expected wait time with c = 2
    print('Double slot T test', stats.ttest_1samp(double_slot_wait_time, 4.26))
    # 1.96 is the expected wait time with c = 4
    print('Quad slot T test', stats.ttest_1samp(quad_slot_wait_time, 1.96))

    return waiting_times


def question_3_2():
    print('===========\n')
    print('How does the sample variance of our E(W) depend on ρ? \n')
    print('How does the sample variance of our E(W) depend on the number of customers per simulation? \n')
    print('===========\n')

    lambdas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    def repeat_until_significant(nb_jobs):
        # simulations required for significance for each value of RHO
        samp_var = np.zeros(len(lambdas))

        print("Simulation starting...")
        for i in range(len(lambdas)):
            nb_simulations = 30
            count = 0
            mean_waiting_times = []

            while count < nb_simulations:
                random.seed(random.random())
                server_priority = ServerPriority(1, 1, lambdas[i], random.expovariate, random.expovariate, lambda idx: idx <= nb_jobs)
                server_priority.env.run()

                mean_waiting_times.append(statistics.mean(server_priority.waiting_times))
                count += 1
            samp_var[i] = np.var(mean_waiting_times)

        print("Simulation done.")

        return samp_var

    xs = [lambdas, lambdas, lambdas]
    ys = [repeat_until_significant(1000), repeat_until_significant(5000), repeat_until_significant(10000)]
    labels = ['1,000 jobs', '5,000 jobs', '10,000 jobs']
    graphic_tools.y_log_plotter(xs, ys, labels, r'$\rho$ Influence Over Sample Variance', r'$\rho$', r'$S^2$')


def question_3_3():

    nb_jobs = 10000
    lambdas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    samp_mean = [np.zeros(len(lambdas)), np.zeros(len(lambdas))]
    samp_var = [np.zeros(len(lambdas)), np.zeros(len(lambdas))]

    print("Simulation starting...")
    for i in range(len(lambdas)):
        nb_simulations = 50
        count = 0
        mean_waiting_times = [[], []]

        while count < nb_simulations:
            random.seed(random.random())
            server_fifo = ServerFIFO(1, 1,  lambdas[i], random.expovariate, random.expovariate, lambda idx: idx <= nb_jobs)
            server_fifo.env.run()

            server_priority = ServerPriority(1, 1, lambdas[i], random.expovariate, random.expovariate, lambda idx: idx <= nb_jobs)
            server_priority.env.run()

            mean_waiting_times[0].append(statistics.mean(server_fifo.waiting_times))
            mean_waiting_times[1].append(statistics.mean(server_priority.waiting_times))
            count += 1

        data = [np.array(mean_waiting_times[0]), np.array(mean_waiting_times[1])]
        labels = ['FIFO queue', 'Priority queue']
        graphic_tools.box_plot(data, labels, r'Median, Quartiles, Intervals with $\rho = {:.2f}$'.format(lambdas[i]), r'$E_c(W)$')

        fifo_wait_time = np.array(mean_waiting_times[0])
        priority_wait_time = np.array(mean_waiting_times[1])

        samp_mean[0][i] = fifo_wait_time.mean()
        samp_mean[1][i] = priority_wait_time.mean()
        samp_var[0][i] = np.var(fifo_wait_time)
        samp_var[1][i] = np.var(priority_wait_time)

    print("Simulation done.")

    labels = [r'FIFO $10^4$ jobs', 'Priority $10^4$ jobs']
    graphic_tools.y_log_plotter([lambdas, lambdas], samp_var, labels, r'Comparaison between FIFO and Priority queue', r'$\rho$', r'$S^2$')
    graphic_tools.simple_plotter([lambdas, lambdas], samp_mean, labels, r'Comparaison between FIFO and Priority queue', r'$\rho$', r'$E(W)$')


def question_4_1():
    print('===========\n')
    print('Notched Box Plot Deterministic vs Expo')
    print('===========\n')

    print("Simulation starting...")

    SIMS = 50
    nb_jobs = 10000
    RHO = 0.9

    # waiting_times[0] is the 
    waiting_times = [[], [], [], []]

    for j in range(0, SIMS):
        random.seed(random.random())
        
        det_one_slot = ServerFIFO(1, 1, 1 * RHO, random.expovariate, lambda z: 1 / z, lambda idx: idx <= nb_jobs)
        det_one_slot.env.run()

        det_two_slot = ServerFIFO(1, 2, 2 * RHO, random.expovariate, lambda z: 1 / z, lambda idx: idx <= nb_jobs)
        det_two_slot.env.run()

        exp_one_slot = ServerFIFO(1, 1, 1 * RHO, random.expovariate, random.expovariate, lambda idx: idx <= nb_jobs)
        exp_one_slot.env.run()

        exp_two_slot = ServerFIFO(1, 2, 2 * RHO, random.expovariate, random.expovariate, lambda idx: idx <= nb_jobs)
        exp_two_slot.env.run()

        waiting_times[0].append(statistics.mean(det_one_slot.waiting_times))
        waiting_times[1].append(statistics.mean(det_two_slot.waiting_times))
        waiting_times[2].append(statistics.mean(exp_one_slot.waiting_times))
        waiting_times[3].append(statistics.mean(exp_two_slot.waiting_times))

    print("Simulation Done")

    data = [np.array(waiting_times[0]), np.array(waiting_times[1]), np.array(waiting_times[2]), np.array(waiting_times[3])]
    labels = ['c = 1 Det.', 'c = 2 Det.', 'c = 1 Expo.', 'c = 2 Expo.']
    graphic_tools.box_plot(data, labels, 'Median, Quartiles, Intervals', r'$E_c(W)$')    


def question_4_2():
    print('===========\n')
    print('Deterministic Sample Variance')
    print('===========\n')

    print("Simulation starting...")

    # Test for a range of RHO values 
    RHO = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    SIMS  = 30

    def repeat_for_rho(customers, slots, distribution_b):
        mean_waiting_times = []
        # simulations required for significance for each value of RHO
        samp_var = np.zeros(len(RHO))
        for i in range(len(RHO)):
            count = 0
            while count < SIMS:
                server_fifo = ServerFIFO(1, slots, 1 * RHO[i], random.expovariate, distribution_b, lambda idx: idx <= customers)
                server_fifo.env.run()
                mean_waiting_times.append(statistics.mean(server_fifo.waiting_times))
                count += 1
            samp_var[i] = np.var(mean_waiting_times, ddof = 1)
        return samp_var

    var_one_expo = repeat_for_rho(1000, 1, random.expovariate)
    var_ten_expo = repeat_for_rho(10000, 1, random.expovariate)
    var_one_det = repeat_for_rho(1000, 1, lambda z: 1 / z)
    var_ten_det =repeat_for_rho(10000, 1, lambda z: 1 / z)

    print("Simulation Done")

    data = [var_one_expo, var_ten_expo, var_one_det, var_ten_det]
    line_labels = ['One Thousand Customers Expo', 'Ten Thousand Customers Expo', 'One Thousand Customers Det', 'Ten Thousand Customers Det']
    graphic_tools.sample_stat_rho(RHO, data, line_labels, r'$\rho$', r'$S^2$', r'$\rho$ Influence Over Sample Variance', 'log')

def question_4_3():
    print('===========\n')
    print('Hyper-Exponential Stats Table')
    print('===========\n')

    SIMS = 50
    RHO = 0.9
    nb_jobs = 10000

    print("Simulation starting...")

    # waiting_times[0] is the 
    waiting_times = [[], [], []]

    for j in range(0, SIMS):
        random.seed(random.random())
        
        one_slot = ServerFIFO((1, 1/5), 1, 1 * RHO, random.expovariate, distributions.long_tail, lambda idx: idx <= nb_jobs)
        one_slot.env.run()

        two_slot = ServerFIFO((1, 1/5), 2, 2 * RHO, random.expovariate, distributions.long_tail, lambda idx: idx <= nb_jobs)
        two_slot.env.run()

        four_slot = ServerFIFO((1, 1/5), 4, 4 * RHO, random.expovariate, distributions.long_tail, lambda idx: idx <= nb_jobs)
        four_slot.env.run()

        waiting_times[0].append(statistics.mean(one_slot.waiting_times))
        waiting_times[1].append(statistics.mean(two_slot.waiting_times))
        waiting_times[2].append(statistics.mean(four_slot.waiting_times))

    one_slot = np.array(waiting_times[0])
    two_slot = np.array(waiting_times[1])
    four_slot = np.array(waiting_times[2])

    one_slot_mean = one_slot.mean()
    two_slot_mean = two_slot.mean()
    four_slot_mean = four_slot.mean()

    print('Average wait time, Single slot', one_slot_mean)
    print('Average wait time, Double slot', two_slot_mean)
    print('Average wait time, Quad slot', four_slot_mean)

    print('Sample Variance, Single slot', np.var(one_slot))
    print('Sample Variance, Double slot', np.var(two_slot))
    print('Sample Variance, Quad slot', np.var(four_slot))

    print("Simulation done")


def question_4_4():
    print('===========\n')
    print('How does the mean of E(W) depend on ρ with a HyperExponential Service Time Distribution? \n')
    print('===========\n')

    print("Simulation starting...")

    RHO = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    nb_jobs = 10000

    def repeat_for_rho(slots):
        # Test for a range of RHO values 
        # simulations required for significance for each value of RHO
        samp_mean = np.zeros(len(RHO))
        for i in range(len(RHO)):
            SIMS  = 10
            count = 0
            waiting_times = []
            while count < SIMS:
                random.seed(random.random())
                server_fifo = ServerFIFO((1, 1/5), slots, slots * RHO[i], random.expovariate, distributions.long_tail, lambda idx: idx <= nb_jobs)
                server_fifo.env.run()
                waiting_times.append(statistics.mean(server_fifo.waiting_times))
                count += 1
            samp_mean[i] = np.mean(waiting_times)
        return samp_mean

    one_slot = repeat_for_rho(1)
    two_slot = repeat_for_rho(2)
    four_slot = repeat_for_rho(4)

    print("Simulation done")

    data = [one_slot, two_slot, four_slot]
    line_labels = ['C = 1', 'C = 2', 'C = 4']
    graphic_tools.sample_stat_rho(RHO, data, line_labels, r'$\rho$', r'$E_c(W)$', r'$\rho$ Influence Over Sample Mean', 'linear')


def question_4_5():
    print('===========\n')
    print('How does the sample variance of our E(W) depend on ρ for Hyperexponential? \n')
    print('===========\n')

    print("Simulation starting...")

    RHO = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    SIMS  = 30

    def repeat_for_rho(customers):
        # Test for a range of RHO values 
        # simulations required for significance for each value of RHO
        samp_var = np.zeros(len(RHO))
        for i in range(len(RHO)):
            count = 0
            waiting_times = []
            while count < SIMS:
                random.seed(random.random())
                server_fifo = ServerFIFO((1, 1/5), 1, 1 * RHO[i], random.expovariate, distributions.long_tail, lambda idx: idx <= customers)
                server_fifo.env.run()
                waiting_times.append(statistics.mean(server_fifo.waiting_times))
                count += 1
            samp_var[i] = np.var(waiting_times)
        return samp_var

    one_thous = repeat_for_rho(1000)
    five_thous = repeat_for_rho(5000)
    ten_thous = repeat_for_rho(10000)

    print("Simulation done")

    data = [one_thous, five_thous, ten_thous]
    line_labels = ['1000 Customers', '5000 Customers', '10000 Customers']

    graphic_tools.sample_stat_rho(RHO, data, line_labels, r'$\rho$', r'$S^2$', r'$\rho$ Influence Over Sample Variance, Hyperexponential', 'log')

if __name__ == '__main__':
    question_2_1()
    question_2_2()
    question_2_3()
    question_3_1()
    question_3_2()
    question_3_3()
    question_4_1()
    question_4_2()
    question_4_3()
    question_4_4()
    question_4_5()
