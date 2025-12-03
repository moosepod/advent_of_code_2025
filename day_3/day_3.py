import argparse
import re
import itertools

def iterate_silver(line):
    return max(int(''.join(s)) for s in itertools.combinations(line, 2))

def digit_prefixed_substrings(line, digit_s):
    # Find all indexes of this number
    indexes = [i for i in range(0,len(line)-12) if line[i] == digit_s]
    return [line[i:] for i in indexes]

def iterate_gold(line):
    m = 0

    # Find the max prefix digit for a 12-char string
    md = max(int(line[i]) for i in range(0,len(line)-12))

    # From max digit and working down, find smallest possible substring with largest possible prefixes
    prefix = ""
    candidate = line
    for digit in range(md, 0, -1):
        lines = digit_prefixed_substrings(line, str(digit))
        if lines:
            prefix += str(digit)
            candidate = lines[0][1:]

    if len(line) > len(prefix+candidate):
        print(f"Error: {prefix+candidate} longer than {line}!")
        return 0

    print(prefix,candidate)
    
    return max(int(''.join(s)) for s in itertools.combinations(prefix+candidate, 12))


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

