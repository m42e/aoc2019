from aoc.input import get_input
import sys
from aoc.partselector import part_one, part_two

def inp_decode(x):
    return list(map(int,x.split(',')))

inp = get_input(inp_decode)

class processor(object):

    def __init__(self, lst):
        self.olst = lst.copy()

    opcodes = {
        1: 'opcode1',
        2: 'opcode2',
        99: 'opcode_exit',
        'default': 'opcode_none',
    }
    def opcode1(self, index):
        pos = self.lst[index+3]
        self.lst[pos] = self.lst[self.lst[index+1]] + self.lst[self.lst[index+2]]
        return index + 4

    def opcode2(self, index):
        pos = self.lst[index+3]
        self.lst[pos] = self.lst[self.lst[index+1]] * self.lst[self.lst[index+2]]
        return index + 4

    def opcode_exit(self, index):
        self._processing = False

    def opcode_none(self, x):
        return x

    def process(self, verb, noun):
        self.lst = self.olst.copy()
        self._processing = True
        index = 0
        self.lst[1] = verb
        self.lst[2] = noun
        print(verb, noun)
        while self._processing:
            print(index, end=' ')
            index = getattr(self, self.opcodes[self.lst[index]])(index)
        print()
        return self.lst[0]

    def process_till(self, result):
        for i in range(0, len(self.olst)):
            for j in range(0, len(self.olst)):
                res = p.process(i, j)
                if res == result:
                    return 100*i+j



if part_one():
    p = processor(inp)
    result = p.process(12, 2)
    print('result')
    print(result)
    pass

if part_two():
    p = processor(inp)
    result = p.process_till(19690720)
    print('result 2')
    print(result)
    pass
