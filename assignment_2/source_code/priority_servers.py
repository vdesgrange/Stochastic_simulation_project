import logging
import sys
import math
import simpy
import random
import statistics

from servers import Server

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.disable(logging.DEBUG)


class ServerPriority(Server):
    def __init__(self, mu, n, lamb_da, a_distribution, b_distribution, cond):
        """
        :param mu: capacity of the server
        :param n: number of server
        :param lamb_da: arrival rate into the system as a whole
        :param a_distribution: inter-arrival time distribution
        :param b_distribution: service time (job size) distribution
        """
        super(ServerPriority, self).__init__(mu, n, lamb_da, a_distribution, b_distribution)

        self.env = simpy.Environment()
        self.resource = simpy.PriorityResource(self.env, capacity=n)  # n*mu to replace n servers of mu capacity.
        self.env.process(self.run(cond))

    def get_job_size(self):
        tib = self.b_distribution(self.mu)
        priority = math.ceil(tib * 10**8)
        return tib, priority

    def job(self, name):
        """
        Job behavior in the system: waiting, processing, cancellation behavior.
        :param name: Name of the job task
        """
        received = self.env.now
        logging.debug('%7.4f %s: Job received' % (received, name))
        tib, priority = self.get_job_size()

        with self.resource.request(priority=priority) as req:
            yield req

            wait = self.env.now - received

            # We got to the counter
            logging.debug('%7.4f %s: Waiting time %6.3f' % (self.env.now, name, wait))

            yield self.env.timeout(tib)  # tib
            logging.debug('%7.4f %s: Processing time %6.3f' % (self.env.now, name, tib))

        self.logger(received, wait, tib)


if __name__ == '__main__':
    limit = 10000
    total_waiting_times = []

    for i in range(10):
        print("Simulation %d" % i)
        random.seed(random.random())
        server_priority = ServerPriority(mu=1, n=1, lamb_da=0.9, a_distribution=random.expovariate, b_distribution=random.expovariate)
        server_priority.env.run(until=limit)
        total_waiting_times += server_priority.waiting_times

    ave_waiting_time = statistics.mean(total_waiting_times)
    print("Mean waiting time: E(W) = ", ave_waiting_time)
