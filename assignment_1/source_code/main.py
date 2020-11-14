import mandelbrot
import investigate_convergence
import statistical_analysis
from sampling_method import pure_random, halton_sequence, latin_square_chaos, orthogonal


def assignment_1_main():
    print("====================================")
    print("=== 1 - Visualize Mandelbrot set ===")
    print("====================================")

    Get mandelbrot set
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
    re_area_1 = (-0.5829980107526879, -0.557898010752688)  # Pre-determined coordinates using Zoom-in tool.
    im_area_1 = (-0.5752179435483872, -0.5522179435483873)
    img2 = mandelbrot.mandelbrot_set(re_area_1, im_area_1, 100)
    mandelbrot.mandelbrot_visualizer_tool(img2)
    print("Done")

    # Example 2
    print("Zoom into section (-0.12 < re < -0.09 and -0.93 < im < -0.91)")
    re_area_2 = (-0.1181925672043013, -0.09309256720430129)  # Pre-determined coordinates using Zoom-in tool.
    im_area_2 = (-0.93586814516129, -0.9128681451612901)
    img3 = mandelbrot.mandelbrot_set(re_area_2, im_area_2, 100)
    mandelbrot.mandelbrot_visualizer_tool(img3)
    print("Done")

    print("===================================")
    print("=== 2 - Investigate convergence ===")
    print("===================================")

    print("=== Study convergence of mandelbrot set in complex plan")
    investigate_convergence.study_convergence_mandelbrot(re, im, w, h)
    print("Done")

    print("=== Evolution of difference by number of iterations and sampling ===")
    print("Pure random sampling method")
    print("Evolution of difference from 0 to 1000 iteration with [10^3, 10^4, 10^5] random points")

    investigate_convergence.study_difference_by_iteration(1000, 1500, re, im, w, h)
    investigate_convergence.study_difference_by_iteration(50000, 1500, re, im, w, h)

    print("Done")

    print("Evolution of difference from 0 to 10^4 random pints with [500, 800, 1000] iterations")
    investigate_convergence.study_difference_by_sampling(10000, 800, re, im, w, h)
    investigate_convergence.study_difference_by_sampling(10000, 1000, re, im, w, h)
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
    x_, s2_, min, max = statistical_analysis.confidence_interval_estimate_fixed(sims, 2500, 600, re, im, w, h, orthogonal)
    print("Sample mean     x_  = ", x_)
    print("Sample variance s2_ = ", s2_)
    print("Confidence interval = [{:5f}, {:5f}]".format(min, max))


    print("=== Study confidence interval by sampling method, When to Stop Algorithm ===")
    print("=== Pure random ===")
    x_, s2_, min, max = statistical_analysis.confidence_interval_estimate(0.008, 50, 10000, 800, re, im, w, h, pure_random)
    print("Sample mean     x_  = ", x_)
    print("Sample variance s2_ = ", s2_)
    print("Confidence interval [{:5f}, {:5f}] ".format(min, max))
    print("Done")

    print("=== Latin Hypercube ===")
    x_, s2_, min, max = statistical_analysis.confidence_interval_estimate(0.008, 50, 10000, 800, re, im, w, h, latin_square_chaos)
    print("Sample mean     x_  = ", x_)
    print("Sample variance s2_ = ", s2_)
    print("Confidence interval = [{:5f}, {:5f}]".format(min, max))
    print("Done")

    print("=== Orthogonal Sampling ===")
    x_, s2_, min, max = statistical_analysis.confidence_interval_estimate(0.008, 50, 10000, 800, re, im, w, h, orthogonal)
    print("Sample mean     x_  = ", x_)
    print("Sample variance s2_ = ", s2_)
    print("Confidence interval = [{:5f}, {:5f}]".format(min, max))

    print("===================================================")
    print("=== 4 - Improve convergence rate of Monte-Carlo ===")
    print("===================================================")

    print("=== Halton Sequence ===")
    x_, s2_, min, max = statistical_analysis.confidence_interval_estimate(0.008, 30, 10000, 800, re, im, w, h, halton_sequence)
    print("Sample mean     x_  = ", x_)
    print("Sample variance s2_ = ", s2_)
    print("Confidence interval = [{:5f}, {:5f}]".format(min, max))


if __name__ == '__main__':
    assignment_1_main()
