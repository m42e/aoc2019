from aoc.input import get_input
from aoc.partselector import part_one, part_two
import matplotlib.pyplot as plt

def inpfmt(x):
    return x.split(',')
inp = get_input(inpfmt)

def common_member(a, b): 

    a_set = set(a) 
    b_set = set(b) 

    # check length  
    if len(a_set.intersection(b_set)) > 0: 
        return(a_set.intersection(b_set))   
    else: 
        return("no common elements")

wires = []
for w in inp:
    current = (0,0)
    coordinates = [current]
    for p in w:
        if p[0] == 'R':
            x=1
            y=0
        if p[0] == 'L':
            x=-1
            y=0
        if p[0] == 'U':
            x=0
            y=1
        if p[0] == 'D':
            x=0
            y=-1
        for i in range(0, int(p[1:])):
            current = (current[0] + x, current[1]+y)
            coordinates.append(current)
    wires.append(coordinates)


plt.plot(*zip(*wires[0]), zorder=1)
plt.plot(*zip(*wires[1]), zorder=1)
plt.scatter(0,0, marker="D", zorder=3)

if part_one():
    commons = common_member(wires[0], wires[1])
    def hd(x):
        return x[0]+x[1]
    minimal = sorted(commons, key=hd)[1]
    print(sorted(commons, key=hd))
    plt.scatter(*zip(*commons), color="#FF0000", zorder=2)
    plt.scatter(*minimal, marker="x", color="#0000FF", zorder=3)

if part_two():
    m = 100000
    for c in commons:
        if c != (0,0):
            m = min(m, wires[0].index(c) + wires[1].index(c))
    print(m)
plt.show()
