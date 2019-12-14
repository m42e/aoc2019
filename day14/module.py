import sys
from collections import defaultdict
from aoc.input import get_input
from aoc.partselector import part_one, part_two, get_logger


def inp_decode(x):
    in_, out_ = map(str.strip, x.split("=>"))
    in_ = list(map(lambda x: tuple(x.split(" ")), map(str.strip, in_.split(","))))
    out_ = tuple(out_.split(" "))
    return (in_, out_)


inp = get_input(inp_decode)
_logger = get_logger()

reactions = {}
for reaction in inp:
    a, r = reaction[1]
    reactions[r] = reaction


def calculate(nr):
    needed = {"FUEL": nr}
    available = {}
    while len(needed) != 1 or not "ORE" in needed:
        cneeded = needed.copy()
        todel = []
        needednow = {}
        for n in cneeded:
            if n == "ORE":
                continue
            start = reactions[n]
            if n in available:
                needed[n] -= available[n]
                available[n] -= available[n]
            needednow[n] = needed[n]
        fac = {}
        for n in needednow:
            start = reactions[n]
            producable = int(start[1][0])
            if needed[n] <= producable:
                fac[n] = 1
            else:
                fac[n] = needednow[n] // producable
                if needednow[n] % producable != 0:
                    fac[n] += 1
        for n in needednow:
            start = reactions[n]
            for elem in start[0]:
                amount = int(elem[0]) * fac[n]
                if elem[1] in needed:
                    needed[elem[1]] += amount
                else:
                    needed[elem[1]] = amount
                amount - needed[n]
            needed[n] -= int(start[1][0]) * fac[n]
            if needed[n] < 0:
                needed[n] = 0
            else:
                needed[n] = needed[n]

        for d in list(needed.keys()):
            if needed[d] == 0:
                del needed[d]
    return needed["ORE"]


def p1():
    return calculate(1)


def p2():
    nr = 1
    step = 100000
    while step > 0:
        while calculate(nr) < 1000000000000:
            nr += step
        nr -= step
        step = step // 10
    return nr


def main():
    if part_one():
        result = p1()
        print(f"Result: {result}")

    if part_two():
        result = p2()
        print(f"Result: {result}")


if __name__ == "__main__":
    main()
