import sys
from collections import defaultdict, namedtuple
import aoc

def inp_decode(x):
    return list(map(int,x.split(',')))

inp = aoc.get_input(inp_decode)
_logger = aoc.get_logger()

opcode = namedtuple('opcode', ['name', 'parameter'])

class p2(object):
    def __init__(self):
        self.hardreset()
        self.processed_steps = []

    def hardreset(self):
        self.tinput = []
        self.prog = defaultdict(lambda: [0])
        self.reset()

    def reset(self):
        self.tinput_pos = 0
        self.output = []
        self.relativebase = [0]
        self.ip = 0

    def set_prog(self, prog):
        for i, f in enumerate(prog):
            self.prog[i] = [f]

    def add_input(self, inp):
        self.tinput.append(inp)

    opcodes = {
        1: opcode(name='add', parameter='iio'),
        2: opcode(name='mul', parameter='iio'),
        3: opcode(name='inp', parameter='o'),
        4: opcode(name='out', parameter='i'),
        5: opcode(name='jit', parameter='ii'),
        6: opcode(name='jif', parameter='ii'),
        7: opcode(name='lt ', parameter='iio'),
        8: opcode(name='eq ', parameter='iio'),
        9: opcode(name='arb', parameter='i'),
        99: opcode(name='hlt', parameter=''),
    }

    def decode(self, parameters):
        opcode = self.prog[self.ip][-1]
        params = []
        self.decodeinfo = {}
        for pindex, param in enumerate(parameters, start=1):
            encoding = ((opcode // pow(10, pindex+1)) % 10)
            val = self.prog[self.ip+pindex][-1]
            if encoding == 2:
                val += self.relativebase[-1]
            self.decodeinfo[pindex] = {'position': self.ip+pindex, 'value':val, 'mode': encoding, 'paramtype': param, 'opcode': opcode}
            if param == 'i':
                if encoding == 0 or encoding == 2:
                    val = self.prog[val][-1]
            self.decodeinfo[pindex]['decoded'] = val
            params.append(val)
        return params

    def fetch_and_decode(self, commandcode):
        return self.decode(self.opcodes[commandcode].parameter)

    def step(self):
        commandcode = self.prog[self.ip][-1] % 100
        params = self.fetch_and_decode(commandcode)
        getattr(self, f'opcode{commandcode:02d}')(params)
        self.processed_steps.append({
            'decodinginfo': self.decodeinfo,
            'opcode': commandcode,
            'ip': self.ip,
            'params': params,
        })

    def run(self):
        self._processing = True
        while(self._processing):
            self.step()

    def write(self, pos, value):
        self.prog[pos].append(value)

    def opcode01(self, params):
        res = params[0] + params[1]
        self.write(params[2], res)
        self.ip += 4

    def opcode02(self, params):
        res = params[0] * params[1]
        self.write(params[2], res)
        self.ip += 4

    def opcode03(self, params):
        if self.tinput_pos == len(self.tinput):
            _logger.debug('read, no input available')
        elif isinstance(self.tinput, list):
            res = self.tinput[self.tinput_pos]
            self.tinput_pos += 1
        else:
            _logger.debug('store: % 5s: % 15s', pos, self.tinput)
            res = self.tinput
        self.write(params[0], res)
        self.ip += 2

    def opcode04(self, params):
        self.output.append(params[0])
        self.ip += 2

    def opcode05(self, params):
        p1, p2 = params
        if p1 > 0:
            self.ip = p2
        else:
            self.ip += 3

    def opcode06(self, params):
        p1, p2 = params
        if p1 == 0:
            self.ip = p2
        else:
            self.ip += 3

    def opcode07(self, params):
        p1, p2, pos = params
        res = 1 if p1 < p2 else 0
        self.write(pos, res)
        self.ip += 4

    def opcode08(self, params):
        p1, p2, pos = params
        res = 1 if p1 == p2 else 0
        self.write(pos, res)
        self.ip += 4

    def opcode09(self, params):
        self.relativebase.append(self.relativebase[-1] + params[0])
        self.ip += 2

    def opcode99(self, index):
        self._processing = False


def main():
    p = p2()
    p.add_input(1)
    p.set_prog(inp)
    p.run()
    graph = ['nstart [label="Start"];']
    from pprint import pprint
    lastnode = 'nstart'
    graph.append('subgraph {')
    graph.append('rank = same;')
    for s in p.processed_steps:
        nodestr = f'n{s["ip"]}'
        graph.append(f'{nodestr} [label="{s["opcode"]}"];')
    graph.append('}')
    graph.append('subgraph {')
    graph.append('rank = same;')
    for s in p.processed_steps:
        for r in s['decodinginfo'].values():
            if r['paramtype'] == 'i':
                if r['mode'] == 1:
                    graph.append(f'n{r["position"]};')
    graph.append('}')
    for s in p.processed_steps:
        nodestr = f'n{s["ip"]}'
        graph.append(f'{lastnode} -> {nodestr} [style=bold];')
        lastnode = nodestr
        for r in s['decodinginfo'].values():
            if r['paramtype'] == 'i':
                if r['mode'] == 1:
                    graph.append(f'{nodestr} -> n{r["position"]};')
                if r['mode'] == 0 or r['mode'] == 2:
                    graph.append(f'{nodestr} -> n{r["position"]};')
                    graph.append(f'n{r["position"]} -> n{r["value"]} [style=dashed, constraint=false];')
    print('digraph G{')
    print('\n'.join(graph))
    print('}')


if __name__ == "__main__":
    main()
