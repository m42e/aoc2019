import sys
from collections import defaultdict, namedtuple
import fileinput

opcode = namedtuple("opcode", ["name", "parameter"])
opcodes = {
    1: opcode(name="ADD", parameter="iio"),
    2: opcode(name="MUL", parameter="iio"),
    3: opcode(name="INP", parameter="o"),
    4: opcode(name="OUT", parameter="i"),
    5: opcode(name="JIT", parameter="ii"),
    6: opcode(name="JIF", parameter="ii"),
    7: opcode(name="LT ", parameter="iio"),
    8: opcode(name="EQ ", parameter="iio"),
    9: opcode(name="ARB", parameter="i"),
    99: opcode(name="HLT", parameter=""),
}


class Assembler(object):
    def __init__(self):
        self.variables = {}
        self.consts = {}
        self.locs = {}

    def assemble_code(self, code):
        self.opcode = []

        for line in code:
            self.opcode += self.assemble(line.strip(), len(self.opcode))
        self.second_pass()
        return opcode

    def second_pass(self):
        for i in range(0, len(self.opcode)):
            if str(self.opcode[i]).isnumeric():
                continue
            if self.opcode[i][0] == "L":
                if not self.opcode[i][1:] in self.locs:
                    raise Exception(" no {}".format(self.opcode[i][1:]))
                self.opcode[i] = self.locs[self.opcode[i][1:]]

    def token_var(self, token, pos):
        varpos = pos + 3
        self.variables[token[1]] = varpos
        return [1105, 1, pos + 4, int(token[2])]

    def token_con(self, token, pos):
        self.consts[token[1]] = int(token[2])
        return []

    def token_loc(self, token, pos):
        self.locs[token[1]] = pos
        return []

    def assemble(self, line, pos):
        if "#" in line:
            linecontent, _ = line.split("#")
        else:
            linecontent = line
        linecontent = linecontent.strip()
        if len(linecontent) == 0:
            return []
        tokens = linecontent.split(" ")
        commands = {x.name: y for y, x in opcodes.items()}
        commands.update(
            {"VAR": self.token_var, "CON": self.token_con, "LOC": self.token_loc,}
        )
        command = commands[tokens[0]]
        if callable(command):
            return command(self, tokens, pos)

        instruction = []

        if len(tokens) > 1:
            for i, p in enumerate(tokens[1:]):
                if p[0] == "V":
                    instruction.append(self.variables[p[1:]])
                    continue
                if p[0] == "C":
                    command += 1 * pow(10, i + 2)
                    instruction.append(self.consts[p[1:]])
                    continue
                if p[0] == "L":
                    command += 1 * pow(10, i + 2)
                    if p[1:] in self.locs:
                        instruction.append(self.locs[p[1:]])
                    else:
                        instruction.append(p)
                    continue
                if p[0] == "A":
                    instruction.append(p[1:])
                    continue
                if p[0] == "R":
                    command += 2 * pow(10, i + 2)
                    instruction.append(p[1:])
                else:
                    command += 1 * pow(10, i + 2)
                    instruction.append(p)
        instruction.insert(0, command)

        return instruction

class Disassembler(object):
    @classmethod
    def disassemble(cls, prog):
        pos = 0
        commands = []
        while pos < len(prog):
            assemblerline = [f"[{pos:< 5}]"]
            commandcode = prog[pos] % 100
            try:
                assemblerline.append(opcodes[commandcode].name)
                for pindex, _ in enumerate(opcodes[commandcode].parameter, start=1):
                    encoding = (prog[pos] // pow(10, pindex + 1)) % 10
                    modes = {0: "A", 1: "", 2: "R"}
                    pv = prog[pos + pindex]
                    assemblerline.append(f"{modes[encoding]}{pv}")
                pos += len(opcodes[commandcode].parameter) + 1
            except:
                assemblerline.append("DATA")
                pos += 1
            finally:
                commands.append(
                    " ".join(map(lambda x: "{0:>10}".format(x), assemblerline))
                )
        return commands


class Processor(object):
    def __init__(self):
        self.hardreset()
        self.processed_steps = []
        self._processing = False

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

    def set_mem(self, mem):
        self.hardreset()
        self.mem = mem

    def set_prog(self, prog):
        for i, f in enumerate(prog):
            self.mem[i] = [{"v": f, "r": 0, "e": 0, "w": {}}]

    def add_input(self, inp):
        self.tinput.append(inp)

    def fetch_and_decode(self):
        opcode = self.read(self.ip, execute=True)
        params = [opcode % 100]
        self.decodeinfo = {"ip": self.ip, "opcode": opcode, "params": {}}
        for pindex, param in enumerate(opcodes[params[0]].parameter, start=1):
            encoding = (opcode // pow(10, pindex + 1)) % 10
            val = self.read(self.ip + pindex)
            if encoding == 2:
                val += self.relativebase[-1]
            self.decodeinfo["params"][pindex] = {
                "position": self.ip + pindex,
                "value": val,
                "mode": encoding,
                "paramtype": param,
            }
            if param == "i":
                if encoding == 0 or encoding == 2:
                    val = self.read(val)
            self.decodeinfo["params"][pindex]["decoded"] = val
            params.append(val)
        return params

    def step(self):
        self.steps += 1
        self.result = None
        fetched = self.fetch_and_decode()
        commandcode = fetched[0]
        params = fetched[1:]
        ip = self.ip
        getattr(self, f"opcode{commandcode:02d}")(params)
        self.processed_steps.append(
            {
                "decodinginfo": self.decodeinfo,
                "opcode": commandcode,
                "ip": ip,
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


def print_memory_info(p, file=sys.stderr):
    for mi, m in p.mem.items():
        print(f"{mi:>6}", end=" ", file=file)
        if len(m) > 1:
            for mn in m:
                print(f'    v: {mn["v"]} r: {mn["r"]} e: {mn["e"]} w: ', file=file)
                for pii, pi in mn["w"].items():
                    print(f"        {pii}: {pi}", file=file)
        else:
            print(f"{m}", file=file)


def print_steps(p, params=False, file=sys.stderr):
    for mi, m in enumerate(p.processed_steps):
        print(f"{mi:>6}", end=" ", file=file)
        print(
            opcodes[m["opcode"]].name,
            m["params"],
            m["result"],
            m["processing"],
            m["ip"],
            file=file,
        )
        if not params:
            continue
        for di in m["decodinginfo"]["params"]:
            print("       {}".format(m["decodinginfo"]["params"][di]), file=file)

def generate_jump_graph(p:Processor):
    lastjump = 1
    jumps = defaultdict(int)
    execflow = defaultdict(int)
    jumps['start->1'] = 1
    for _, m in enumerate(p.processed_steps):
        if opcodes[m["opcode"]].name[0] == 'J':
            execflow['{}->{}'.format(lastjump, m['ip'])] += 1
            jumps['{}->{}'.format(m['ip'], m['params'][1])] += 1
            lastjump = m['params'][1]
    execflow['{}->{}'.format(lastjump, 'end')] = 1

    graph = ['digraph G {']
    for edge, count in jumps.items():
        graph.append('{0} [label="{1}"];'.format(edge, count))
    for edge, count in execflow.items():
        graph.append('{0} [label="{1}", style=dotted];'.format(edge, count))
    graph.append('}')
    return '\n'.join(graph)





def print_stats(stat):
    for n, v in stat.items():
        print(f"{n}: {v}")
