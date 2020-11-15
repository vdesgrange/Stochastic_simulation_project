import numpy as np
import matplotlib.pyplot as plt

RUNS = 100
MAJOR = 5
SAMPLES = MAJOR **2

xlist = np.zeros((MAJOR, MAJOR))
ylist = np.zeros((MAJOR, MAJOR))
x_scale = 600 / SAMPLES
y_scale = 400 / SAMPLES

i = 0 
j = 0
k = 0 
m = 0 
x = 0
y = 0
m = 0

x_samples = []
y_samples = []

for i, val in enumerate(range(0, MAJOR)):
    for j, val in enumerate(range(0, MAJOR)):
        m += 1
        xlist[i][j] = m
        ylist[i][j] = m 

for k, val in enumerate(range(0, RUNS)):
    for i, val in enumerate(range(0, MAJOR)):
        np.random.shuffle(xlist[i])
        np.random.shuffle(ylist[i])
    for i, val in enumerate(range(0, MAJOR)):
        for j, val in enumerate(range(0, MAJOR)): 
            x = x_scale * (xlist[i][j] + np.random.uniform(0, 0.9))
            y = y_scale * (ylist[j][i] + np.random.uniform(0, 0.9))
            x_samples.append(x)
            y_samples.append(y)


plt.Figure()
plt.scatter(x_samples, y_samples)
plt.show()        
    



