from aoc.input import get_input
import timeit
from aoc.partselector import part_one, part_two

i = [256310, 732736]
if part_one():
    def p1():
        count = 0
        for x in range(256310, 732736):
            last = '0'
            for l in str(x):
                if l < last:
                    break
                last = l
            else:
                count += 1
        return count
    def p1b():
        count = 0
        for x in range(256310, 732736):
            for i in range(1,7):
                if x/pow(10,i) < x/pow(10,i-1):
                    break
            else:
                count += 1
        return count
    print (p1b())
    t = timeit.Timer(p1)
    pass

if part_two():
    def p2():
        count = 0
        for x in range(256310, 732736):
            x = str(x)
            last = '0'
            for l in x:
                if l < last:
                    break
                last = l
            else:
                last = '0'
                valid = False
                for i, y in enumerate(x):
                    if y == last:
                        continue
                    cnt = 0
                    for z in x[i:]:
                        if z == y:
                            cnt += 1
                    if cnt == 2:
                        valid |= True
                    last = y
                if valid:
                    count += 1
        return count
    print(p2())
    pass
