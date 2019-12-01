import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sample', action='store_true')
    parser.add_argument('input', type=str, nargs='*')
    return parser.parse_known_args()

def get_input(transform):
    p = parse_args()[0]
    if p.input:
        return transform(p.input)
    inp = []
    if p.sample:
        with open('data/sample.txt') as f:
            for line in f.readlines():
                inp.append(transform(line.strip()))
    else:
        with open('data/data.txt') as f:
            for line in f.readlines():
                inp.append(transform(line.strip()))
    if len(inp) == 1:
        return next(inp)
    return inp
