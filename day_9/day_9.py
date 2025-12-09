import math
import time
import argparse
import re
import itertools
from dataclasses import dataclass

def solve_part_1(path="day_9/inputs/test.txt"):
    t = time.time()

    a = 0
    print(f"Answer: {a} in {time.time() - t:.2f}s")    

def solve_part_2(path="day_9/inputs/test.txt"):
    t = time.time()

    a = 0
    print(f"Answer: {a} in {time.time() - t:.2f}s")    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part")
    args = parser.parse_args()
    if args.part == "1":
        solve_part_1()
    elif args.part == "2":
        solve_part_2()
    else:
        print("First argument must be 1 or 2")

