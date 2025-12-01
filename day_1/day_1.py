import argparse

def iterate_silver(dial, count, direction, amount):
    dial = (dial + (amount * direction)) % 100
    if dial == 0:
        count += 1

    return dial, count

def iterate_gold(dial, count, direction, amount):
    initial_dial = dial
    dial += amount * direction
    if dial <= 0 and initial_dial != 0:
        count += 1
    count += int(abs(dial)/100)
    dial = dial % 100
    return dial, count
                
    print(f"Final dial: {dial}")                    
    print(f"Answer: {count}")


def solve(iterate_f, path="day_1/inputs/input.txt", initial_dial=50):
    dial = 50
    count = 0
    with open(path) as f:
        for line in f.read().split("\n"):
            if line:
                amount = int(line[1:])            
                direction = 1 if line[0] == 'R' else -1
                dial, count = iterate_f(dial, count, direction, amount)

    print(f"Final dial: {dial}")                    
    print(f"Answer: {count}")

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

