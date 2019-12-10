import sys
from collections import defaultdict
from aoc.input import get_input
from aoc.partselector import part_one, part_two, get_logger

def inp_decode(x):
    return list(x)

inp = get_input(inp_decode)
_logger = get_logger()

def visible(my_x,my_y,inp):
    checkpoints = []
    for x in range(0, len(inp[0])):
        checkpoints.append((x, 0))
        checkpoints.append((x, len(inp)-1))
    for y in range(0, len(inp)):
        checkpoints.append((0, y))
        checkpoints.append((len(inp[0])-1, y))
    if (my_x, my_y) in checkpoints:
        checkpoints.remove((my_x, my_y))

    for cp in checkpoints:
        count = 0
        if (cp[0] - my_x) == 0:
            continue
        r = (1.0*cp[1] - my_y)/(cp[0] - my_x)
        for cur_x in range(0, len(inp[1])):
            cur_y = cur_x * r
            if cur_y.is_integer():
                count += 1
                break
                print(cur_x, int(cur_y))
    print(count)


def p1():
    results = {}
    for y, row in enumerate(inp):
        for x, col in enumerate(row):
            results[(x,y)] = visible(x,y,inp)
            print (x,y, col)
    return None

def p2():
    return None

def main():
    if part_one():
        result = p1()
        print(f'Result: {result}')

    if part_two():
        result = p2()
        print(f'Result: {result}')

if __name__ == "__main__":
    main()
