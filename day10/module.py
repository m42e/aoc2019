import sys
import math
from collections import defaultdict
from aoc.input import get_input
from aoc.partselector import part_one, part_two, get_logger

def inp_decode(x):
    return list(x)

inp = get_input(inp_decode)
_logger = get_logger()

def visible(my_x,my_y,inp):
    rs = set()
    if inp[my_y][my_x] != '#':
        return 0
    for x in range(0, len(inp[0])):
        for y in range(0, len(inp)):
            if inp[y][x] == '#':
                if x == my_x:
                    if y == my_y:
                        continue
                    n = '-' if y<my_y else '+'
                    rs.add(f'x{n}')
                elif y == my_y:
                    if x == my_x:
                        continue
                    n = '-' if x<my_x else '+'
                    rs.add(f'y{n}')
                else:
                    res = (1.0*y - my_y)/(1.0*x - my_x)
                    n = '-' if y<my_y else '+'
                    rs.add(f'{n}{res}')
    print(my_x,my_y,len(rs))
    return len(rs)

def destroy(my_x,my_y,minp):
    inp = minp.copy()
    coords2 = []
    coords = defaultdict(lambda: defaultdict(lambda: 0))
    for x in range(0, len(inp[0])):
        for y in range(0, len(inp)):
            if inp[y][x] == '#':
                thex = x-my_x
                they = y-my_y
                r = math.sqrt(thex*thex +  they*they)
                if r == 0: 
                    continue
                if thex > 0:
                    phi = math.atan(they/thex)
                if thex < 0 and they >= 0:
                    phi = math.atan(they/thex) + math.pi
                if thex < 0 and they < 0:
                    phi = math.atan(they/thex) - math.pi
                if thex == 0 and they > 0:
                    phi = math.pi/2
                if thex == 0 and they < 0:
                    phi = -math.pi/2
                phi = (phi+math.pi+math.pi/2)%(2*math.pi) - math.pi
                coords2.append((phi, r, (x,y)))
                coords[phi][r] = (x,y)
    c2 = sorted(coords2, key= lambda x: x[0], reverse=True)
    print(c2)
    for i in range(0, 200):
        c2
    return c2[199][2]
    return len(coords)


def p1():
    results = {}
    m = 0
    for y, row in enumerate(inp):
        for x, col in enumerate(row):
            results[(x,y)] = visible(x,y,inp)
            m = max (m, results[(x,y)])
            if m == results[(x,y)]:
                print('----------', x, y)
    return m

def p2():
    return destroy(20,20,inp)
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
