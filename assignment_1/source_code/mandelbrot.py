import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
from graphic_utils import palette

WIDTH = 600
HEIGHT = 400
MAX_ITER = 100
RE_MIN, RE_MAX = -2.02, 0.49
IM_MIN, IM_MAX = -1.15, 1.15


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
        w, h = int(abs(self.ax.viewLim.size[0])), int(abs(self.ax.viewLim.size[1]))  # Plot width

        # Retrieve (x, y) coordinates clicked
        xdata = event.xdata
        ydata = event.ydata

        # Convert to image coordinates to complex coordinates
        # x = re[0] + (xdata / w) * (re[1] - re[0])
        # y = im[0] + (ydata / h) * (im[1] - im[0])
        x = xdata
        y = ydata

        # Get x-, y-axis range. Divided by 2 to center clicked point.
        cur_xrange = (re[1] - re[0])*.5
        cur_yrange = (im[1] - im[0])*.5

        # Determine new image window in complex coordinates
        re_min, re_max = x - cur_xrange * scale_factor, x + cur_xrange * scale_factor
        im_min, im_max = y - cur_yrange * scale_factor, y + cur_yrange * scale_factor
        self.re = (re_min, re_max)
        self.im = (im_min, im_max)

        print("Real (min, max) = ", re_min, re_max)
        print("Imaginary (min, max) = ", im_min, im_max)

        # Compute new fractal and refresh plot
        new_img = mandelbrot_set(self.re, self.im)
        self.ax.imshow(new_img, extent=[re_min, re_max, im_min, im_max])  # 
        self.ax.figure.canvas.draw_idle()

    def disconnect(self):
        self.ax.figure.canvas.mpl_disconnect(self.cidpress)


def mandelbrot_visualizer_tool(img):
    """
    Simple graphic tool to plot image of Mandelbrot set, and zoom in.
    :param img: mandelbrot set
    """
    fig = plt.figure()
    ax = fig.subplots()

    ax.imshow(img, extent=(RE_MIN, RE_MAX, IM_MIN, IM_MAX))  #
    # ax.axis("off")
    ax.set_title("Mandelbrot")

    # Add simple zoom in tool.
    plot_with_zoom = ZoomTool(ax, (RE_MIN, RE_MAX), (IM_MIN, IM_MAX))
    plot_with_zoom.connect()
    plt.show()
    plot_with_zoom.disconnect()


def grid_map(x, y, re=(RE_MIN, RE_MAX), im=(IM_MIN, IM_MAX), w=WIDTH, h=HEIGHT):
    """
    Conversion: mapping from grid points to the complex plane
    :param x: x coordinate from the grid
    :param y: y coordinate from the grid
    :param re: tuple of minimal and maximal coordinates from the real axis
    :param im: tuple of minimal and maximal coordinates from the imaginary axis
    :param w: width of the grid
    :param h: height of the grid
    :return complex: the complex coordinates (r, i) of the point (x,y)
    """
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


def mandelbrot(c, max_iter=MAX_ITER):
    """
    Estimate if f(z)=z^2 + c diverges with complex number c.
    :param c: Complex number (point from the grid) to use.
    :param max_iter: Maximal number of iteration fixed to consider complex number in mandelbrot set.
    :return: Number of iteration until divergence or a fixed maximal number of iteration.
    """
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z**2 + c
        n += 1

    return n


def mandelbrot_detailed(c, max_iter=MAX_ITER):
    """
    Estimate if f(z)=z^2 + c diverges with complex number c.
    :param c: Complex number (point from the grid) to use.
    :param max_iter: Maximal number of iteration fixed to consider complex number in mandelbrot set.
    :return: Array of computed z
    """
    z = 0
    n = 0
    fz = [c]
    while abs(z) <= 2 and n < max_iter:
        z = z**2 + c
        fz.append(z)
        n += 1

    return fz


def mandelbrot_set(re=(RE_MIN, RE_MAX), im=(IM_MIN, IM_MAX), max_iter=MAX_ITER, w=WIDTH, h=HEIGHT):
    """
    Estimate set of complex numbers for which function f(z) = z^2 + c does not diverges.
    :param re: tuple of minimal and maximal coordinates from the real axis
    :param im: tuple of minimal and maximal coordinates from the imaginary axis
    :param max_iter: Maximal number of iteration
    :param w: width of the grid
    :param h: height of the grid
    :return: image
    """

    # Create a simple image
    img = Image.new("RGB", (w, h), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    # For each pixel of the surface
    for x in range(0, w):  # Each column
        for y in range(0, h):  # Each row
            # Convert point (x, y) to complex coordinates (re, im)
            c = grid_map(x, y, re, im)

            # Determine if there's divergence with c.
            n = mandelbrot(c, max_iter)
            draw.point([x, y], fill=get_color(n))
    return img


if __name__ == '__main__':
    img = mandelbrot_set()
    mandelbrot_visualizer_tool(img)

