import sys
from aoc.input import get_input
from aoc.partselector import part_one, part_two
import itertools
import logging

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

def inp_decode(x):
    return list(map(int,x.split(',')))

inp = get_input(inp_decode)

class processor(object):

    def __init__(self, lst, tinput):
        self.olst = lst.copy()
        self.olst += [0 for x in range (0, 100)]
        self.tinput = tinput
        self.tinput_pos = 0
        self.currentindex = 0
        self.output = []
        self._processing = True

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

    def get_param(self, index, opcode, param):
        val = self.lst[index+param]
        if opcode%100 == 3 and param == 1:
            return val
        if (opcode // pow(10, param+1)) % 10 == 0 and param != 3:
            return self.lst[val]
        else:
            return val

    def opcode1(self, index):
        opcode = self.lst[index] % 10000
        pos = self.get_param(index, opcode, 3)
        p1 = self.get_param(index, opcode, 1)
        p2 = self.get_param(index, opcode, 2)
        _logger.debug('%s: %s = %s', opcode, index, self.get_param(index, opcode, 1))
        _logger.debug('%s: %s = %s', opcode, index, self.get_param(index, opcode, 2))
        res = self.get_param(index, opcode, 1) + self.get_param(index, opcode, 2)
        self.lst[pos] = res
        return index + 4

    def opcode2(self, index):
        opcode = self.lst[index] % 10000
        pos = self.get_param(index, opcode, 3)
        self.lst[pos] = self.get_param(index, opcode, 1) * self.get_param(index, opcode, 2)
        return index + 4

    def opcode3(self, index):
        opcode = self.lst[index]
        pos = self.get_param(index, opcode, 1)
        if self.tinput_pos == len(self.tinput):
            return index
        if isinstance(self.tinput, list):
            _logger.debug('%s: %s', pos, self.tinput[self.tinput_pos])
            self.lst[pos] = self.tinput[self.tinput_pos]
            self.tinput_pos += 1
        else:
            self.lst[pos] = self.tinput
        return index + 2

    def opcode4(self, index):
        opcode = self.lst[index]
        pos = self.get_param(index, opcode, 1)
        self.output.append(pos)
        _logger.debug('output: %s', pos)
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
        pos = self.get_param(index, opcode, 3)
        self.lst[pos] = 1 if self.get_param(index, opcode, 1) < self.get_param(index, opcode, 2) else 0
        return index + 4

    def opcode8(self, index):
        opcode = self.lst[index] % 10000
        pos = self.get_param(index, opcode, 3)
        self.lst[pos] = 1 if self.get_param(index, opcode, 1) == self.get_param(index, opcode, 2) else 0
        return index + 4

    def opcode_exit(self, index):
        self._processing = False

    def opcode_none(self, x):
        return x

    @property
    def finished(self):
        return not self._processing

    def process(self, inp=None):
        self.output = []
        self.lst = self.olst.copy()
        if inp is not None:
            self.tinput.append(inp)
        while self._processing:
            index = getattr(self, self.opcodes[self.lst[self.currentindex]%100])(self.currentindex)
            if index == self.currentindex:
                break
            self.currentindex = index



if part_one():
    max_ = 0
    in_ = 0
    for x in itertools.permutations([0, 1, 2, 3, 4], 5):
        in_ = 0
        for s in x:
            p = processor(inp, [s, in_])
            p.process()
            in_ = p.output[-1]
        print('result')
        print(p.output)
        max_ = max(max_, p.output[-1])
        pass
    print(max_)

if part_two():
    max_ = 0
    in_ = 0
    for x in itertools.permutations([5, 6, 7, 8, 9], 5):
        in_ = 0
        ps = []
        for s in x:
            ps.append(processor(inp, [s]))
        pos = 0
        while(any(map(lambda x: not x.finished, ps))):
            ps[pos%5].process(in_)
            in_ = ps[pos%5].output[-1]
            pos += 1
        max_ = max(max_, ps[4].output[-1])
        pass
    print(max_)
