import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import math

WIDTH = 600
HEIGHT = 400
MAX_ITER = 100
RE_MIN, RE_MAX = -2, 1
IM_MIN, IM_MAX = -1, 1

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
        new_img = main(self.re, self.im)
        self.ax.imshow(new_img)
        self.ax.figure.canvas.draw_idle()

    def disconnect(self):
        self.ax.figure.canvas.mpl_disconnect(self.cidpress)

# returns a hexadecimal colour to fill individual
# pixel based on number of iterations
def get_color(it):
    color = (it / MAX_ITER) * (len(palette) - 1)
    return palette[int(round(color))]

def experiment_func(a, b):
    return a**2 + b

def mandelbrot(c, func=(lambda a, b: a**2 + b)):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = func(z, c)
        n += 1

    return n

def main(re=(RE_MIN, RE_MAX), im=(IM_MIN, IM_MAX)):
    w, h = WIDTH, HEIGHT
    img = Image.new("RGB", (w, h), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    for x in range(0, w):
        for y in range(0, h):
            c = complex(re[0] + (x / w) * (re[1] - re[0]), im[0] + (y / h) * (im[1] - im[0]))
            n = mandelbrot(c, experiment_func)
            draw.point([x, y], fill = get_color(n))

    return img


def graphic_tool(img):
    fig = plt.figure()
    ax = fig.subplots()
    ax.imshow(img)
    ax.axis("off")
    ax.set_title("Mandelbrot")
    plot_with_zoom = ZoomTool(ax, (RE_MIN, RE_MAX), (IM_MIN, IM_MAX))
    plot_with_zoom.connect()
    plt.show()
    plot_with_zoom.disconnect()

if __name__ == '__main__':
    img = main()
    graphic_tool(img)
