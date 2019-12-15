import sys
import time
import termcolor
from collections import defaultdict, namedtuple
import aoc
from aoc.intcode import Processor, Disassembler, Assembler, print_steps
import matplotlib.pyplot as plt
import escpos.printer


def inp_decode(x):
    def removecomment(x):
        if "#" in x:
            x, _ = x.split("#")
        return x

    return list(map(int, x.split(",")))


inp = aoc.get_input(inp_decode)
_logger = aoc.get_logger()

p = escpos.printer.Usb(0x04b8, 0x0202, 0, profile="TM-T88IV")
p.line_spacing(0)

class arcade(object):
    def __init__(self):
        self.grid = defaultdict(lambda: defaultdict(int))
        self.twos = 0
        self.ball = (0, 0)
        self.paddle = (0, 0)

    def reset(self):
        for r in self.grid.values():
            r.clear()

    def draw(self, x, y, w):
        if x == -1:
            self.points = w
            return
        self.grid[y][x] = w
        if w == 4:
            self.ball = x, y
            return
        if w == 3:
            self.paddle = x, y
            return
        if w == 0:
            if y in self.grid:
                if x in self.grid[y]:
                    del self.grid[y][x]
            return
        if w == 2:
            self.twos += 1

    def show(self):
        pstr = []
        printmap = {
            0: " ",
            1: '░',
            2: "█",
            3: '¯',
            4: '■'
        }
        for y in range(0, len(self.grid.keys())):
            lstr= []
            for x in range(0, len(self.grid[0].keys())):
                lstr.append(printmap[self.grid[y][x]])
            lstr.append('\n')
            pstr.append(''.join(lstr))
        pstr.append(' \n')
        pstr.append(f'Points: {self.points}')

        p.text(''.join(pstr[0:10]))
        time.sleep(0.25)
        p.text(''.join(pstr[10:]))
        p.text(' \n')
        pass

    def get_ball(self):
        return self.ball, self.paddle


f = lambda A, n=3: [A[i : i + n] for i in range(0, len(A), n)]

def part2intcode():
    pki = Processor()
    with open("data/prog.txt") as file:
        for line in file.readlines():
            pkinp = inp_decode(line.strip())
    pki.set_prog(pkinp)
    r = arcade()
    p = Processor()
    p.set_prog(inp)
    cnt = 1
    while not p.halt:
        p.run()
        outp = p.output
        kiin = list(f(outp))
        pki.add_input(len(kiin))
        for v in kiin:
            r.draw(*v)
            for vv in v:
                pki.add_input(vv)
        p.output.clear()
        pki.output.clear()
        pki.run()
        r.show()
        cnt+=1
        p.add_input(pki.output[-1])
        pki.output.clear()


def main():
    if aoc.part_one():
        return
        result = part1()
        print(f"Result: {result}")

    if aoc.part_two():
        result = part2intcode()
        print(f"Result: {result}")


if __name__ == "__main__":
    main()
