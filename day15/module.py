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

def read_single_keypress():
    import termios, fcntl, sys, os
    fd = sys.stdin.fileno()
    # save old state
    flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
    attrs_save = termios.tcgetattr(fd)
    # make raw - the way to do this comes from the termios(3) man page.
    attrs = list(attrs_save) # copy the stored version to update
    # iflag
    attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK
                  | termios.ISTRIP | termios.INLCR | termios. IGNCR
                  | termios.ICRNL | termios.IXON )
    # oflag
    attrs[1] &= ~termios.OPOST
    # cflag
    attrs[2] &= ~(termios.CSIZE | termios. PARENB)
    attrs[2] |= termios.CS8
    # lflag
    attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                  | termios.ISIG | termios.IEXTEN)
    termios.tcsetattr(fd, termios.TCSANOW, attrs)
    # turn off non-blocking
    fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
    # read a single keystroke
    ret = []
    try:
        ret.append(sys.stdin.read(1)) # returns a single character
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save | os.O_NONBLOCK)
        c = sys.stdin.read(1) # returns a single character
        while len(c) > 0:
            ret.append(c)
            c = sys.stdin.read(1)
    except KeyboardInterrupt:
        ret.append('\x03')
    finally:
        # restore old state
        termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
    return tuple(ret)

class Droid(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.grid = defaultdict(dict)
        self.grid[0][0] = 1
        self.dirs = [(0,0), (0,-1), (0, 1), (1, 0), (-1,0)]

        if aoc.draw():
            import curses

            self.stdscr = curses.initscr()
            self.stdscr.clear()
            self.stdscr.addstr(0, 0, "^")

    def move(self, direction, result):
        self.grid[self.y + self.dirs[direction][1]][self.x + self.dirs[direction][0]] = result
        if result == 1 or result == 2:
            self.x += self.dirs[direction][0]
            self.y += self.dirs[direction][1]

    def test(self, direction):
        if (self.y + self.dirs[direction][1]) in self.grid:
            if (self.x + self.dirs[direction][0]) in self.grid[(self.y + self.dirs[direction][1])]:
                return self.grid[(self.y + self.dirs[direction][1])][(self.x + self.dirs[direction][0])]
        return None

    def draw(self):
        if not aoc.draw():
            return
        offset_y = -min(self.grid.keys())
        offset_x = -min(map(lambda x: min(x.keys()), self.grid.values()))
        max_y = max(self.grid.keys())
        max_x = max(map(lambda x: max(x.keys()), self.grid.values()))
        draw = ['#', '.', 'O']
        self.stdscr.clear()
        for y in range(-offset_y, max_y):
            for x in range(-offset_x, max_x):
                self.stdscr.addstr(offset_y + y, offset_x + x, "_")
        for y in self.grid.keys():
            for x in self.grid[y].keys():
                self.stdscr.addstr(offset_y + y, offset_x + x, draw[self.grid[y][x]])
        self.stdscr.addstr(self.y+offset_y, self.x+offset_x, 'D')
        self.stdscr.refresh()

def manu():
    p = Processor()
    p.set_prog(inp)
    d = Droid()
    while not p.halt:
        goto = read_single_keypress()
        if goto[0] == 'x':
            break
        if goto[0] != '\x1b':
            print('not accepted')
            continue
        goto = ord(goto[2])-ord('A') + 1
        p.add_input(goto)
        p.run()
        d.move(goto, p.output[0])
        p.output.clear()
        reverse = [0, 2, 1, 4, 3]
        for dire in [1,2,3,4]:
            p.add_input(dire)
            p.run()
            d.move(dire, p.output[0])
            if p.output[0] == 1:
                p.output.clear()
                p.add_input(reverse[dire])
                p.run()
                d.move(reverse[dire], p.output[0])
            p.output.clear()
        #print(d.x, d.y, p.output[0])
        d.draw()
        p.output.clear()

    return None

def p1():
    p = Processor()
    p.set_prog(inp)
    moves = [(None, None), (0, -1), (0, 1), (-1, 0), (1, 0)]
    reverse = [0, 2, 1, 4, 3]
    pos = (0, 0)
    queue = [(pos, [], 0)]
    visited = set([pos])
    isEmpty = set([pos])
    hasOxygen = set()
    d = Droid()
    while queue:
        cur, btpath, lenpath = queue.pop()

        for pth in btpath:
            p.add_input(pth)
            p.run()
            assert(p.output[-1] == 1)
            d.move(pth, p.output[-1])

        for i in range(1, 5):
            npos = (cur[0]+moves[i][0], cur[1]+moves[i][1])
            nbtpath = btpath + [i]
            nlenpath = lenpath+1
            if npos not in visited:
                visited.add(npos)
                p.add_input(i)
                p.run()
                out = p.output[-1]
                d.move(i, p.output[-1])
                d.draw()
                if out == 1:
                    isEmpty.add(npos)
                    queue.append((npos, nbtpath, nlenpath))
                    p.add_input(reverse[i])
                    p.run()
                    d.move(reverse[i], p.output[-1])
                    assert(p.output[-1] == 1)
                elif out == 2:
                    hasOxygen.add(npos)
                    print(isEmpty)
                    print(hasOxygen)
                    print(lenpath+1)
                    exit()

        for pth in btpath[::-1]:
            p.add_input(reverse[pth])
            p.run()
            d.move(reverse[pth], p.output[-1])
            assert(p.output[-1] == 1)

class oxy(object):
    def __init__(self, plan, x, y):
        self.plan = plan
        self.x = x
        self.y = y

    def flood(self):
        set_this_round = {}
        count = 0
        for y, xrow in self.plan.items():
            for x in xrow:
                if f'{y}_{x}' in set_this_round:
                    continue
                if self.plan[y][x] == 'O':
                    y1 = 0
                    for x1 in range(-1, 2, 2):
                        #print(y, x, y+y1, x+x1, self.plan[y+y1][x+x1])
                        if self.plan[y+y1][x+x1] == '.':
                            self.plan[y+y1][x+x1] = 'O'
                            set_this_round[f'{y+y1}_{x+x1}'] = 1
                            count -= 1
                    x1 = 0
                    for y1 in range(-1, 2, 2):
                        #print(y, x, y+y1, x+x1, self.plan[y+y1][x+x1])
                        if self.plan[y+y1][x+x1] == '.':
                            self.plan[y+y1][x+x1] = 'O'
                            set_this_round[f'{y+y1}_{x+x1}'] = 1
                            count -= 1
                if self.plan[y][x] == '.':
                    count += 1
        return count


def p2():
    grid = defaultdict(dict)
    ox = 0
    oy = 0
    with open('plan.txt') as p:
        for y, line in enumerate(p.readlines()):
            for x, c in enumerate(line.strip()):
                grid[y][x] = c
                if c == 'O':
                    ox = x
                    oy = y
    print('\n'.join(map(lambda x: ''.join(x.values()), grid.values())))
    o = oxy(grid, ox, oy)
    count = 0
    while o.flood() > 0:
        print('\n'.join(map(lambda x: ''.join(x.values()), grid.values())))
        count += 1
    print(o.flood())
    print('\n'.join(map(lambda x: ''.join(x.values()), grid.values())))
    return count


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
