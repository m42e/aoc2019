import sys
from aoc.input import get_input
from aoc.partselector import part_one, part_two

def inp_decode(x):
    return list(map(int,x.split(',')))

inp = get_input(inp_decode)

class processor(object):

    def __init__(self, lst, tinput):
        self.olst = lst.copy()
        self.olst += [0 for x in range (0, 100)]
        self.tinput = tinput

    opcodes = {
        1: 'opcode1',
        2: 'opcode2',
        3: 'opcode3',
        4: 'opcode4',
        5: 'opcode5',
        6: 'opcode6',
        7: 'opcode7',
        8: 'opcode8',
        99: 'opcode_exit',
        'default': 'opcode_none',
    }

    def get_param(self, index, opcode, param, force_positional=False):
        val = self.lst[index+param]
        if force_positional or ((opcode // pow(10, param+1)) % 10 == 1):
            return val
        return self.lst[val]

    def opcode1(self, index):
        opcode = self.lst[index] % 10000
        pos = self.get_param(index, opcode, 3, force_positional=True)
        p1 = self.get_param(index, opcode, 1)
        p2 = self.get_param(index, opcode, 2)
        res = self.get_param(index, opcode, 1) + self.get_param(index, opcode, 2)
        self.lst[pos] = res
        return index + 4

    def opcode2(self, index):
        opcode = self.lst[index] % 10000
        pos = self.get_param(index, opcode, 3, force_positional=True)
        self.lst[pos] = self.get_param(index, opcode, 1) * self.get_param(index, opcode, 2)
        return index + 4

    def opcode3(self, index):
        opcode = self.lst[index]
        pos = self.get_param(index, opcode, 1, force_positional=True)
        self.lst[pos] = self.tinput
        return index + 2

    def opcode4(self, index):
        opcode = self.lst[index]
        pos = self.get_param(index, opcode, 1)
        self.output.append(pos)
        return index + 2

    def opcode5(self, index):
        opcode = self.lst[index]
        p1 = self.get_param(index, opcode, 1)
        p2 = self.get_param(index, opcode, 2)
        if p1 > 0:
            return p2
        return index + 3

    def opcode6(self, index):
        opcode = self.lst[index]
        p1 = self.get_param(index, opcode, 1)
        p2 = self.get_param(index, opcode, 2)
        if p1 == 0:
            return p2
        return index + 3

    def opcode7(self, index):
        opcode = self.lst[index] % 10000
        pos = self.get_param(index, opcode, 3, force_positional=True)
        self.lst[pos] = 1 if self.get_param(index, opcode, 1) < self.get_param(index, opcode, 2) else 0
        return index + 4

    def opcode8(self, index):
        opcode = self.lst[index] % 10000
        pos = self.get_param(index, opcode, 3, force_positional=True)
        self.lst[pos] = 1 if self.get_param(index, opcode, 1) == self.get_param(index, opcode, 2) else 0
        return index + 4

    def opcode_exit(self, index):
        self._processing = False

    def opcode_none(self, x):
        return x

    def process(self, verb, noun):
        self.output = []
        self.lst = self.olst.copy()
        self._processing = True
        index = 0
        while self._processing:
            index = getattr(self, self.opcodes[self.lst[index]%100])(index)
        return self.lst[0]

    def process_till(self, result):
        for i in range(0, len(self.olst)):
            for j in range(0, len(self.olst)):
                res = p.process(i, j)
                if res == result:
                    return 100*i+j



if part_one():
    p = processor(inp, 1)
    result = p.process(12, 2)
    print(p.output)

if part_two():
    p = processor(inp, 5)
    result = p.process(1,19690720)
    print(p.output)
