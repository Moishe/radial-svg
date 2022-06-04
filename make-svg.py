import math
import os
import svgwrite
from svgwrite import cm, mm

layers = [
    {
        'steps': 256,
        'circles': [
            {
                'radius': 90,
                'speed': 1.0,
                'offset': math.pi,
                'epicycle': {
                    'radius': 3,
                    'speed': 12,
                    'offset': 0
                }
            },
            {
                'radius': 70,
                'speed': 1.0,
                'offset': math.pi,
                'epicycle': {
                    'radius': 20,
                    'speed': 9,
                    'offset': 0
                }
            },
        ]
    },
    {
        'steps': 256,
        'circles': [
            {
                'radius': 70,
                'speed': 1.0,
                'offset': math.pi,
                'epicycle': {
                    'radius': 20,
                    'speed': 9,
                    'offset': 0
                }
            },
            {
                'radius': 50,
                'speed': 1.0,
                'offset': math.pi,
                'epicycle': {
                    'radius': 5,
                    'speed': 4,
                    'offset': 0
                }
            },
        ]
    },
    {
        'steps': 256,
        'circles': [
            {
                'radius': 50,
                'speed': 1.0,
                'offset': math.pi,
                'epicycle': {
                    'radius': 5,
                    'speed': 4,
                    'offset': 0
                }
            },
            {
                'radius': 30,
                'speed': 1.0,
                'offset': math.pi,
                'epicycle': {
                    'radius': 3,
                    'speed': 11,
                    'offset': 0
                }
            },
        ]
    },
    {
        'steps': 128,
        'circles': [
            {
                'radius': 30,
                'speed': 1.0,
                'offset': math.pi,
                'epicycle': {
                    'radius': 3,
                    'speed': 11,
                    'offset': 0
                }
            },
            {
                'radius': 5,
                'speed': -2.0,
                'offset': math.pi,
                'epicycle': {
                    'radius': 0,
                    'speed': 0,
                    'offset': 0
                }
            },
        ]
    }
]

def get_xy(c, ratio, oxy):
    sub_t = math.pi * 2 * ratio * c['speed'] + c['offset']
    x = (math.cos(sub_t) * c['radius'] + oxy[0])
    y = (math.sin(sub_t) * c['radius'] + oxy[1])
    if 'epicycle' in c:
        (x, y) = get_xy(c['epicycle'], ratio, (x, y))
    return (x, y)

def make_svg(dir, filename):
    prev_x = None
    prev_y = None
    for (idx, layer) in enumerate(layers):
        print("Processing circle %d" % idx)
        layer_filename = "%s/%s-%d.svg" % (dir, filename, idx)
        dwg = svgwrite.Drawing(filename=layer_filename, debug=True, height='210mm', width='297mm')
        lines = dwg.add(dwg.g(id='lines', stroke='black', stroke_width='0.1'))

        steps = layer['steps']
        for t in range(0, steps):
            ratio = t / steps
            for c in layer['circles']:
                (x, y) = get_xy(c, ratio, (105, 148))

                if prev_x and prev_y:
                    lines.add(dwg.line(start=(prev_x * mm, prev_y * mm), end=(x * mm, y * mm)))

                prev_x = x
                prev_y = y

        dwg.save()
        print("vpype processing")
        new_filename = "%s/proc-%s-%d.svg" % (dir, filename, idx)
        os.system("vpype read %s linemerge reloop linesort write %s" % (layer_filename, new_filename))

if __name__ == "__main__":
    make_svg('output', 'test-flower')
