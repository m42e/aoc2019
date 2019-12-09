import sys
from collections import defaultdict, namedtuple
import aoc

def inp_decode(x):
    return list(map(int,x.split(',')))

inp = aoc.get_input(inp_decode)
_logger = aoc.get_logger()

opcode = namedtuple('opcode', ['name', 'parameter'])
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


class disassembler(object):
    def disassemble(self, prog):
        pos = 0
        commands = []
        while pos < len(prog):
            assemblerline = [f'[{pos:< 5}]']
            commandcode = prog[pos] % 100
            try:
                assemblerline.append(opcodes[commandcode].name)
                for pindex, param in enumerate(opcodes[commandcode].parameter, start=1):
                    encoding = ((prog[pos] // pow(10, pindex+1)) % 10)
                    modes = {0: '*', 1: '', 2: '@'}
                    pv = prog[pos + pindex]
                    assemblerline.append(f'{modes[encoding]}{pv}')
                pos += len(opcodes[commandcode].parameter) + 1
            except:
                assemblerline.append('XXX')
                pos += 1
            finally:
                commands.append(' '.join(map(lambda x: '{0:>10}'.format(x), assemblerline)))
        return commands


class p2(object):
    def __init__(self):
        self.hardreset()
        self.processed_steps = []

    def hardreset(self):
        self.tinput = []
        self.mem = defaultdict(lambda: [{'r': 0, 'v': 0, 'e': 0, 'w': {}}])
        self.reset()

    def reset(self):
        self.tinput_pos = 0
        self.output = []
        self.relativebase = [0]
        self.ip = 0
        self.steps = 0

    def set_prog(self, prog):
        for i, f in enumerate(prog):
            self.mem[i] = [{'v': f, 'r': 0, 'e': 0, 'w': {}}]

    def add_input(self, inp):
        self.tinput.append(inp)

    def fetch_and_decode(self):
        opcode = self.read(self.ip, execute=True)
        params = [opcode % 100]
        self.decodeinfo = {'ip': self.ip, 'opcode': opcode}
        for pindex, param in enumerate(opcodes[params[0]].parameter, start=1):
            encoding = ((opcode // pow(10, pindex+1)) % 10)
            val = self.read(self.ip + pindex)
            if encoding == 2:
                val += self.relativebase[-1]
            self.decodeinfo[pindex] = {'position': self.ip+pindex, 'value':val, 'mode': encoding, 'paramtype': param}
            if param == 'i':
                if encoding == 0 or encoding == 2:
                    val = self.read(val)
            self.decodeinfo[pindex]['decoded'] = val
            params.append(val)
        return params

    def step(self):
        self.steps += 1
        fetched = self.fetch_and_decode()
        commandcode = fetched[0]
        params = fetched[1:]
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
        self.mem[pos].append({'v': value, 'r': 0, 'e': 0, 'w': self.decodeinfo})
        return self.mem[pos][-1]['v']

    def read(self, pos, execute=False):
        if execute:
            self.mem[pos][-1]['e'] += 1
        self.mem[pos][-1]['r'] += 1
        return self.mem[pos][-1]['v']

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

    def get_mem_sum(self, what):
        m_id = -1
        m_val = 0
        for i, m in self.mem.items():
            s = sum(map(lambda x: x[what] if str(x[what]).isnumeric() else 1, m))
            if m_val < s:
                m_val = s
                m_id = i
        return m_id, m_val

    def statistics(self):
        statdata = {}
        statdata['steps'] = self.steps
        statdata['most read'], statdata['most read count'] = self.get_mem_sum('r')
        statdata['most exec'], statdata['most exec count'] = self.get_mem_sum('e')
        statdata['most write'], statdata['most write count'] = self.get_mem_sum('w')
        return statdata


def main():
    p = p2()
    p.add_input(1)
    p.set_prog(inp)
    p.run()
    print(f'processed: {p.steps} steps')
    print(f'Result: {p.output}')
    for n, v in p.statistics().items():
        print(f'{n}: {v}')
    if False:
        for mi, m in p.mem.items():
            print(f'{mi:>5}', end = ' ')
            if len(m) > 1:
                for mn in m:
                    if mn['e'] != 0:
                        print('!'*100)
                    print(f'    v: {mn["v"]} r: {mn["r"]} e: {mn["e"]} w: ')
                    for pii, pi in mn['w'].items():
                        print(f'        {pii}: {pi}')
            else:
                print(f'{m}')

    p.hardreset()
    p.add_input(2)
    p.set_prog(inp)
    p.run()
    print(f'processed: {p.steps} steps')
    print(f'Result: {p.output}')
    for n, v in p.statistics().items():
        print(f'{n}: {v}')
    d = disassembler()
    r = d.disassemble(inp)

    #print('\n'.join(r))

if __name__ == "__main__":
    main()
