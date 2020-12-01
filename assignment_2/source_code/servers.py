from abc import ABC, abstractmethod


class Server(ABC):
    def __init__(self, mu, n, lamb_da, a_distribution, b_distribution):
        """
        :param mu: capacity of the server
        :param n: number of server
        :param lamb_da: arrival rate into the system as a whole
        :param a_distribution: inter-arrival time distribution
        :param b_distribution: service time (job size) distribution
        """
        self.lamb_da = lamb_da
        self.mu = mu
        self.n = n
        self.a_distribution = a_distribution
        self.b_distribution = b_distribution

        self.arrival_times = []
        self.waiting_times = []
        self.service_times = []

    def logger(self, receive, wait, process):
        """
        Store log data
        :param receive: time of reception of the job
        :param wait: waiting time in queue
        :param process: service time (job size), -1 if rejected
        """
        self.arrival_times.append(receive)
        self.waiting_times.append(wait)
        self.service_times.append(process)

    def run(self, cond=(lambda _: True)):
        """
        Job generator generates tasks randomly
        """
        i = 1
        while cond(i):
            c = self.job('Job%02d' % i)
            self.env.process(c)
            t = self.a_distribution(self.lamb_da)  # Inter arrival time distribution
            i += 1
            yield self.env.timeout(t)

    @abstractmethod
    def job(self, name):
        pass
