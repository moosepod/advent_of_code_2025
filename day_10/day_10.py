import math
import time
import argparse
import re
import itertools
from dataclasses import dataclass

@dataclass
class Machine:
    lights: str
    buttons: list[list[int]]

def extract_buttons(s):
    buttons = []
    for b in s.split(" "):
        lights = []
        for d in re.findall("(\d+)",b):
            lights.append(int(d))
        buttons.append(lights)

    return buttons
    
def load_machines(path) -> list[Machine]:
    machines = []
    with open(path) as f:
        for line in f:
            if m := re.search(r"^\[([#.]+)\] (\(.+\))", line):
                machines.append(Machine(lights=m.group(1), buttons=extract_buttons(m.group(2))))

    return machines
    
def solve_part_1(path="day_10/inputs/test.txt"):
    t = time.time()
    machines = load_machines(path)
    for machine in machines:
        print(machine)
    a = 0
    print(f"Answer: {a} in {time.time() - t:.2f}s")    

def solve_part_2(path="day_10/inputs/test.txt"):
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

