import sys
from itertools import permutations
from collections import defaultdict, OrderedDict
from aoc.input import get_input

from aoc.partselector import part_one, part_two, get_logger

def inp_decode(x):
    return dict(map(lambda x: (x.strip()[0],int(x.strip()[2:])), x[1:-1].split(',')))

inp = get_input(inp_decode)
_logger = get_logger()
print(inp)

class moon(object):
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.vel = {'x':0, 'y':0, 'z': 0}
        self.hist = {'x':{}, 'y':{}, 'z': {}}
        self.asteps = {'x':0, 'y':0, 'z': 0}
        self.steps = 0
        self.rotate = {'x':False, 'y':False, 'z': False}

    @property
    def posidx(self):
        posidx = 'x{}y{}z{}x{}y{}z{}'.format(self.pos['x'], self.pos['y'], self.pos['z'], self.vel['x'], self.vel['y'], self.vel['z'])
        posidx = 'x{}y{}z{}'.format(self.pos['x'], self.pos['y'], self.pos['z'], self.vel['x'], self.vel['y'], self.vel['z'])
        return posidx

    def apply_gravity(self, moon2):
        for axis in ['x', 'y', 'z']:
            if self.pos[axis] > moon2.pos[axis]:
                self.vel[axis] -= 1
            elif self.pos[axis] < moon2.pos[axis]:
                self.vel[axis] += 1

    def apply_velocity(self):
        self.steps += 1
        for axis in ['x', 'y', 'z']:
            if not self.rotate[axis]:
                if self.had_position():
                    self.rotate = True
                    self.astep[axis] = self.steps
                    print(self.name, self.asteps)
        for axis in ['x', 'y', 'z']:
            self.pos[axis] += self.vel[axis]
            self.hist[axis][self.posidx] = 1

    def had_position(self):
        return self.posidx in self.hist

    def energy(self):
        pot = sum(map(abs, self.pos.values()))
        kin = sum(map(abs, self.vel.values()))
        return pot*kin


def p1():
    moons = []
    name = 0
    for m in inp:
        moons.append(moon(name, m))
        name += 1
    for m in moons:
        print('pos=<x={0:3d}, y={1:3d}, z={2:3d} vel=<x={3:3d}, y={4:3d}, z={5:3d}>'.format(m.pos['x'], m.pos['y'], m.pos['z'], m.vel['x'], m.vel['y'], m.vel['z']))
    for s in range(0, 14):
        for p in permutations(moons, 2):
            #print(list(map(lambda x: x.name, p)))
            p[0].apply_gravity(p[1])
        for m in moons:
            m.apply_velocity()
        for m in moons:
            continue
            print('pos=<x={0:3d}, y={1:3d}, z={2:3d}'.format(m.pos['x'], m.pos['y'], m.pos['z']))
    for m in moons:
        print('pos=<x={0:3d}, y={1:3d}, z={2:3d} vel=<x={3:3d}, y={4:3d}, z={5:3d}>'.format(m.pos['x'], m.pos['y'], m.pos['z'], m.vel['x'], m.vel['y'], m.vel['z']))
    return sum(map(moon.energy, moons))


from functools import reduce    # need this line if you're using Python3.x

from math import gcd 
#from fractions import gcd # If python version is below 3.5
from functools import reduce # Needed for Python3.x

def lcm(denominators):
    return reduce(lambda a,b: a*b // gcd(a,b), denominators)

def p2():
    moons = []
    name = 0
    for m in inp:
        moons.append(moon(name, m))
        name += 1
    for m in moons:
        print('pos=<x={0:3d}, y={1:3d}, z={2:3d}'.format(m.pos['x'], m.pos['y'], m.pos['z']))
    steps = 22972854
    csteps = [160, 101505526, 11939094, 22972854]
    bsteps = steps
    step = max(csteps)
    while True:
        for p in permutations(moons, 2):
            p[0].apply_gravity(p[1])
        for m in moons:
            m.apply_velocity()
        if all(map(lambda m: m.rotate, moons)):
            csteps = list(map(lambda m: m.steps, moons))
            print(csteps)
            print(lcm(csteps))
            return lcm(csteps)
            bsteps = steps
            step = max(csteps)
            while True:
                bsteps += 1
                if all(map(lambda i: bsteps%csteps[i] == 0, [0,1,2,3])):
                    return bsteps

    return steps

def main():
    if part_one():
        result = p1()
        print(f'Result: {result}')

    if part_two():
        result = p2()
        print(f'Result: {result}')

if __name__ == "__main__":
    main()
