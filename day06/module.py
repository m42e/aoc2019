from aoc.input import get_input
from aoc.partselector import part_one, part_two

def orbit(x):
    return x.split(')')

inp = get_input(orbit)

orbits = {'COM': None}
for c,o in inp:
    orbits[o] = c

if part_one():
    total = 0
    for o in orbits:
        count = 0
        while orbits[o] is not None:
            count+=1
            o = orbits[o]
        total += count
    print (total)

    pass

if part_two():
    chains={}
    for o in ['YOU', 'SAN']:
        count = 0
        i = o
        chains[o] = []
        while orbits[o] is not None:
            count+=1
            chains[i].append(o)
            o = orbits[o]
    common = len(list(set(chains['YOU']).intersection(chains['SAN'])))
    print(len(chains['SAN']) + len(chains['YOU']) - 2*common -2)
    print(chains['SAN'][:-common])
    print(chains['YOU'][:-common])
    print(len(chains['SAN'][:-common]) + len(chains['YOU'][:-common]) -2)

    pass
