import sys
import curses
import time
import termcolor
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
        self.decodeinfo = {"ip": self.ip, "opcode": opcode, 'params': {}}
        for pindex, param in enumerate(opcodes[params[0]].parameter, start=1):
            encoding = (opcode // pow(10, pindex + 1)) % 10
            val = self.read(self.ip + pindex)
            if encoding == 2:
                val += self.relativebase[-1]
            self.decodeinfo['params'][pindex] = {
                "position": self.ip + pindex,
                "value": val,
                "mode": encoding,
                "paramtype": param,
            }
            if param == "i":
                if encoding == 0 or encoding == 2:
                    val = self.read(val)
            self.decodeinfo['params'][pindex]["decoded"] = val
            params.append(val)
        return params

    def step(self):
        self.steps += 1
        self.result = None
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
                "result": self.result,
                "processing": self._processing,
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
        self.result = res

    def opcode02(self, params):
        res = params[0] * params[1]
        self.write(params[2], res)
        self.ip += 4
        self.result = res

    def opcode03(self, params):
        if self.tinput_pos == len(self.tinput):
            _logger.debug("read, no input available")
            self._processing = False
            self.result = "no read"
            return self.ip
        elif isinstance(self.tinput, list):
            res = self.tinput[self.tinput_pos]
            self.tinput_pos += 1
        else:
            res = self.tinput
        self.write(params[0], res)
        self.ip += 2
        self.result = res

    def opcode04(self, params):
        self.output.append(params[0])
        self.ip += 2

    def opcode05(self, params):
        p1, p2 = params
        if p1 > 0:
            self.ip = p2
        else:
            self.ip += 3
        self.result = self.ip

    def opcode06(self, params):
        p1, p2 = params
        if p1 == 0:
            self.ip = p2
        else:
            self.ip += 3
        self.result = self.ip

    def opcode07(self, params):
        p1, p2, pos = params
        res = 1 if p1 < p2 else 0
        self.write(pos, res)
        self.ip += 4
        self.result = res

    def opcode08(self, params):
        p1, p2, pos = params
        res = 1 if p1 == p2 else 0
        self.write(pos, res)
        self.ip += 4
        self.result = res

    def opcode09(self, params):
        self.relativebase.append(self.relativebase[-1] + params[0])
        self.ip += 2
        self.result = self.relativebase[-1]

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

def print_steps(p, file = sys.stderr):
    for mi, m in enumerate(p.processed_steps):
        print(f"{mi:>5}", end=" ", file=file)
        print(opcodes[m['opcode']].name, m['params'], m['result'], m['processing'], file=file)
        continue
        for di in m['decodinginfo']['params']:
            print('       {}'.format(m['decodinginfo']['params'][di]), file=file)
        continue
        if len(m) > 1:
            for mn in m:
                print(f'    v: {mn["v"]} r: {mn["r"]} e: {mn["e"]} w: ', file=file)
                for pii, pi in mn["w"].items():
                    print(f"        {pii}: {pi}", file)
        else:
            print(f"{m}", file=file)

def print_stats(stat):
    for n, v in stat.items():
        print(f"{n}: {v}")


p = p2()

class drawbot(object):
    directions = ['u', 'l', 'd', 'r']
    drawdir = ['^', '<', 'v', '>']
    step = [(0,1), (-1,0), (0, -1), (1,0)]
    def __init__(self, x,y, startval, off_x=30, off_y=45):
        self.x = x
        self.y = y
        self.off_x = off_x
        self.off_y = off_y
        self.direction = 'u'
        self.grid = defaultdict(lambda: defaultdict(int))
        self.grid[0][0] = startval
        self.steps = 0
        import curses
        self.stdscr = curses.initscr()
        self.stdscr.clear()
        self.stdscr.addstr(self.off_y, self.off_x, "^")

    def get_color(self):
        return self.grid[self.y][self.x]

    def command(self, color, direction):
        self.grid[self.y][self.x] = color
        if direction == 0:
            self.direction = self.directions[(self.directions.index(self.direction)+1)%4]
        else:
            self.direction = self.directions[(self.directions.index(self.direction)-1)%4]

    def move(self):
        x,y = self.step[self.directions.index(self.direction)]
        v = self.grid[self.y][self.x]
        self.stdscr.refresh()
        try:
            if v == 1:
                 self.stdscr.addstr(self.off_y+self.y, self.off_x+self.x, '█')
            else:
                self.stdscr.addstr(self.off_y+self.y, self.off_x+self.x, '░')
        except: pass
        self.x += x
        self.y -= y
        try:
            self.stdscr.addstr(self.off_y+self.y, self.off_x+self.x, '' +self.drawdir[self.directions.index(self.direction)])
        except: pass
        self.steps += 1

    def colored(self):
        return sum(map(len, self.grid.values()))

class arcade(object):
    def __init__(self):
        self.grid = defaultdict(lambda: defaultdict(int))
        self.twos = 0
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)
        self.stdscr.clear()
        self.ball = (0,0)
        self.paddle = (0,0)

    def reset(self):
        for r in self.grid.values():
            r.clear()
        self.stdscr.clear()

    def draw(self, x,y,w):
        if w == 4:
            self.stdscr.addstr(self.ball[1], self.ball[0],' ')
            self.ball = x,y
            self.stdscr.addstr(y, x, str('o'))
            return
        if w == 3:
            self.stdscr.addstr(self.paddle[1], self.paddle[0], ' ')
            self.paddle = x,y
            self.stdscr.addstr(y, x, str('█'))
            return
        if x == -1:
            self.stdscr.addstr(1, 45, str('{}'.format(w)))
            return
        if w == 0:
            if y in self.grid:
                if x in self.grid[y]:
                    del self.grid[y][x]
            self.stdscr.addstr(y, x, ' ')
            return 
        self.grid[y][x] = w
        if w == 2:
            self.twos += 1
        self.stdscr.addstr(y, x, '█', curses.color_pair(w))

    def show(self):
        self.stdscr.refresh()
    def print(self, i, val):
        self.stdscr.addstr(5+i, 45, '                ')
        self.stdscr.addstr(5+i, 45, '{0}'.format(val))
    def step(self, val):
        self.stdscr.addstr(5, 45, '{0:2d}'.format(val))
        self.stdscr.move(23,0)

    def get_ball(self):
        return self.ball, self.paddle

