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
    coords2 = []
    inp[my_y][my_x] = '0'
    coords = defaultdict(lambda: defaultdict(lambda: 0))
    for x in range(0, len(inp[0])):
        for y in range(0, len(inp)):
            if inp[y][x] == '#':
                thex = x-my_x
                they = y-my_y
                r = math.sqrt(thex*thex +  they*they)
                if r == 0: 
                    continue
                if False:
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
                    phi = phi+math.pi
                if they >= 0:
                    phi = math.acos(thex/r)
                if they < 0:
                    phi = math.pi*2-math.acos(thex/r)
                phi = phi+math.pi/2
                if phi >= math.pi*2:
                    phi = phi - math.pi *2
                if phi < 0:
                    phi = phi + math.pi *2
                coords2.append((phi, r, (x,y)))
                coords[phi][r] = (x,y)
    c2 = sorted(coords2, key= lambda x: x[1])
    angles = sorted(coords.keys())
    dists = set()
    for i in coords.values():
        for d in i.keys():
            dists.add(d)
    dists = sorted(dists)
    result = None
    results = []
    while result is None:
        for a in angles:
            def inner():
                global count
                for d in dists:
                    if d in coords[a]:
                        count += 1
                        if count in [1, 2, 3, 10, 20, 50, 100, 199]:
                            results.append(coords[a][d])
                        if count == 200:
                            result = coords[a][d]
                            inp[coords[a][d][1]][coords[a][d][0]] = 'C'
                            print_grid(inp)
                            print(results)
                            return result
                        inp[coords[a][d][1]][coords[a][d][0]] = 'x'
                        print_grid(inp)
                        print(results)
                        del coords[a][d]
                        time.sleep(0.125)
                        return
            result = inner()
            if result is not None:
                return result
    return 0


maxp = (0,0)
def p1():
    global maxp
    results = {}
    m = 0
    for y, row in enumerate(inp):
        for x, col in enumerate(row):
            results[(x,y)] = visible(x,y,inp)
            m = max (m, results[(x,y)])
            if m == results[(x,y)]:
                maxp = (x,y)
                print('----------', x, y)
    return m

def p2(result):
    return destroy(*result,inp)
    return None

def main():
    if part_one():
        result = p1()
        print(f'Result: {result}')
        print(maxp)

    if part_two():
        result = p2(maxp)
        print(f'Result: {result}')

if __name__ == "__main__":
    main()
