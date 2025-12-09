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

def flood_fill(grid, size, p,c):
    if grid.get(p) is not None or p[X] < 0 or p[Y] > size[X] or p[Y] < 0 or p[Y] > size[Y]:
        return

    grid[p] = c
    for d in NESW:
        flood_fill(grid, size, padd(p,d), c)

def valid_rect_size(grid, ul, lr): 
    a = 0
    for x in range(ul[X],lr[X]+1):
        for y in range(ul[Y],lr[Y]+1):
            if grid.get((x,y)) in ('#','X'):
                a+=1
            else:
                return 0

    return a
        
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
    flood_fill(grid, size, (points[0][X]+1,points[0][Y]+1),'X')

    rects = set()

    for p1, p2 in itertools.combinations(points,2):
        ul = (min(p1[X],p2[X]), min(p1[Y],p2[Y]))
        lr = (max(p1[X],p2[X]), max(p1[Y],p2[Y]))
        rects.add((ul,lr))
        
    max_area = 0
    rect = (0,0)
    
    for ul,lr in list(rects):
        a = valid_rect_size(grid, ul, lr)
        if a > max_area:
            max_area = a
            rect = (p1,p2)    
            
    #print(dump_grid(grid,size))
    print(f"Answer: {max_area} in {time.time() - t:.2f}s")    

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

