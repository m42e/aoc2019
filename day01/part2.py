
with open('data/sample.txt') as f:
    input = list(map(int, map(str.strip, f.readlines())))

with open('data/sample_output.txt') as f:
    output = list(map(int, map(str.strip, f.readlines())))

for value,expected in zip(input, output):
    amount = 0
    while True:
        result = value//3 - 2
        if result <= 0:
            break
        amount += result
        value = result
    print(amount, expected)

with open('data/data.txt') as f:
    input = list(map(int, map(str.strip, f.readlines())))

sum = 0
for value in input:
    amount = 0
    while True:
        result = value//3 - 2
        if result <= 0:
            break
        amount += result
        value = result
    sum += amount
    print(amount)
print(sum)
