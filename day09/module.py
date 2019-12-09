import sys
from collections import defaultdict
from aoc.input import get_input
from aoc.partselector import part_one, part_two, get_logger

def inp_decode(x):
    return list(map(int,x.split(',')))

inp = get_input(inp_decode)
_logger = get_logger()

class processor(object):

    def __init__(self, lst, tinput):
        self.olst = defaultdict(lambda: 0)
        for i, f in enumerate(lst):
            self.olst[i] = f
        self.tinput = tinput
        self.tinput_pos = 0
        self.currentindex = 0
        self.output = []
        self._processing = True
        self.relativebase = 0

    opcodes = {
        1: 'opcode1',
        2: 'opcode2',
        3: 'opcode3',
        4: 'opcode4',
        5: 'opcode5',
        6: 'opcode6',
        7: 'opcode7',
        8: 'opcode8',
        9: 'opcode9',
        99: 'opcode_exit',
        'default': 'opcode_none',
    }

    def get_param(self, index, opcode, param, force_positional=False):
        val = self.lst[index+param]
        encoding = ((opcode // pow(10, param+1)) % 10)
        print(encoding)
        if encoding == 2:
            if force_positional:
                _logger.debug('read:  % 5s [relative %s]', self.relativebase + val, force_positional)
                return self.relativebase + val
            _logger.debug('read:  % 5s: % 15s [relative %s]', self.relativebase + val, self.lst[self.relativebase + val], force_positional)
            return self.lst[self.relativebase + val]
        if force_positional or encoding == 1:
            _logger.debug('read:  % 5s: % 15s', 'immed', val)
            return val
        _logger.debug('read:  % 5s: % 15s', val, self.lst[val])
        return self.lst[val]

    def opcode1(self, index):
        opcode = self.lst[index] 
        pos = self.get_param(index, opcode, 3, force_positional=True)
        p1 = self.get_param(index, opcode, 1)
        p2 = self.get_param(index, opcode, 2)
        res = p1+p2
        print (pos)
        _logger.info('add: % 5s: % 10s + % 10s = % 15s', index, p1, p2, res)
        _logger.debug('store: % 5s: % 15s', pos, res)
        self.lst[pos] = res
        return index + 4

    def opcode2(self, index):
        opcode = self.lst[index] 
        pos = self.get_param(index, opcode, 3, force_positional=True)
        p1 = self.get_param(index, opcode, 1)
        p2 = self.get_param(index, opcode, 2)
        res = p1*p2
        _logger.info('mul: % 5s: % 10s * % 10s = % 15s', index, p1, p2, res)
        _logger.debug('store: % 5s: % 15s', pos, res)
        self.lst[pos] =  res
        return index + 4

    def opcode3(self, index):
        opcode = self.lst[index]
        pos = self.get_param(index, opcode, 1, force_positional=True)
        if self.tinput_pos == len(self.tinput):
            _logger.debug('read, no input available')
            return index
        if isinstance(self.tinput, list):
            _logger.debug('store: % 5s: % 15s', pos, self.tinput[self.tinput_pos])
            self.lst[pos] = self.tinput[self.tinput_pos]
            self.tinput_pos += 1
        else:
            _logger.debug('store: % 5s: % 15s', pos, self.tinput)
            self.lst[pos] = self.tinput
        return index + 2

    def opcode4(self, index):
        opcode = self.lst[index]
        pos = self.get_param(index, opcode, 1)
        _logger.debug('output: %s', pos)
        self.output.append(pos)
        return index + 2

    def opcode5(self, index):
        opcode = self.lst[index]
        p1 = self.get_param(index, opcode, 1)
        p2 = self.get_param(index, opcode, 2)
        if p1 > 0:
            _logger.info('got: % 5s: yes', p2)
            return p2
        _logger.info('got: % 5s: no', p2)
        return index + 3

    def opcode6(self, index):
        opcode = self.lst[index]
        p1 = self.get_param(index, opcode, 1)
        p2 = self.get_param(index, opcode, 2)
        if p1 == 0:
            _logger.info('got: % 5s: yes', p2)
            return p2
        _logger.info('got: % 5s: no', p2)
        return index + 3

    def opcode7(self, index):
        opcode = self.lst[index]
        pos = self.get_param(index, opcode, 3, force_positional=True)
        p1 =self.get_param(index, opcode, 1)
        p2 =self.get_param(index, opcode, 2)
        self.lst[pos] = 1 if p1 < p2 else 0
        _logger.info('lt : % 5s: % 10s < % 10s = % 15s', index, p1, p2, self.lst[pos])
        _logger.debug('store: % 5s: % 15s', pos, self.lst[pos])
        return index + 4

    def opcode8(self, index):
        opcode = self.lst[index]
        pos = self.get_param(index, opcode, 3, force_positional=True)
        p1 =self.get_param(index, opcode, 1)
        p2 =self.get_param(index, opcode, 2)
        self.lst[pos] = 1 if p1 == p2 else 0
        _logger.info('lt : % 5s: % 10s < % 10s = % 15s', index, p1, p2, self.lst[pos])
        _logger.debug('store: % 5s: % 15s', pos, self.lst[pos])
        return index + 4

    def opcode9(self, index):
        opcode = self.lst[index]
        pos = self.get_param(index, opcode, 1)
        self.relativebase += pos
        _logger.info('rb : % 5s: % 10s => % 10s', index, pos, self.relativebase)
        return index + 2

    def opcode_exit(self, index):
        _logger.debug('exit')
        self._processing = False

    def opcode_none(self, x):
        return x+1

    def process(self):
        self.output = []
        self.lst = self.olst.copy()
        self._processing = True
        index = 0
        while self._processing:
            _logger.info('opc: % 5s', self.lst[index])
            _logger.debug('....[% 5s] % 5s, % 5s, % 5s, % 5s, % 5s ....', index, self.lst[index],self.lst[index+1],self.lst[index+2],self.lst[index+3],self.lst[index+4])
            index = getattr(self, self.opcodes[self.lst[index]%100])(index)
        return self.lst[0]

    def process_till(self, result):
        for i in range(0, len(self.olst)):
            for j in range(0, len(self.olst)):
                res = p.process(i, j)
                if res == result:
                    return 100*i+j



if part_one():
    p = processor(inp, [1])
    result = p.process()
    print(p.output)

if part_two():
    p = processor(inp, [1])
    result = p.process()
    print(p.output)
