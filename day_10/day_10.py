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

def sub_joltages(j1,j2):
    return [j1[i] - j2[i] for i in range(0, len(j1))]

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
        
    print(f"Answer: {a} in {time.time() - t:.2f}s")

def joltage_exceeded(a, b):
    for i in range(0,len(a)):
        if a[i] > b[i]:
            return True

    return False
    

def apply_matches(matching, joltage, target_joltage):
    pressed = 0
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

def find_min_joltage_idx(joltages):
    l = [j for j in joltages if j]
    if not l:
        return []
    return [i for i in range(0, len(joltages)) if joltages[i] == min(l)]

def solve_joltages_tmp(joltages, buttons, state, target_state, count=0):
    if sum(joltages) == 0:
        if state == target_state:
            return count
        return None
    
    # Find the lowest non-zero joltages
    indexes = find_min_joltage_idx(joltages)
    if not indexes:
        if state == target_state:        
            return count
        return None

    min_count = None
    
    for button in buttons:
        if sum([button.joltages[i] for i in range(0,len(joltages)) if i in indexes]) == len(indexes):
            pressed_joltages = joltages.copy()
            press_count = joltages[indexes[0]]
            pressed_state = state
            for i in range(0, press_count):
                pressed_state = pressed_state ^ button.mask                
                pressed_joltages = sub_joltages(pressed_joltages, button.joltages)
            pressed_buttons = [b for b in buttons if b.mask != button.mask]
            new_count = solve_joltages(pressed_joltages, pressed_buttons, pressed_state, target_state, count+press_count)
            if new_count:
                if min_count is None or new_count < min_count:
                    min_count = new_count

    return min_count

def solve_joltages(joltages, buttons, target_state, state, count = 0):
    # Do we need to re-sort every pass through?
    # joltages could change
    if min(joltage.keys()) < 0:
        # Have pressed too many times
        return None
    if len(joltages) == 0:
        if state == target_state:
            return count
        return None

    min_count = None
    for press_count, button_indexes in joltages:
        for idx in button_indexes:
            button = buttons[idx]
            pressed_joltages = joltages.copy()
            pressed_state = state

            # Handle pressing the button
            for i in range(0, press_count):
                pressed_state = pressed_state ^ button.mask

            

                t = []
                for k,v in pressed_voltages:
                    if idx in v:
                        t[k--] = v
                    else:
                        t[k] = v
                pressed_voltages = t
                        
            c = solve_joltages(pressed_joltages, buttons, target_state, pressed_state, count + press_count)
            if min_count is not None and c is not None and c < min_count:
                min_count = c
        
    return min_count

def group_and_sort_joltages(joltages):
    grouped_joltages = {}
    for idx, joltage in enumerate(joltages):
        if grouped_joltages.get(joltage) is None:
            grouped_joltages[joltage] = []
        grouped_joltages[joltage].append(idx)

    target_joltages = list(grouped_joltages.items())
    target_joltages.sort(key=lambda x: x[0])
    return target_joltages
    
def solve_part_2(path="day_10/inputs/test.txt"):
    t = time.time()

    # NOTES FOR REDO OF SOLVE
    # Generate state object -- has target joltages, current state, current count
    # Sort joltages each passthrough
    # Check joltages/state:
    # - joltages all 0 and state matches, valid.
    # - joltages all 0 and state doesn't match, invalid
    # - any joltage below 0, invalid
    # Can't see any reason this won't work? Combinatorics shouldn't be too bad?

    machines = load_machines(path)    
    
    # Find the buttons that affect this number
    # Press these buttons N times
    # Find the next lowest number
    # 2801, too low
    # 3143, too low

    a = 0
    for machine in machines:
        # Sort targets by joltage
        # Group targets into identical joltages
        target_joltages = group_and_sort_joltages(machine.joltages)
        
        print(bits_to_lights(machine.target))
        presses = solve_joltages(target_joltages, machine.buttons, machine.target, 0)
        assert presses
        print(">>>", presses)
        a += presses

    print(f"Answer: {a} in {time.time() - t:.2f}s")
    
    return
    
    a = 0
    error = 0
    for machine in machines:
        print(bits_to_lights(machine.target))
        presses = solve_joltages(0,machine.target,machine.buttons, machine.joltages)
        if presses is None or presses < 0:
            print("... not found")
            error += 1
        else:
            print("...",presses)


        a += presses

    print(error,"errors out of",len(machines))
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

