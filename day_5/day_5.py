import time
import argparse

def solve_silver(fresh, all):
    count = 0

    for i in all:
        for a,b in fresh:
            if i >= a and i <= b:
                count += 1
                break
    
    return count

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
    parser.add_argument("star")
    args = parser.parse_args()
    if args.star == "silver":
        solve(solve_silver)
    elif args.star == "gold":
        solve(solve_gold)
    else:
        print("First argument must be silver or gold")

