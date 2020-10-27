import numpy as np
import cmath
from PIL import Image, ImageDraw

WIDTH = 600
HEIGHT = 400
MAX_ITER = 100


def mandelbrot(c, func=(lambda a, b: a**2 + b)):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = func(z, c)
        n += 1

    return n


def experiment_func(a, b):
    return cmath.exp(-a**2) + b


def main(name):
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            c = complex(-2 + (x / WIDTH) * 3, -1 + (y / HEIGHT) * 2)
            n = mandelbrot(c, experiment_func)
            color = 255 - int(n * 255 / MAX_ITER)
            draw.point([x, y], (color, color, color))

    img.save(name, "PNG")


if __name__ == '__main__':
    main("test.png")