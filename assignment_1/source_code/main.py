import mandelbrot
import investigate_convergence
import investigate_error
import statistical_analysis
import statistical_analysis_utils
import study_mandelbrot

from sampling_method import pure_random, halton_sequence, latin_square_chaos, orthogonal_native
import numpy as np
from scipy import stats


def assignment_1_main():
    print("====================================")
    print("=== 1 - Visualize Mandelbrot set ===")
    print("====================================")

    # Get mandelbrot set
    w, h = mandelbrot.WIDTH, mandelbrot.HEIGHT
    re = (mandelbrot.RE_MIN, mandelbrot.RE_MAX)
    im = (mandelbrot.IM_MIN, mandelbrot.IM_MAX)
    img = mandelbrot.mandelbrot_set(re, im, 100)

    # Graphic tool to plot image of Mandelbrot set, and zoom in.
    mandelbrot.mandelbrot_visualizer_tool(img)
    print("Done")

    print("=== Visualize area of the Mandelbrot set ===")
    # Example 1
    print("Zoom into section (-0.58 < re < -0.56 and -0.57 < im < -0.55)")
    re_area_1 = (-0.6370549551120017, -0.3860549551120018)  # Pre-determined coordinates using Zoom-in tool.
    im_area_1 = (0.4692717684999561, 0.6992717684999561)
    img2 = mandelbrot.mandelbrot_set(re_area_1, im_area_1, 100)
    mandelbrot.mandelbrot_visualizer_tool(img2)
    print("Done")

    # Example 2
    print("Zoom into section (-0.12 < re < -0.09 and -0.93 < im < -0.91)")
    re_area_2 = (-0.783461796536797, -0.7583617965367971)  # Pre-determined coordinates using Zoom-in tool.
    im_area_2 = (0.10449567099567116, 0.12749567099567116)
    img3 = mandelbrot.mandelbrot_set(re_area_2, im_area_2, 100)
    mandelbrot.mandelbrot_visualizer_tool(img3)
    print("Done")

    print("=== Study convergence of mandelbrot set in complex plan")
    study_mandelbrot.example_convergence()
    # study_mandelbrot.study_convergence_mandelbrot(re, im, w, h)  # For random examples
    print("Done")

    print("===================================")
    print("=== 2 - Investigate convergence ===")
    print("===================================")

    print("=== Evolution of difference by number of iterations and sampling ===")
    print("Pure random sampling method")
    print("Evolution of difference from 0 to 20000 iteration with 5000 random points")
    print("(note: smaller value from report to accelerate computing time)")

    investigate_convergence.study_difference_by_iteration(1000, 1000, re, im, w, h)  # In report s=5000, i=20000
    investigate_error.study_iteration_convergence_single_method(1000, 1000, re, im, w, h)  # In report s=5000, i=20000
    print("Done")

    print("Evolution of difference from 0 to 20000 random points with 1000 iterations")
    print("(note: smaller value from report to accelerate computing time)")
    investigate_convergence.study_difference_by_sampling(1000, 1000, re, im, w, h)  # In report s=100000, i=1000
    investigate_error.study_samples_convergence_single_method(1000, 1000, re, im, w, h)  # In report s=50000, i=20000
    print("Done")

    print("================================================")
    print("=== 3 - Compare sampling method and accuracy ===")
    print("================================================")

    # the fixed number of simulation
    sims = 50

    print("=== Study confidence interval by sampling method, Fixed Simulations ===")
    print("=== Pure random, Simulations = {0} ===".format(sims))
    x_, s2_, min, max = statistical_analysis.confidence_interval_estimate_fixed(sims, 2500, 600, re, im, w, h, pure_random)
    print("Sample mean     x_  = ", x_)
    print("Sample variance s2_ = ", s2_)
    print("Confidence interval [{:5f}, {:5f}] ".format(min, max))
    print("Done")

    print("=== Latin Hypercube, Simulations = {0} ===".format(sims))
    x_, s2_, min, max = statistical_analysis.confidence_interval_estimate_fixed(sims, 2500, 600, re, im, w, h, latin_square_chaos)
    print("Sample mean     x_  = ", x_)
    print("Sample variance s2_ = ", s2_)
    print("Confidence interval = [{:5f}, {:5f}]".format(min, max))
    print("Done")

    print("=== Orthogonal Sampling, Simulations = {0} ===".format(sims))
    x_, s2_, min, max = statistical_analysis.confidence_interval_estimate_fixed(sims, 10000, 1000, re, im, w, h, orthogonal_native)
    print("Sample mean     x_  = ", x_)
    print("Sample variance s2_ = ", s2_)
    print("Confidence interval = [{:5f}, {:5f}]".format(min, max))


    print("=== Study confidence interval by sampling method, When to Stop Algorithm ===")
    print("=== Pure random ===")
    x_, s2_, min, max, it = statistical_analysis.confidence_interval_estimate(0.008, 50, 10000, 800, re, im, w, h, pure_random)
    print('Iterations it = ', it)
    print("Sample mean     x_  = ", x_)
    print("Sample variance s2_ = ", s2_)
    print("Confidence interval [{:5f}, {:5f}] ".format(min, max))
    print("Done")

    print("=== Latin Hypercube ===")
    x_, s2_, min, max, it = statistical_analysis.confidence_interval_estimate(0.008, 50, 10000, 800, re, im, w, h, latin_square_chaos)
    print('Iterations it = ', it)
    print("Sample mean     x_  = ", x_)
    print("Sample variance s2_ = ", s2_)
    print("Confidence interval = [{:5f}, {:5f}]".format(min, max))
    print("Done")

    print("=== Orthogonal Sampling ===")
    x_, s2_, min, max, it = statistical_analysis.confidence_interval_estimate(0.008, 50, 10000, 1000, re, im, w, h, orthogonal_native)
    print('Iterations it = ', it)
    print("Sample mean     x_  = ", x_)
    print("Sample variance s2_ = ", s2_)
    print("Confidence interval = [{:5f}, {:5f}]".format(min, max))

    print("===================================================")
    print("=== 4 - Improve convergence rate of Monte-Carlo ===")
    print("===================================================")

    print("=== Halton Sampling, Fixed Simulations, Simulations = {0} ===".format(sims))
    x_, s2_, min, max = statistical_analysis.confidence_interval_estimate_fixed(sims, 10000, 1000, re, im, w, h, halton_sequence)
    print("Sample mean     x_  = ", x_)
    print("Sample variance s2_ = ", s2_)
    print("Confidence interval = [{:5f}, {:5f}]".format(min, max))

    print("================================================")
    print("=== 4 - Convergence Test ===")
    print("================================================")

    runs = 30

    res_orth = []
    for j in range(0, runs):    
        print("=== Orthogonal Sampling ===")
        x_, s2_, min, max, it = statistical_analysis.confidence_interval_estimate(0.0025, 50, 2500, 700, re, im, w, h, orthogonal_native)
        res_orth.append(it) 
        print('Iterations it = ', it)
        print("Sample mean     x_  = ", x_)
        print("Sample variance s2_ = ", s2_)
        print("Confidence interval = [{:5f}, {:5f}]".format(min, max))

    print('Mean Iterations Required Orthogonal', np.mean(np.array(res_orth)))
    print('Variance Iterations Required Orthogonal', statistical_analysis_utils.sample_variance(np.array(res_orth)))

    res_hal = []
    for j in range(0, runs):    
        print("=== Halton Sequence ===, When to Stop Algorithm")
        x_, s2_, min, max, it = statistical_analysis.confidence_interval_estimate(0.0025, 50, 2500, 700, re, im, w, h, halton_sequence)
        res_hal.append(it)
        print('Iterations it = ', it)
        print("Sample mean     x_  = ", x_)
        print("Sample variance s2_ = ", s2_)
        print("Confidence interval = [{:5f}, {:5f}]".format(min, max))

    print('Mean Iterations Required Halton', np.mean(np.array(res_hal)))
    print('Variance Iterations Required Halton', statistical_analysis_utils.sample_variance(np.array(res_hal)))

    print(stats.ttest_ind(np.array(res_orth), np.array(res_hal), equal_var = False))


    print("================================================")
    print("=== 4 - Generate Variance Graphs ===")
    print("================================================")
    investigate_error.study_samples_convergence(50000, 1000)  # Report: s=50000, i=1000
    investigate_error.study_iteration_convergence(10000, 1500)

if __name__ == '__main__':
    assignment_1_main()
