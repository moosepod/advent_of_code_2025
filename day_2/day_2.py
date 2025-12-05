import argparse
import re
import itertools

def iterate_part_1(id1,id2):
    return [n for n in range(id1,id2+1) if str(n)[0:len(str(n))//2] == str(n)[len(str(n))//2:]]

def iterate_part_2(id1,id2):
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
    parser.add_argument("part")
    args = parser.parse_args()
    if args.part == "1":
        solve(iterate_part_1)
    elif args.part == "2":
        solve(iterate_part_2)
    else:
        print("First argument must be 1 or 2")

