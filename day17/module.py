import sys
import time
import random
from collections import defaultdict
import aoc
from aoc.input import get_input
from aoc.partselector import part_one, part_two, get_logger
from aoc.intcode import Processor, Disassembler, Assembler, print_steps, generate_jump_graph

def inp_decode(x):
    return list(map(int, x.split(",")))

inp = get_input(inp_decode)
_logger = get_logger()



def p1():
    p = Processor(False)
    p.set_prog(inp)
    p.run()

    grid = (''.join(map(chr, p.output))).split('\n')
    sum = 0
    cnt = 0
    for x in range(1,len(grid)-3):
        for y in range(1,len(grid[x])-1):
            if grid[x][y-1] == '#' and grid[x][y] == '#' and grid[x+1][y] == '#' and grid[x-1][y] == '#' and grid[x][y+1] == '#':
                cnt += 1
                sum += x*y
    print(cnt)
    return sum

def p2():
    p = Processor(False)
    p.set_prog(inp)
    p.run()

    dirs = ['^',  '<', 'v','>']
    dirs_cnt = [(-1, 0),  (0, -1), (1, 0),(0, 1)]

    grid = (''.join(map(chr, p.output))).split('\n')
    print('\n'.join(grid))
    for x in range(0,len(grid)):
        for y in range(0,len(grid[x])):
            if grid[x][y] in ['^',  '<', 'v','>']:
                pos = (x,y)
                direction = dirs.index(grid[x][y])
    cont = True
    queue = [(pos, [], 0)]
    visited = set([pos])
    while queue:
        cur, btpath, lenpath = queue.pop()
        for d in range(0, 4):
            newx = cur[0] + dirs_cnt[d][0]
            newy = cur[1] + dirs_cnt[d][1]
            npos = (newx, newy)
            if newx >= 48 or newy>=50 or newx < 0 or newy < 0:
                continue
            if npos in visited:
                continue
            visited.add(npos)
            if grid[newx][newy] != '#':
                continue
            queue.append(((newx, newy), btpath + [cur], lenpath+1))
            path = btpath +[cur]

    last = path[0]

    return pos, direction

    
    p = Processor(False)
    inp[0] = 2
    p.set_prog(inp)
    p.run()

    grid = (''.join(map(chr, p.output))).split('\n')
    sum = 0
    cnt = 0
    for x in range(1,len(grid)-3):
        for y in range(1,len(grid[x])-1):
            if grid[x][y-1] == '#' and grid[x][y] == '#' and grid[x+1][y] == '#' and grid[x-1][y] == '#' and grid[x][y+1] == '#':
                cnt += 1
                sum += x*y
    print(cnt)
    return sum

def main():
    if part_one():
        result = p1()
        print(f'Result: {result}')

    if part_two():
        result = p2()
        print(f'Result: {result}')

    if aoc.draw():
        import curses
        curses.endwin()

if __name__ == "__main__":
    main()
