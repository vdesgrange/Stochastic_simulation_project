# pip3 install Pillow 
# for a python3 PIL implementation
from PIL import Image, ImageDraw

max_it = 100

def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_it:
        z = z*z + c
        n += 1
    return n

# Image size (pixels)
WIDTH = 600
HEIGHT = 400

im = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
draw = ImageDraw.Draw(im)

for x in range(0, WIDTH):
    for y in range(0, HEIGHT):
        # coordinate to complex number mapping 
        c = complex(-2 + (x / WIDTH) * (3),
                    -1 + (y / HEIGHT) * (2))
        # how many iterations did it take?
        m = mandelbrot(c)
        colour = 255 - int(m * 255 / max_it)
        # add point to the map
        draw.point([x, y], (colour, colour, colour))

im.save('output.png', 'PNG')

