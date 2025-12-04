import time
import argparse
import re
import itertools

def iterate_silver(line):
    return max(int(''.join(s)) for s in itertools.combinations(line, 2))

def collapse(line):
    """
    >>> collapse('987654321111111')
    '987654321111'
    >>> collapse('1111111123456789')
    '111123456789'
    >>> len(collapse('1111111123456789'))
    12
    >>> collapse('811111111111119')
    '811111111119'
    >>> collapse('877777777777779')
    '877777777779'
    >>> collapse('8799777777777779')
    '997777777779'
    >>> collapse('234234234234278')
    '434234234278'
    >>> collapse('818181911112111')
    '888911112111'
    >>> collapse('3221249222232214222222242232122222222221222212322122224211414222112232122223123222213211222222123221') 
    '944444333332'
    >>> collapse('7225271234724212144362411223531221412264267255242242226526263674477422436246415625223811384523523527')
    '884523523527'
    >>> collapse('5293767949955645755355857588665658624753447554647674393995441228558955575465574835453763652875533465') # Issue: run of nines
    '999999998876'
    """
    original_line = line
    result = ""
    while len(result) < 12:        
        right_idx = len(line) - 11 + len(result) 

        left, right = line[0:right_idx],line[right_idx:]
        max_digit = str(max(int(d) for d in left))
        min_digit = str(min(int(d) for d in left))

        done = True
        for i in range(left.index(max_digit), len(left)-1):
            a, b = int(left[i]), int(left[i+1])
            if a > b or (a == b and a != min_digit):
                result += left[i]
                line = line[i+1:]
                done = False
                break
 
        if done:
            result += left[-1] + right
            break
            
    return result

def iterate_gold(line):
    candidate = collapse(line)
    return int(candidate)

def solve(iterate_f, path="day_3/inputs/input.txt"):
    lines = []
    t = time.time()
    with open(path) as f:
        for line in f.read().split("\n"):
            if line:
                lines.append(iterate_f(line))

    a = sum(lines)
    print(f"Answer: {a} in {time.time() - t:.2f}s")
        
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

