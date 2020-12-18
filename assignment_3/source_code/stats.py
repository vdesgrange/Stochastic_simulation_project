import numpy as np
import scipy.stats as stats
import statistics
from tabulate import tabulate


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), stats.sem(a)
    h = se * stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h


def statistical_analysis_convergence(costs):
    optimal_costs = [c[-1] for c in costs]
    table = tuple(zip(list(range(len(costs))), optimal_costs))
    print(tabulate(table, headers=["Simulation n.", "Distance terminal"]))

    variance = statistics.variance(optimal_costs)
    mean = statistics.mean(optimal_costs)
    confidence_interval = mean_confidence_interval(optimal_costs)
    print(tabulate([[mean, variance, confidence_interval]], headers=["Mean minimum path", "Sample variance", "95pc confidence interval"]))

def summary_stats(costs):
    print('Mean Distance is ', np.mean(np.array(costs)))
    print('Sample Varaince of Distance is ', np.var(np.array(costs), ddof=1))
    print('Confidence Interval is ', mean_confidence_interval(costs))
    print('Best achieved minimum is', np.min(costs))
    print('========================================================')