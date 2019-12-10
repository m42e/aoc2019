import sys
import time
import math
from collections import defaultdict
from aoc.input import get_input
from aoc.partselector import part_one, part_two, get_logger

def inp_decode(x):
    return list(x)

inp = get_input(inp_decode)
#inp = list(map(list, zip(*inp)))
_logger = get_logger()

def visible(my_x,my_y,inp):
    # Use a set to store the factor and the upper or lower half of the coordinate system
    rs = set()
    if inp[my_y][my_x] != '#':
        return 0
    for x in range(0, len(inp[0])):
        for y in range(0, len(inp)):
            if inp[y][x] == '#':
                n = '-' if y<my_y else '+'
                if x == my_x and y == my_y:
                    continue
                elif x == my_x:
                    rs.add(f'x{n}')
                elif y == my_y:
                    rs.add(f'y{n}')
                else:
                    res = (1.0*y - my_y)/(1.0*x - my_x)
                    rs.add(f'{n}{res}')
    return len(rs)

def print_grid(inp):
    print(chr(27)+'[2j')
    print('\033c')
    print('\x1bc')
    cnt = 0
    for y in range(0, len(inp)):
        for x in range(0, len(inp[0])):
            v = inp[y][x]
            if v == '.':
                print(' ', end = '')
            elif v == 'x':
                print('.', end = '')
            else:
                print(v, end = '')
                cnt += 1

        print()
    print(cnt)

count = 0
result = None
def destroy(my_x,my_y,minp):
    inp = minp.copy()
    inp[my_y][my_x] = '0'
    coords = defaultdict(lambda: {})
    for x in range(0, len(inp[0])):
        for y in range(0, len(inp)):
            if inp[y][x] == '#':
                thex = x-my_x
                they = y-my_y
                r = math.sqrt(thex*thex +  they*they)
                if r == 0:
                    continue
                if they >= 0:
                    phi = math.acos(thex/r)
                if they < 0:
                    phi = math.pi*2-math.acos(thex/r)
                phi = phi+math.pi/2
                if phi >= math.pi*2:
                    phi = phi - math.pi *2
                if phi < 0:
                    phi = phi + math.pi *2
                phi = round(phi, 8)
                coords[phi][r] = (x,y)
    angles = sorted(coords.keys())
    dists = set()
    for i in coords.values():
        for d in i.keys():
            dists.add(d)
    dists = sorted(dists)
    result = None
    results = []
    print_grid(inp)
    while result is None:
        for a in angles:
            def inner():
                global count
                for d in dists:
                    if d in coords[a]:
                        count += 1
                        if count in [1, 2, 3, 10, 20, 50, 100, 199, 200]:
                            results.append(coords[a][d])
                        if count == 200:
                            result = coords[a][d]
                            inp[coords[a][d][1]][coords[a][d][0]] = 'C'
                            print_grid(inp)
                            print(sum(map(len, coords.values())), count)
                            print(results)
                            return result
                        inp[coords[a][d][1]][coords[a][d][0]] = 'x'
                        print_grid(inp)
                        print(sum(map(len, coords.values())), count)
                        print(results)
                        del coords[a][d]
                        time.sleep(0.01525)
                        return
            result = inner()
            if result is not None:
                return result
    return 0


def p1():
    maxp = (0,0)
    results = {}
    m = 0
    for y, row in enumerate(inp):
        for x, col in enumerate(row):
            results[(x,y)] = visible(x,y,inp)
            m = max (m, results[(x,y)])
            if m == results[(x,y)]:
                maxp = (x,y)
    return m, maxp

def p2(result):
    return destroy(*result,inp)
    return None

def main():
    result, maxp = p1()
    if part_one():
        print(f'Result: {result}')
        print(maxp)

    if part_two():
        result = p2(maxp)
        print(f'Result: {result}')

if __name__ == "__main__":
    main()
