import argparse
import re
import itertools

def iterate_silver(line):
    m = 0
    for ai,a in enumerate([int(c) for c in line]):
        for bi,b in enumerate([int(c) for c in line]):
            if ai > bi:
                x = b * 10 + a
            elif ai < bi:
                x = a * 10 + b
            else:
                x = 0
            if x > m:
                m = x
                ma,mb = a,b

    return m

def iterate_gold():
    pass

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

