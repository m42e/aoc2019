import sys
from collections import defaultdict
from aoc.input import get_input
from aoc.partselector import part_one, part_two, get_logger

def inp_decode(x):
    return list(x)

inp = get_input(inp_decode)
_logger = get_logger()

def p1():
    for y, row in enumerate(inp):
        for x, col in enumerate(row):
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
