import aoc
from collections import Counter

def inpfct(x):
    return list(map(int, list(x)))

inp = aoc.get_input(inpfct)

_logger = aoc.get_logger(__name__)

width=25
height=6
n = width*height

layers = [inp[i:i+n] for i in range(0, len(inp), n)]
if aoc.part_one():
    _logger.info('%s Layers found (size: %s x %s)', len(layers), width, height)
    clayers = sorted(list(map(Counter, layers)), key=lambda x: x[0])
    print(clayers[0][1]*clayers[0][2])

if aoc.part_two():
    print()
    cnt = 0
    layer = [2] * n
    for l in layers:
        for i, y in enumerate(l):
            if layer[i] == 2:
                layer[i] = y
    for y in range(0, height):
        for x in range(0, width):
            if layer[y*width+x] == 1:
                print('X', end='')
            else:
                print(' ', end='')
        print()
