import math
import time
import argparse
import re
import itertools
from dataclasses import dataclass

type Point = tuple[int,int]
type PointVector = tuple[Point,Point]
type Size = tuple[int,int]

type Rect = tuple[Point,Size]

type Grid = dict[Point,str]

type SizedGrid = tuple[Grid,Size]

# Keys for point/size/rect tuples
WIDTH = 0
HEIGHT = 1
X = 0
Y = 1
P = 0
V = 1

def solve_part_1(path="day_9/inputs/input.txt"):
    t = time.time()
    points = []
    with open(path) as f:
        for line in f:
            points.append([int(x) for x in line.strip().split(',')])

    max_area = 0
    rect = ((0,0),(0,0))

    for p1, p2 in itertools.combinations(points,2):
        w, h = abs(p1[X]-p2[X])+1,abs(p1[Y]-p2[Y])+1
        a = w*h
        if a > max_area:
            max_area = a
            rect = (p1,p2)

    print(rect)
    a = max_area
    print(f"Answer: {a} in {time.time() - t:.2f}s")    

def solve_part_2(path="day_9/inputs/test.txt"):
    t = time.time()

    a = 0
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

