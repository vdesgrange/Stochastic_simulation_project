# Assignment 3 - TSP Optimisation

##  How to run a demonstration

### Main file
The code required to run a demonstration of the results of the report is located in the file `main.py`.
To run the demonstration, in command line, run this command:

```
python3 main.py
```

Since our simulations are resource intensive we have included an 'archive' functionality, our key results are stored as binary files and can be retrieved without re-running the simulations. When main.py is executed, you will have the option of re-executing all of our experiments or retrieving the saved experimental data. We suggest you first run these archived experiments to see some of our best results. 

Part 1:  Summary statistics tables and local optimum path diagrams for all 3 problems
Part 2:  diagrams and data related to our experiments on the cooling schedule. This includes initial temperature values and lowering methods. 
Part 3: experiments on markov chain length and the relationship between steps and chain length.  

###  Invididual testing

However, you might still feel free to run each files individually. While it will not contains the same parameters from the report, you might experiments more easily our implementations.


## Architecture of the repository

Here is the main architecture:

- main.py : Demonstration file
- annealing.py : Our primary algorthms. We have two versions of the annealing algorithm: 1. relative cost difference 2. absolute cost difference. 
- archives.py : functionality for retrieving archived experimental data
- convergence.py : helper file for co-ordinating repeat simulations and plotting convergence behaviour
- geometry.py : functions related to distance calculation. We use precalculated distance matrices to increase the speed of our implmentation. 
- graphics.py : interface for creating matplotlib plots
- stats.py : summary statistics helper using Numpy
- utis.py : reading tsplib files and creating random permutations.