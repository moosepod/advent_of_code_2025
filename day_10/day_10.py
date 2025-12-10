import math
import time
import argparse
import re
import itertools
from dataclasses import dataclass

@dataclass
class Machine:
    target: int
    l: int
    buttons: list[int]


def bits_to_lights(n):
    l = ""
    mask = 0x8000
    while mask:
        l+= "#" if n & mask else "."
        mask = mask >> 1

    return l

def lights_to_bits(l):
    n = 0
    place = 0
    for i in range(len(l)-1, -1, -1):
        if l[i] == '#':
            n |= 1 << place
        place += 1

    return n
    

def extract_buttons(s,l):
    buttons = []
    for b in s.split(" "):
        n = 0
        for d in re.findall(r"(\d+)",b):
            n |= 1 << l-int(d)-1
        buttons.append(n)

    return buttons
    
def load_machines(path) -> list[Machine]:
    machines = []
    with open(path) as f:
        for line in f:
            if m := re.search(r"^\[([#.]+)\] (\(.+\))", line):
                l = len(m.group(1))
                machines.append(Machine(l=l,target=lights_to_bits(m.group(1)), buttons=extract_buttons(m.group(2),l)))

    return machines

def solve_machine(machine):
    for i in range(1,len(machine.buttons)):
        for p in itertools.combinations(machine.buttons, i):
            mask = 0
            for b in p:
                mask = mask ^ b

            if mask == machine.target:
                #print("Hit target with", p,"at",i)
                return i

    return -1

def solve_part_1(path="day_10/inputs/input.txt"):
    t = time.time()
    machines = load_machines(path)

    a = 0
    for machine in machines:
        m = solve_machine(machine)
        a += m                
        #print(bits_to_lights(machine.target), m)

        
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

