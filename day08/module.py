from aoc.input import get_input
from aoc.partselector import part_one, part_two
from collections import Counter

def inpfct(x):
    return list(map(int, list(x)))
inp = get_input(inpfct)

width=25
height=6
n = width*height

if part_one():
    cnt = 0
    layers = []
    layers = [inp[i:i+n] for i in range(0, len(inp), n)]
    lowest = 10000
    for i, l in enumerate(layers):
        c = Counter(l)
        lowest = min(c[0], lowest)
        if lowest == c[0]:
            result = c[1]*c[2]
            ind = i
    print(result)




    pass

if part_two():
    cnt = 0
    layer = [2] * n
    while cnt < len(inp):
        for y in range(0, height):
            for x in range(0, width):
                if layer[y*width+x] == 2:
                    layer[y*width+x] = inp[cnt]
                cnt += 1
    for y in range(0, height):
        for x in range(0, width):
            if layer[y*width+x] == 1:
                print('X', end='')
            else:
                print(' ', end='')
        print()
    pass
