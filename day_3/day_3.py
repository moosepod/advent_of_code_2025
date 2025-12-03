import argparse
import re
import itertools

def iterate_silver(line):
    return max(int(''.join(s)) for s in itertools.combinations(line, 2))

def iterate_gold(line):
    m = 0
    for s in itertools.combinations(line, 12):
        x = int(''.join(s))
        if x > m:
            m = x

    return m


def solve(iterate_f, path="day_3/inputs/input.txt"):
    lines = []
    with open(path) as f:
        for line in f.read().split("\n"):
            if line:
                lines.append(iterate_f(line))

    a = sum(lines)
    print(f"Answer: {a}")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("star")
    args = parser.parse_args()
    if args.star == "silver":
        solve(iterate_silver)
    elif args.star == "gold":
        solve(iterate_gold)
    else:
        print("First argument must be silver or gold")

