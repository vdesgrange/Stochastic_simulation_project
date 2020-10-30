import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

from monte_carlo import monte_carlo_integration

WIDTH = 1000
HEIGHT = 1000
MAX_ITER = 700
RE_MIN, RE_MAX = -2.02, 0.49
IM_MIN, IM_MAX = -1.15, 1.15

# colour scheme for our visualisation
# https://coolors.co
palette = ['#008148', '#C6C013', '#EF8A17', '#EF2917']


class ZoomTool:
    """
    To clean - simple zoom tool (only zooming right now).
    Zoom x10 at the clicked point in the image window.
    """
    def __init__(self, ax, re, im):
        self.ax = ax
        self.press = None
        self.re = re
        self.im = im

    def connect(self):
        self.cidpress = self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)

    def on_press(self, event):
        scale_factor = 0.1  # scale
        re, im = self.re, self.im  # Current real axis x (min, max) and imaginary axis y (min, max)
        w, h = WIDTH, HEIGHT  # Plot width

        # Retrieve (x, y) coordinates clicked
        xdata = event.xdata
        ydata = event.ydata

        # Convert to image coordinates to complex coordinates
        x = re[0] + (xdata / w) * (re[1] - re[0])
        y = im[0] + (ydata / h) * (im[1] - im[0])

        # Get x-, y-axis range. Divided by 2 to center clicked point.
        cur_xrange = (re[1] - re[0])*.5
        cur_yrange = (im[1] - im[0])*.5

        # Determine new image window in complex coordinates
        global RE_MIN, RE_MAX, IM_MIN, IM_MAX  # Update global variable
        RE_MIN, RE_MAX = x - cur_xrange * scale_factor, x + cur_xrange * scale_factor
        IM_MIN, IM_MAX = y - cur_yrange * scale_factor, y + cur_yrange * scale_factor
        self.re = (RE_MIN, RE_MAX)
        self.im = (IM_MIN, IM_MAX)

        print("Real (min, max) = ", RE_MIN, RE_MAX)
        print("Imaginary (min, max) = ", IM_MIN, IM_MAX)

        # Compute new fractal and refresh plot
        new_img, result = mandelbrot_set(self.re, self.im)
        self.ax.imshow(new_img)
        self.ax.figure.canvas.draw_idle()

    def disconnect(self):
        self.ax.figure.canvas.mpl_disconnect(self.cidpress)


def grid_map(x, y, re=(RE_MIN, RE_MAX), im=(IM_MIN, IM_MAX)):
    """
    Conversion: mapping from grid points to the complex plane
    :param x: x coordinate from the grid
    :param y: y coordinate from the grid
    :param re: tuple of minimal and maximal coordinates from the real axis
    :param im: tuple of minimal and maximal coordinates from the imaginary axis
    :return complex: the complex coordinates (r, i) of the point (x,y)
    """
    w, h = WIDTH, HEIGHT
    r_part = re[0] + (x / w) * (re[1] - re[0])
    i_part = im[0] + (y / h) * (im[1] - im[0])
    return complex(r_part, i_part)


def get_color(it):
    """
    Returns a hexadecimal colour to fill individual pixel based on number of iterations
    :param it: integer, number of iteration
    :return: string, hexadecimal color
    """
    color = (it / MAX_ITER) * (len(palette) - 1)
    return palette[int(round(color))]


def experiment_func(a, b):
    """
    Function used by mandelbrot to compute Z_n+1
    """
    return a**2 + b


def mandelbrot(c, func=(lambda a, b: a**2 + b)):
    """
    Estimate if f(z)=z^2 + c diverges with complex number c.
    :param c: Complex number (point from the grid) to use.
    :param func: function used to compute Z_n+1
    :return: Number of iteration until divergence or a fixed maximal number of iteration.
    """
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = func(z, c)
        n += 1

    return n


def mandelbrot_set(re=(RE_MIN, RE_MAX), im=(IM_MIN, IM_MAX)):
    """
    Estimate set of complex numbers for which function f(z) = z^2 + c does not diverges.
    :param re: tuple of minimal and maximal coordinates from the real axis
    :param im: tuple of minimal and maximal coordinates from the imaginary axis
    :return: image with
    """
    w, h = WIDTH, HEIGHT

    # Create a simple image
    img = Image.new("RGB", (w, h), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Initialisation
    result = np.zeros((h, w))

    # For each pixel of the surface
    for x in range(0, w):  # Each column
        for y in range(0, h):  # Each row
            # Convert point (x, y) to complex coordinates (re, im)
            c = grid_map(x, y, re, im)

            # Determine if there's divergence with c.
            n = mandelbrot(c, experiment_func)
            if n == MAX_ITER:
                result[y, x] = 1
            draw.point([x, y], fill=get_color(n))
    return img, result


def graphic_tool(img):
    """
    Simple graphic tool to plot image of Mandelbrot set, and zoom in.
    :param img: mandelbrot set
    """
    fig = plt.figure()
    ax = fig.subplots()

    ax.imshow(img)
    ax.axis("off")
    ax.set_title("Mandelbrot")

    # Add simple zoom in tool.
    plot_with_zoom = ZoomTool(ax, (RE_MIN, RE_MAX), (IM_MIN, IM_MAX))
    plot_with_zoom.connect()
    plt.show()
    plot_with_zoom.disconnect()


if __name__ == '__main__':
    img, result = mandelbrot_set()
    graphic_tool(img)
    monte_carlo_integration(result, WIDTH, HEIGHT, (RE_MIN, RE_MAX), (IM_MIN, IM_MAX))

