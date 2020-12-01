# Assignment 2 -  Discrete-event simulation - Multiple queues and multiple servers

##  How to run a demonstration

### Main file

The code required to run a demonstration of the results of the report is located in the file `main.py`.
To run the demonstration, in command line, run this command:

```
python3 main.py
```

The several experiments we made have been splits between different function. If you want to reduce computing time, 
feel free to comment the function call at the bottom of the `main.py` file.

###  Invididual testing

However, you might still feel free to run each files individually. 
While it will not contains the same parameters from the report, nor the experiments all grouped together in `main.py`, 
you might find interesting to have a look to our implementations.

## Architecture of the repository

Here is the main architecture:

- main.py : demonstration file
- servers.py : an abstract class which we used as a base for the different type of queue we experimented. It
contains method for logging some information on arrival time, waiting time, service time, etc. As well as characteristic
of the servers and distribution used for arrival and service time.
- fifo_servers.py : An implementation of a FIFO (first in - first out) queue scheduling system, inherited from the 
abstract class Server. Used for Part 2  and Part 4 of the assignment (as it allows to provide custom distribution).
- priority_servers.py : An implementation of a Non-preemptive priority queue scheduling system, inherited from the 
abstract class Server. Used for Part 3 of the assignment (as it allows to provide custom distribution). It use
a simple function to convert service time obtains from exponential distribution into an integer used for priority based
on shortest job.
- graphic_utils.py : Graphic tools, all code to plots function are located here.
- distributions.py : Contains custom distribution, hyper-exponential, used in the Part 4 of the assignment.
