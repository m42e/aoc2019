from aoc.input import get_input
from aoc.partselector import part_one, part_two

inp = get_input(int)

def calc_amount(value):
    return value//3 - 2

if part_one():
    sum = 0
    for value in inp:
        result = calc_amount(value)
        print(f'{value:15}:{result}')
        sum += result
    print(sum)

if part_two():
    sum = 0
    for value in inp:
        amount = 0
        while True:
            result = calc_amount(value)
            if result <= 0:
                break
            amount += result
            value = result
        sum += amount
        print(amount)
    print(sum)
