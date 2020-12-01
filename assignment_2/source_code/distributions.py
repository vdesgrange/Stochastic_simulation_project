import random

# hyperexponential
def long_tail(capacities):
    mu_1, mu_2 = capacities
    p_1 = 0.75
    p_2 = 0.25        
    # decide which distribution to sample from 
    dist = random.choices([0, 1], [p_1, p_2])[0]
    if dist == 0:
        t = random.expovariate(mu_1)
    else:
        t = random.expovariate(mu_2)
    return t
