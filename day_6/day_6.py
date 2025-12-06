""" Not thrilled with solution for this one. Got to be a simpler way to do it """

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

def solve_part_1(path="day_6/inputs/test.txt"):
    t = time.time()
    problems = []
    answers = []

    with open(path) as f:
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

    for problem in problems:
        if problem.operator == '*':
            answers.append(math.prod(int(x) for x in problem.numbers))
        else:
            answers.append(sum(int(x) for x in problem.numbers))
    a = sum(answers)
    print(f"Answer: {a} in {time.time() - t:.2f}s")    

def solve_part_2(path="day_6/inputs/input.txt"):
    a = 0
    t = time.time()
    with open(path) as f:
        lines = [l.replace("\n","") for l in f]
        rows, operator_s = lines[:-1],lines[-1]
        columns = []

        index = 0
        for o,p in re.findall(r"([*+])(\s+)", operator_s):
            columns.append((index, index+len(p),math.prod if o == '*' else sum))
            index += len(p)+1

        for start_idx, end_idx, o in columns:
            calculation = 0

            ns = []
            
            for i in range(start_idx,end_idx+1):
                n = ""
                for row in rows:
                    try:
                        d = int(row[i])
                        n += row[i]
                    except ValueError:
                        pass
                if n:
                    ns.append(n)

            a += o(int(x) for x in ns)

    print(f"Answer: {a} in {time.time() - t:.2f}s")
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("part")
    args = parser.parse_args()
    if args.part == "1":
        solve_part_1()
    elif args.part == "2":
        solve_part_2()
    else:
        print("First argument must be 1 or 2")

