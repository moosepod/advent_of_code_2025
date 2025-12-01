import argparse

def solve_silver(path="day_1/inputs/input.txt"):
    dial = 50
    count = 0
    with open(path) as f:
        for line in f.read().split("\n"):
            if line:
                direction = 1 if line[0] == 'R' else -1
                amount = int(line[1:])
                dial = (dial + (amount * direction)) % 100
                if dial == 0:
                    count += 1

    print(f"Final dial: {dial}")
    print(f"Answer: {count}")

def solve_gold(path="day_1/inputs/input.txt"):
    dial = 50
    count = 0
    with open(path) as f:
        for line in f.read().split("\n"):
            if line:
                initial_dial = dial
                direction = 1 if line[0] == 'R' else -1
                amount = int(line[1:])
                dial += amount * direction
                if dial <= 0 and initial_dial != 0:
                    count += 1
                count += int(abs(dial)/100)
                dial = dial % 100

                
    print(f"Final dial: {dial}")                    
    print(f"Answer: {count}")    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("star")
    args = parser.parse_args()
    if args.star == "silver":
        solve_silver()
    elif args.star == "gold":
        solve_gold()
    else:
        print("First argument must be silver or gold")

