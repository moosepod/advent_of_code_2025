import argparse
import re
import itertools

def iterate_silver():
    pass

def iterate_gold():
    pass

def solve(iterate_f, path="day_2/inputs/input.txt"):
    with open(path) as f:
        for line in f.read().split("\n"):
            if line:
                pass

    a = 0
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

