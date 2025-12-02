import argparse
import re
import itertools

def iterate_silver(id1,id2):
    results = []
    for n in range(id1,id2+1):
        s = str(n)
        l = len(s)
        if l % 2 == 0:
            if s[0:l//2] == s[l//2:]:
                results.append(n)
    return results

def iterate_gold(id1,id2):
    results = []
    for n in range(id1,id2+1):
        s = str(n)
        for l in range(1,len(s)):
            if s == s[0:l] * (len(s)//l):
                results.append(n)
                break
            
    return results

def solve(iterate_f, path="day_2/inputs/input.txt"):
    with open(path) as f:
        s = [iterate_f(int(id1),int(id2)) for id1,id2 in re.findall(r"(\d+)-(\d+)", f.read())]

    a = sum(list(itertools.chain(*s)))

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

