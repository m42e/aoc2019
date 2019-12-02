from aoc.input import get_input
import sys
from aoc.partselector import part_one, part_two

def inp_decode(x):
    return list(map(int,x.split(',')))

inp = get_input(inp_decode)

def opcode1(index):
    print(index)
    print(inp)
    pos = inp[index+3]
    print(inp[inp[index+1]])
    print(inp[inp[index+2]])
    inp[pos] = inp[inp[index+1]] + inp[inp[index+2]]
    return index + 4

def opcode2(index):
    print(index)
    print(inp)
    pos = inp[index+3]
    inp[pos] = inp[inp[index+1]] * inp[inp[index+2]]
    return index + 4

def opcode_exit(index):
    print(inp)
    sys.exit()

def opcode_none(x):
    print(x)
    print(inp)
    sys.exit()
    return x

opcodes = [
    opcode_none,
    opcode1,
    opcode2,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_none,
    opcode_exit
]

if part_one():
    index = 0
    while True:
        index = opcodes[inp[index]](index)
    pass

if part_two():
    pass
