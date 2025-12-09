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

def draw_line(grid,size, p1, p2):
    if p1[Y] == p2[Y]:
        x1,x2 = p1[X],p2[X]
        if x2 < x1:
            x1,x2 = x2,x1
        for x in range(x1,x2+1):
            grid[(x,p1[Y])] = 'X'
    elif p1[X] == p2[X]:
        y1,y2 = p1[Y],p2[Y]
        if y2 < y1:
            y1,y2 = y2,y1
        for y in range(y1,y2+1):
            grid[(p1[X]),y] = 'X'

    grid[p1] = '#'
    grid[p2] = '#'

def update_size(size, p1, p2):
    # Adjust size
    if p1[X] > size[X]:
        size = p1[X]+1,size[Y]
    if p2[X] > size[X]:
        size = p2[X]+1,size[Y]
    if p1[Y] > size[Y]:
        size = size[X], p1[Y]+1
    if p2[Y] > size[Y]:
        size = size[X], p2[Y]+1

    return size
    
def solve_part_2(path="day_9/inputs/test.txt"):
    t = time.time()

    grid = {}
    size = (0,0)

    points = []
    with open(path) as f:
        for line in f:
            points.append(tuple([int(x) for x in line.strip().split(',')]))

    for i in range(0, len(points)-1):
        p1,p2 = points[i],points[i+1]
        size = update_size(size, p1,p2)
        draw_line(grid, size, p1,p2)

    draw_line(grid,size, points[0], points[-1])
            
    print(dump_grid(grid,size))
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

