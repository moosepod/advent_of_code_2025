import argparse

def iterate_silver(dial, count, direction, amount):
    pass

def iterate_gold():
    pass

def solve(iterate_f, path="day_2/inputs/input.txt"):
    with open(path) as f:
        for line in f.read().split("\n"):
            pass

    print("Answer will go here")
        
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

