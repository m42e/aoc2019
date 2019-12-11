import sys
import time
from collections import defaultdict, namedtuple
import aoc
import matplotlib.pyplot as plt


def inp_decode(x):
    return list(map(int, x.split(",")))


inp = aoc.get_input(inp_decode)
_logger = aoc.get_logger()

opcode = namedtuple("opcode", ["name", "parameter"])
opcodes = {
    1: opcode(name="add", parameter="iio"),
    2: opcode(name="mul", parameter="iio"),
    3: opcode(name="inp", parameter="o"),
    4: opcode(name="out", parameter="i"),
    5: opcode(name="jit", parameter="ii"),
    6: opcode(name="jif", parameter="ii"),
    7: opcode(name="lt ", parameter="iio"),
    8: opcode(name="eq ", parameter="iio"),
    9: opcode(name="arb", parameter="i"),
    99: opcode(name="hlt", parameter=""),
}


class disassembler(object):
    def disassemble(self, prog):
        pos = 0
        commands = []
        while pos < len(prog):
            assemblerline = [f"[{pos:< 5}]"]
            commandcode = prog[pos] % 100
            try:
                assemblerline.append(opcodes[commandcode].name)
                for pindex, param in enumerate(opcodes[commandcode].parameter, start=1):
                    encoding = (prog[pos] // pow(10, pindex + 1)) % 10
                    modes = {0: "*", 1: "", 2: "@"}
                    pv = prog[pos + pindex]
                    assemblerline.append(f"{modes[encoding]}{pv}")
                pos += len(opcodes[commandcode].parameter) + 1
            except:
                assemblerline.append("XXX")
                pos += 1
            finally:
                commands.append(
                    " ".join(map(lambda x: "{0:>10}".format(x), assemblerline))
                )
        return commands


class p2(object):
    def __init__(self):
        self.hardreset()
        self.processed_steps = []

    def hardreset(self):
        self.tinput = []
        self.mem = defaultdict(lambda: [{"r": 0, "v": 0, "e": 0, "w": {}}])
        self.reset()

    def reset(self):
        self.halt = False
        self.tinput_pos = 0
        self.output = []
        self.relativebase = [0]
        self.ip = 0
        self.steps = 0

    def set_prog(self, prog):
        for i, f in enumerate(prog):
            self.mem[i] = [{"v": f, "r": 0, "e": 0, "w": {}}]

    def add_input(self, inp):
        self.tinput.append(inp)

    def fetch_and_decode(self):
        opcode = self.read(self.ip, execute=True)
        params = [opcode % 100]
        self.decodeinfo = {"ip": self.ip, "opcode": opcode}
        for pindex, param in enumerate(opcodes[params[0]].parameter, start=1):
            encoding = (opcode // pow(10, pindex + 1)) % 10
            val = self.read(self.ip + pindex)
            if encoding == 2:
                val += self.relativebase[-1]
            self.decodeinfo[pindex] = {
                "position": self.ip + pindex,
                "value": val,
                "mode": encoding,
                "paramtype": param,
            }
            if param == "i":
                if encoding == 0 or encoding == 2:
                    val = self.read(val)
            self.decodeinfo[pindex]["decoded"] = val
            params.append(val)
        return params

    def step(self):
        self.steps += 1
        fetched = self.fetch_and_decode()
        commandcode = fetched[0]
        params = fetched[1:]
        getattr(self, f"opcode{commandcode:02d}")(params)
        self.processed_steps.append(
            {
                "decodinginfo": self.decodeinfo,
                "opcode": commandcode,
                "ip": self.ip,
                "params": params,
            }
        )

    def run(self):
        self._processing = True
        while self._processing:
            self.step()

    def write(self, pos, value):
        self.mem[pos].append({"v": value, "r": 0, "e": 0, "w": self.decodeinfo})
        return self.mem[pos][-1]["v"]

    def read(self, pos, execute=False):
        if execute:
            self.mem[pos][-1]["e"] += 1
        self.mem[pos][-1]["r"] += 1
        return self.mem[pos][-1]["v"]

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
            _logger.debug("read, no input available")
            self._processing = False
            return self.ip
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
        self.halt = True

    def get_mem_sum(self, what):
        m_id = -1
        m_val = 0
        for i, m in self.mem.items():
            s = sum(
                map(
                    lambda x: x[what]
                    if str(x[what]).isnumeric()
                    else len(str(x[what])) > 5,
                    m,
                )
            )
            if m_val < s:
                m_val = s
                m_id = i
        return m_id, m_val

    def get_mem_stat(self, what):
        stat = {}
        for i, m in self.mem.items():
            s = sum(
                map(
                    lambda x: x[what]
                    if str(x[what]).isnumeric()
                    else len(str(x[what])) > 5,
                    m,
                )
            )
            if s == 0:
                continue
            stat[i] = s
        return stat

    def statistics(self):
        statdata = {}
        statdata["steps"] = self.steps
        statdata["most read"], statdata["most read count"] = self.get_mem_sum("r")
        statdata["most exec"], statdata["most exec count"] = self.get_mem_sum("e")
        statdata["most write"], statdata["most write count"] = self.get_mem_sum("w")
        statdata["exec"] = self.get_mem_stat("e")
        statdata["read"] = self.get_mem_stat("r")
        statdata["written"] = self.get_mem_stat("w")
        return statdata


def heatmap(data, filename, show=True):
    fig, ax = plt.subplots()
    for d, m in [("read", "."), ("written", "o"), ("exec", "x")]:
        ax.scatter(*zip(*data[d].items()), alpha=0.5, marker=m, label=d)
    ax.grid()
    ax.legend()
    fig.savefig(filename)
    if show:
        plt.show()


def print_memory_info(p):
    for mi, m in p.mem.items():
        print(f"{mi:>5}", end=" ")
        if len(m) > 1:
            for mn in m:
                if mn["e"] != 0:
                    print("!" * 100)
                print(f'    v: {mn["v"]} r: {mn["r"]} e: {mn["e"]} w: ')
                for pii, pi in mn["w"].items():
                    print(f"        {pii}: {pi}")
        else:
            print(f"{m}")


def print_stats(stat):
    for n, v in stat.items():
        print(f"{n}: {v}")


p = p2()

class robot(object):
    directions = ['u', 'l', 'd', 'r']
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.direction = 'u'
        self.grid = defaultdict(lambda: defaultdict(int))
        self.grid[0][0] = 1
        self.steps = 0

    def get_color(self):
        return self.grid[self.y][self.x]

    def command(self, color, direction):
        self.grid[self.y][self.x] = color
        print(direction, self.direction)
        if direction == 0:
            self.direction = self.directions[(self.directions.index(self.direction)+1)%4]
        else:
            self.direction = self.directions[(self.directions.index(self.direction)-1)%4]
        print(self.direction)

    def move(self):
        if self.direction == 'u':
            x = 0
            y = 1
        elif self.direction == 'l':
            x = -1
            y = 0
        elif self.direction == 'r':
            x = 1
            y = 0
        elif self.direction == 'd':
            x = 0
            y = -1
        self.x += x
        self.y += y
        self.steps += 1

    def colored(self):
        return sum(map(len, self.grid.values()))

    def print_grid(self):
        print(chr(27)+'[2j')
        print('\033c')
        print('\x1bc')
        cnt = 0
        RANGE=30
        for y in range(RANGE, -RANGE, -1):
            for x in range(-RANGE, 10+RANGE, 1):
                if x == self.x and y == self.y:
                    print('x', end='')
                    continue
                if y not in self.grid or not x in self.grid[y]:
                    print(' ', end='')
                    continue
                v = self.grid[y][x]
                cnt += 1
                if v == 1:
                    print('#', end = '')
                else:
                    print('.', end = '')

            print()
        print(cnt)



def part1a():
    r = robot(0,0)
    r.command(1,0)
    r.move()
    r.print_grid()
    time.sleep(1)
    r.command(0,0)
    r.move()
    r.print_grid()
    time.sleep(1)
    r.command(1,0)
    r.move()
    r.print_grid()
    time.sleep(1)
    r.command(1,0)
    r.move()
    r.print_grid()
    time.sleep(1)
    r.command(0,1)
    r.move()
    r.print_grid()
    time.sleep(1)
    r.command(1,0)
    r.move()
    r.print_grid()
    time.sleep(1)
    r.command(1,0)
    r.move()
    r.print_grid()
    time.sleep(1)
    return 1
def part1b():
    r = robot(0,0)
    p = p2()
    p.set_prog(inp)
    while not p.halt:
        p.add_input(r.get_color())
        p.run()
        outp = p.output
        r.command(*outp)
        p.output.clear()
        r.move()
        r.print_grid()
        #r.print_grid()
    print(r.colored())
    print(r.steps)

    pass
def part2():
    pass


def main():
    if aoc.part_one():
        result = part1b()

        print(f'Result: {result}')

    if aoc.part_two():
        result = part2()
        print(f'Result: {result}')

if __name__ == "__main__":
    main()
