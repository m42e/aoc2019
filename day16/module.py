import sys
from collections import defaultdict
from aoc.partselector import part_one, part_two, get_logger
import aoc

def inp_decode(x):
    return str(x)

inp = aoc.get_input(inp_decode)
_logger = get_logger()


def mult(inpt, pattern):
    inpt = list(inpt)
    absout = []
    for n in range(1, len(inpt)+1):
        indx = 1
        outp = {}
        rpattern = []
        for p in pattern:
            for i in range(0, n):
                rpattern.append(p)

        for z in range(0, len(inpt)):
            res = int(inpt[z])*rpattern[indx]
            outp[z] = res
            indx = (indx+1)%len(rpattern)
        absout.append(abs(sum(outp.values()))%10)
    return absout

def p1():
    i = inp
    print (inp)
    for x in range(0, 100):
         i = mult(i, [0, 1,0,-1])
         print(''.join(map(str, i)))
    return None

def p2():
    i = 10000*inp
    print(int(i[0:7]))
    ii = i[int(i[0:7]):]
    new = list(map(int, ii))
    for x in range(100):
        for x in range(len(new)-2, -1, -1):
            new[x] = (new[x] + new[x+1]) % 10
    return ''.join(map(str, new[0:8]))

def main():
    if part_one():
        result = p1()
        print(f'Result: {result}')

    if part_two():
        result = p2()
        print(f'Result: {result}')

if __name__ == "__main__":
    main()