f = lambda A, n=3: [A[i:i+n] for i in range(0, len(A), n)]

def part1():
    r = arcade()
    p = p2()
    p.set_prog(inp)
    while not p.halt:
        p.run()
        outp = p.output
        #r.command(*outp)
    for p in f(outp):
        r.draw(*p)
    return r.twos
    pass

def part2():
    r = arcade()
    p = p2()
    p.set_prog(inp)
    last_x = 15
    last_y = 18 
    target =18 
    step = 0
    while not p.halt:
        p.run()
        outp = p.output
        for v in f(outp):
            r.draw(*v)
        p.output.clear()
        b, pd = r.get_ball()
        right = last_x < b[0]
        down = last_y < b[1]
        if not down:
            target = b[0]
        else:
            target = (pd[1]-b[1])*(1 if right else -1)+ b[0] -1
        if target != pd[0]:
            if target > pd[0]:
                step = 1
            elif target < pd[0]:
                step = -1
        else:
            step = 0
        r.step(step)
        last_x = b[0]
        last_y = b[1]
        r.show()
        p.add_input(step)
        time.sleep(4)

def part2intcode():


    pki = p2()
    with open('data/prog.txt') as file:
        for line in file.readlines():
            pkinp = inp_decode(line.strip())
    pki.set_prog(pkinp)
    r = arcade()
    p = p2()
    p.set_prog(inp)
    while not p.halt:
        p.run()
        outp = p.output
        kiin = list(f(outp))
        pki.add_input(len(kiin))
        for v in kiin:
            r.draw(*v)
            for vv in v:
                pki.add_input(vv)
        p.output.clear()
        pki.output.clear()
        pki.run()
        r.show()
        p.add_input(pki.output[-1])
        pki.output.clear()
    with open('steps.txt', 'w+') as fo:
        print_steps(pki, fo)

def main():
    if aoc.part_one():
        result = part2()
        print(f'Result: {result}')

    if aoc.part_two():
        result = part2intcode()
        print(f'Result: {result}')

if __name__ == "__main__":
    main()
