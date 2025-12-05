import time
import argparse

def solve_part_1(fresh, all):
    count = 0

    for i in all:
        for a,b in fresh:
            if i >= a and i <= b:
                count += 1
                break
    
    return count

def join_ranges(r1,r2):
    """
    >>> join_ranges((1,3),(4,5))
    ([(1, 3), (4, 5)], False)
    >>> join_ranges((4,5),(1,3))
    ([(4, 5), (1, 3)], False)
    >>> join_ranges((1,3),(1,5))
    ([(1, 5)], True)
    >>> join_ranges((1,5),(1,3))
    ([(1, 5)], True)
    >>> join_ranges((2,4),(3,5))
    ([(2, 5)], True)
    >>> join_ranges((3,5),(2,4))
    ([(2, 5)], True)
    >>> join_ranges((1,10),(5,15))
    ([(1, 15)], True)
    >>> join_ranges((1,10),(11,15))
    ([(1, 10), (11, 15)], False)
    >>> join_ranges((16,20),(12,18))
    ([(12, 20)], True)
    
    """
    #print("...comparing",r1,r2)
    a1,b1 = r1
    a2,b2 = r2

    if a1 >= a2 and b1 <= b2:
        return [(a2,b2)], True

    if a2 >= a1 and b2 <= b1:
        return [(a1,b1)], True

    if b1 < a2 :
        return [r1,r2],False

    if a2 > b1:
        return [r1,r2],False

    if a1 > b2:
        return [r1,r2],False        

    return [(min(a1,a2),max(b1,b2))], True        

def compress_ranges(ranges):
    new_ranges = []
    changed = False
    for i in range(0,len(ranges)):
        a1,b1 = ranges[i]
        for j in range(i,len(ranges)):
            if j != i:
                a2,b2 = ranges[j]
                l, r = join_ranges((a1,b1),(a2,b2))
                if r:
                    new_ranges.extend(l)
                    changed = True
                    #print(".....break",l)
                    break
        if not changed:
            new_ranges.append((a1,b1))
        else:
            for x in range(i+1, len(ranges)):
                if x != j:
                    new_ranges.append(ranges[x])
            return new_ranges, True

    return new_ranges, changed

def solve_part_2(fresh, _):
    
    count = 0

    ranges = fresh
    while True:
        new_ranges, changed = compress_ranges(ranges)
        #print(">>>>")
        #print(ranges)
        #print(new_ranges)
        if not changed:
            break
        ranges = new_ranges
    
    return sum(b-a+1 for a,b in ranges)

def solve(solve_f, path="day_5/inputs/input.txt"):
    fresh = []
    all = []
    
    t = time.time()
    with open(path) as f:
        for line in f.read().split("\n"):
            line = line.strip()
            if line:
                if '-' in line:
                    fresh.append([int(x) for x in line.split('-')])
                else:
                    all.append(int(line))

    a = solve_f(fresh, all)
    print(f"Answer: {a} in {time.time() - t:.2f}s")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part")
    args = parser.parse_args()
    if args.part == "1":
        solve(solve_part_1)
    elif args.part == "2":
        solve(solve_part_2)
    else:
        print("First argument must be 1 or 2")

