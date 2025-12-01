def main(path="day_1/inputs/silver.txt"):
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
    
    

if __name__ == "__main__":
    main()
