import math
import time
import argparse
import re
import itertools
from dataclasses import dataclass

@dataclass
class Problem:
    operator: str
    numbers: list[str]



def solve_part_1(problems):
    answers = []

    for problem in problems:
        if problem.operator == '*':
            answers.append(math.prod(int(x) for x in problem.numbers))
        else:
            answers.append(sum(int(x) for x in problem.numbers))
    
    return answers

def solve_part_2(problems):
    return [0]


def solve(solve_f, path="day_6/inputs/test.txt"):
    t = time.time()    
    with open(path) as f:
        problems = []

        for row, line in enumerate(f):
            line = line.strip()
            if line:
                for col, (num,operator) in enumerate(re.findall(r"(\d+)|([+*])", line)):
                    if row == 0:
                        problems.append(Problem(operator=operator, numbers=[num]))
                    else:
                        if operator:
                            problems[col].operator = operator
                        else:
                            problems[col].numbers.append(num)

    a = sum(solve_f(problems))

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

