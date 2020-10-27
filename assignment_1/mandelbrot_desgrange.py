import numpy as np
import cmath
from PIL import Image, ImageDraw

WIDTH = 600
HEIGHT = 400
MAX_ITER = 100
RE_MIN, RE_MAX = -2, 1
IM_MIN, IM_MAX = -1, 1


def mandelbrot(c, func=(lambda a, b: a**2 + b)):
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = func(z, c)
        n += 1

    return n

def experiment_func(a, b):
    # return cmath.exp(-a**2) + b
    return a**2 + b

def main(name):
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            c = complex(RE_MIN + (x / WIDTH) * (RE_MAX - RE_MIN), IM_MIN + (y / HEIGHT) * (IM_MAX - IM_MIN))
            n = mandelbrot(c, experiment_func)
            color = 255 - int(n * 255 / MAX_ITER)
            draw.point([x, y], (color, color, color))

    img.save(name, "PNG")


if __name__ == '__main__':
    main("test.png")