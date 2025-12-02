import argparse

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
    s = 0
    with open(path) as f:
        for line in f.read().split("\n"):
            if line:
                for pair in line.split(','):
                    id1,id2 = pair.split('-')
                    s += sum(iterate_f(int(id1),int(id2)))

    print(f"Answer: {s}")
        
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

