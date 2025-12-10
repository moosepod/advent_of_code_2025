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

def find_candidates(machine):
    candidates = []
    for i in range(1,len(machine.buttons)):
        for p in itertools.combinations(machine.buttons, i):
            joltages = [0] * machine.l
            mask = 0
            for b in p:
                mask = mask ^ b.mask
                for i,j in enumerate(b.joltages):
                    if j == 1:
                        joltages[i] = 1

            #print(joltages,machine.joltages)
            if mask == machine.target and [1 for j in joltages if j] == [1 for j in machine.joltages if j]:
                candidates.append(p)

    return candidates

def add_joltages(j1,j2):
    return [j1[i] + j2[i] for i in range(0, len(j1))]

def add_double_joltages(j1,j2):
    return [j1[i] + (j2[i] * 2) for i in range(0, len(j1))]


def sub_double_joltages(j1,j2):
    return [j1[i] - (j2[i] * 2) for i in range(0, len(j1))]

def minimize_joltage(joltages, target_joltages, machine_buttons):
    # If any joltage over, return 0
    if joltages == target_joltages:
        #print("...found")
        return 1
    
    for i in range(0, len(joltages)):
        if joltages[i] > target_joltages[i]:
            return 0

    # Always press twice to cycle
    for button in machine_buttons:
        new_joltages = add_double_joltages(joltages, button.joltages)
        minimize_joltage(new_joltages, target_joltages, machine_buttons)

    return 0

def button_matching_joltage(target_joltage, button):
    for i in range(0, len(target_joltage)):
        # Button is 1 but target is untoucned
        if button.joltages[i] and not target_joltage[i]:
            return False

    return True

def solve_part_1(path="day_10/inputs/input.txt"):
    t = time.time()
    machines = load_machines(path)

    a = 0
    for machine in machines:
        m = solve_machine(machine)
        a += m                
        #print(bits_to_lights(machine.target), m)

        
    print(f"Answer: {a} in {time.time() - t:.2f}s")

def joltage_exceeded(a, b):
    for i in range(0,len(a)):
        if a[i] > b[i]:
            return True

    return False
    

def apply_matches(matching, joltage, target_joltage):
    pressed = 0
    print(joltage,target_joltage)
    for _, button in matching:
        while True:
            if joltage == target_joltage:
                return pressed
            joltage = add_double_joltages(joltage, button.joltages)
            if joltage_exceeded(joltage, target_joltage):
                #print("Exceeded with:",joltage,"vs",target_joltage)                
                joltage = sub_double_joltages(joltage, button.joltages)
                break # Move onto next match
            
            pressed += 2


def solve_part_2(path="day_10/inputs/test.txt"):
    t = time.time()
    a = 0

    # Any button applied twice is a nop
    # So:
    # - find all combos of single buttons that reach outcome
    # -solve th rest
    
    machines = load_machines(path)
    checked = 0
    for machine in machines:
        candidates = find_candidates(machine)
        min_presses = 10000
        for candidate in candidates:
            pressed = 0
            joltages = [0] * machine.l
            for b in candidate:
                joltages = add_joltages(joltages, b.joltages)
            matching = [(sum([j for j in b.joltages]), b) for b in machine.buttons if button_matching_joltage(machine.joltages, b)]
            matching.sort(key=lambda x: x[0], reverse=True)

            pressed = apply_matches(matching, joltages, machine.joltages)
            if pressed and pressed < min_presses:
                min_presses = pressed
        print(min_presses)

                    
                    
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

