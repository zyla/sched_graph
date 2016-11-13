#!/usr/bin/env python
import math
import sys
import numpy
from PIL import Image, ImageDraw

procs = []

start = None
end = None

for f in sys.argv[1:]:
    proc_data = numpy.loadtxt(f, dtype=int) 
    procs.append(proc_data)

    off = 0
    raw = proc_data.reshape(-1)

    for i in range(1, len(raw)):
        p = raw[i-1]
        x = raw[i]
        x += off
        if x < p:
            print('WARP', p, x)
            x += 0x100000000
            off += 0x100000000
        raw[i] = x

    for ts in list(proc_data[0]) + list(proc_data[-1]):
        start = min(start, ts) if start else ts
        end = max(end, ts) if end else ts

proc_height = 30
padding = 100

def scale_time(time):
    return (time - start) / 100000 / 10

width = 1920

num_screens = int(math.ceil(scale_time(end)/width))
screen_height = len(procs)*proc_height + padding
height = screen_height * num_screens

print('start:', start, 'end:', end)
print('image size:', (width, height))

im = Image.new('RGB', (width, height), (255,255,255))
draw = ImageDraw.Draw(im)

proc_colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0), (255, 128, 128),
        (255, 255, 0), (200, 0, 255), (255, 0, 0),
        (0, 0, 64), (128, 255, 128), (129, 128, 255)]

for n in range(num_screens):
    y = padding/2 + n * screen_height
    draw.rectangle((0, y, width, y + len(procs)*proc_height), fill=(240,)*3)

start_yoffset = padding/2
for proc_no in range(len(procs)):
    proc = procs[proc_no]
    proc_color = proc_colors[proc_no]

    yoffset = start_yoffset
    xoff = 0

    for x1, x2 in proc:
        x1 = scale_time(x1) - xoff
        x2 = scale_time(x2) - xoff
        if x1 == x2:
            x2 += 1
        while x1 > width:
            x1 -= width
            x2 -= width
            xoff += width
            yoffset += screen_height

        draw.rectangle((x1, yoffset, min(width - 1, x2), yoffset + proc_height), fill=proc_color, outline=tuple(int(x/2) for x in proc_color))

        if x2 > width:
            xoff += width
            yoffset += screen_height

            draw.rectangle((0, yoffset, x2 - width, yoffset + proc_height), fill=proc_color)

    start_yoffset += proc_height

for n in range(num_screens):
    for m in range(len(procs) + 1):
        y = padding/2 + n * screen_height + m * proc_height
        draw.line((0, y, width, y), fill=(128,128,128))

im.save('lol.png')
