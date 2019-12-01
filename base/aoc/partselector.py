import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-A', action='store_true')
    parser.add_argument('-B', action='store_true')
    return parser.parse_known_args()

def part_one():
    p = parse_args()[0]
    if p.B:
        return False
    return True

def part_two():
    p = parse_args()[0]
    if p.A:
        return False
    return True
