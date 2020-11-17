# Assignment 1 -  Computing the area of the Mandelbrot set

##  How to run a demonstration

### Main file
The code required to run a demonstration of the results of the report is located in the file `main.py`.
To run the demonstration, in command line, run this command:

```
python3 main.py
```

You should be aware that not all the function call in this demonstration file contains the same parameters than the one used
in the report. These few changes are here to let you run the demonstration a little bit faster.

- Part 1 related to Mandelbrot set visualization contains the same results.
- Part 2 related to Monte-Carlo approach with pure random sampling, which study its convergence, is using smaller parameters: 1,000 sampling and 1,000 iterations instead of 5,000 samples, 20,000 iterations; or 100,000 samples and 1,000 iterations, etc. 
- Part 3 and 4 mostly use the same parameters and so remains quite slow.

###  Invididual testing

However, you might still feel free to run each files individually. While it will not contains the same parameters from the report, 
you might experiments more easily our implementations.


## Architecture of the repository

Here is the main architecture:

- main.py : demonstration file
- mandelbrot.py : implement mandelbrot recursive sequence, as well as visualization tools of the Mandelbrot set. Used in Part 1.
- study_mandelbrot.py : investigates the convergence of points from the complex plan when using the recursive sequence. Used in Part 1.
- monte_carlo.py : Monte-carlo algorithm used in Part 2, Part 3 and Part 4.
- investigate_convergence.py : compute the relative error of monte-carlo approach with provided sampling method. The convergence is studied by maximal number of iterations, or size of the samples set (random points in complex plan). Used in part 2.
- investigate_error.py : it runs X simulations of Monte-Carlo approach with each sampling methods (Latin Hypercube, Orthogonal, Halton, Pure Random), depending on the maximal number of iterations or size of the samples set. The results computed visualized and used in the report are : the average area, the variance. Used in Part 3 and Part 4.
- sampling_method.py : Files with the different sampling method : pure random (pure_random), latin hypercube (latin_square_chaos), orthogonal sampling (orthogonal_native), halton sequence(halton_sequence).
- statistical_analysis_utils.py : Formula used for computing mean, variance, confidence interval: sample_mean, recursive_sample_mean, sample_variance, etc.
- statistical_analysis.py : Compute confidence interval: until interval condition is met, or with a fixed number of simultions.
- graphic_utils.py : Graphic tools, most of the code to plot results (except Mandelbrot set) are located here.
