import math
import time
import argparse
import re
import itertools
from dataclasses import dataclass

@dataclass
class Button:
    mask: int
    joltages: list[int]

@dataclass
class Machine:
    target: int
    l: int
    buttons: list[Button]
    joltages: list[int]


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
        joltages = [0] * l
        for c in re.findall(r"(\d+)",b):
            d = int(c)
            n |= 1 << l-d-1
            joltages[d] = 1
        buttons.append(Button(mask=n, joltages=joltages))

    return buttons

def extract_joltages(s):
    return [int(x) for x in s.split(",")]

def load_machines(path) -> list[Machine]:
    machines = []
    with open(path) as f:
        for line in f:
            if m := re.search(r"^\[([#.]+)\] (\(.+\)) {(.+)}", line):
                l = len(m.group(1))
                machine = Machine(l=l,target=lights_to_bits(m.group(1)), buttons=extract_buttons(m.group(2),l),joltages=extract_joltages(m.group(3)))
                assert l == len(machine.joltages)
                machines.append(machine)

    return machines

def solve_machine(machine):
    for i in range(1,len(machine.buttons)):
        for p in itertools.combinations(machine.buttons, i):
            mask = 0
            for b in p:
                mask = mask ^ b.mask

            if mask == machine.target:
                return i

    return -1

def add_joltages(j1,j2):
    return [j1[i] + j2[i] for i in range(0, len(j1))]

def solve_machine_with_joltages(machine, button_sets, index):
    # If lights match and joltages match, return success
    if count > 10:
        return 0
    #print(" " *count,joltages)
    if lights == machine.target and joltages == machine.joltages:
        print("FOUND")
        return count
    
    # If any joltage over, return 0
    for i in range(0, len(joltages)):
        if joltages[i] > machine.joltages[i]:
            return 0

    min_c = 100000
    for button in machine.buttons:
        c = solve_machine_with_joltages(lights ^ button.mask, add_joltages(button.joltages, joltages), machine, count+1)
        if c and c < min_c:
            min_c = c

    return min_c

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

    # Any button applied twice is a nop
    # So:
    # - find a sequence that works
    # - then compare the jolts
    
    machines = load_machines(path)
    for machine in machines:
        # Bucket based on touching a place
        button_sets = []
        for i in range(0, machine.l):
            button_sets.append([])
            for button in machine.buttons:
                if button.joltages[i] == 1:
                    button_sets[-1].append(button)

        # EITHER button set is key OR mods are key
        # Applying twice = same result, but 2+ joltage
        # Anything applied twice _only_ serves to adjust joltage.
        # So optimize to 1,1,1,1 first?
        # So for instance: 2, 4, 3, 6
        m = solve_machine_with_joltages(machine, button_sets, 0)
        #a += m
        break

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

