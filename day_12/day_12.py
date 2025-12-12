

import math
import queue
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

LABEL_OFFSET = -2

DIRECTIONS = {
    "NE": (1,-1), 
    "E": (1,0), 
    "SE": (1,1), 
    "S": (0,1), 
    "SW": (-1,1), 
    "W": (-1,0), 
    "NW": (-1,-1), 
    "N": (0,-1), 
    }

NESW = (DIRECTIONS["N"], DIRECTIONS["E"], DIRECTIONS["S"], DIRECTIONS["W"])

def padd(p1: Point, p2: Point) -> Point:
    return (p1[X] + p2[X], p1[Y] + p2[Y])

def psub(p1: Point, p2: Point) -> Point:
    return (p1[X] - p2[X], p1[Y] - p2[Y])

@dataclass
class Region:
    size: Size
    targets: list[int]
    
@dataclass
class Puzzle:
    presents: list[list[dict]]
    regions: list[Region]

def dump_grid(grid: Grid, size: Size, message: str="", int_grid=False, extra:dict[Point,str] = None, labels=False) -> str:
    s = message
    for row in range(LABEL_OFFSET if labels else 0,size[1]):
        if s:
            s+="\n"
        for col in range(LABEL_OFFSET if labels else 0,size[0]):
            c = (extra or {}).get((col,row))
            if c is None:
                c = grid.get((col,row))
            if int_grid:
                if c is not None:
                    if c >= 0 and c <= 10:
                        c = chr(48+c)
                    else:
                        c = "?"
            s+=str(c) if c is not None else '.'
    return s

def rotate(puzzle):
    return {(2,0): puzzle.get((0,0)),
            (2,1): puzzle.get((1,0)),
            (2,2): puzzle.get((2,0)),
            (1,0): puzzle.get((0,1)),
            (1,1): puzzle.get((1,1)),
            (1,2): puzzle.get((2,1)),
            (0,0): puzzle.get((0,2)),
            (0,1): puzzle.get((1,2)),
            (0,2): puzzle.get((2,2))}                                                                                                                                          

def load_puzzle(path):
    puzzle = Puzzle(presents=[], regions=[])
    y = 0
    with open(path) as f:
        for line in f:
            if m := re.match(r"^(\d+)x(\d+):\s+([\d ]+)",line):
                w,h,s = m.groups()
                puzzle.regions.append(Region(size=(int(w),int(h)), targets=[int(x) for x in s.split(' ')]))
            elif m := re.match(r"^(\d+):",line):
                y = 0
                puzzle.presents.append([{}])
            elif m := re.match(r"^([#.]+)", line):
                for x,c in enumerate(m.group(1)):
                    if c == '#':
                        puzzle.presents[-1][-1][(x, y)] = "#"
                y+=1

    for presents in puzzle.presents:
        for i in range(0,3):
            presents.append(rotate(presents[-1]))
                    
    return puzzle

def solve_part_1(path="day_12/inputs/test.txt"):
    # Pre-calcuate all rotations
    t = time.time()
    puzzle = load_puzzle(path)
    for idx, presents in enumerate(puzzle.presents):
        print(">>>>",idx)        
        for present in presents:
            print(dump_grid(present, (3,3)))
            print()
    for region in puzzle.regions:
        print(region)
    a = 0
    print(f"Answer: {a} in {time.time() - t:.2f}s")   

def solve_part_2(path="day_12/inputs/test.txt"):
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
