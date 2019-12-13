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
        self.initial = pos
        self.vel = {'x':0, 'y':0, 'z': 0}

    def apply_gravity(self, moon2):
        for axis in ['x', 'y', 'z']:
            if self.pos[axis] > moon2.pos[axis]:
                self.vel[axis] -= 1
            elif self.pos[axis] < moon2.pos[axis]:
                self.vel[axis] += 1

    def apply_velocity(self):
        for axis in ['x', 'y', 'z']:
            self.pos[axis] += self.vel[axis]

    def energy(self):
        pot = sum(map(abs, self.pos.values()))
        kin = sum(map(abs, self.vel.values()))
        return pot*kin

    def __str__(self):
        return ('pos=<x={0:3d}, y={1:3d}, z={2:3d} vel=<x={3:3d}, y={4:3d}, z={5:3d}>'.format(self.pos['x'], self.pos['y'], self.pos['z'], self.vel['x'], self.vel['y'], self.vel['z']))


def p1():
    moons = []
    name = 0
    for m in inp:
        moons.append(moon(name, m))
        name += 1
    for m in moons:
        print(f'{m}')
    for s in range(0, 1000):
        for p in permutations(moons, 2):
            p[0].apply_gravity(p[1])
        for m in moons:
            m.apply_velocity()
        for m in moons:
            print(f'{m}')
        print()
    for m in moons:
        print(f'{m}')
    return sum(map(moon.energy, moons))


from functools import reduce    # need this line if you're using Python3.x
from math import gcd 
from functools import reduce # Needed for Python3.x

def lcm(denominators):
    return reduce(lambda a,b: a*b // gcd(a,b), denominators)

def p2():
    moons = []
    f = {}
    name = 0
    for m in inp:
        moons.append(moon(name, m))
        name += 1
    for m in moons:
        print(f'{m}')
    for axis in ['x', 'y', 'z']:
        f[axis] = {}
    steps = 0
    rtt = {'x':0, 'y':0, 'z': 0}
    while True:
        for p in permutations(moons, 2):
            p[0].apply_gravity(p[1])
        for m in moons:
            m.apply_velocity()
        for axis in ['x', 'y', 'z']:
            idx = ''.join(map(lambda x: '.{}:{}{}'.format(x.name, x.pos[axis], x.vel[axis]), moons))
            if rtt[axis] == 0 and idx in f[axis]:
                rtt[axis] = steps
                print(idx, steps)
            f[axis][idx] = 1
        if all(map(lambda x: x != 0, rtt.values())):
            print(rtt)
            break
        steps += 1

    return lcm(rtt.values())

def main():
    if part_one():
        result = p1()
        print(f'Result: {result}')

    if part_two():
        result = p2()
        print(f'Result: {result}')

if __name__ == "__main__":
    main()
