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

def area(rect):
    ul,lr = rect[0],rect[2]
    return (abs(ul[X] - lr[X])+1) * (abs(ul[Y] - lr[Y])+1)

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

def center(rect):
    ul, _, lr, _ = rect
    return (ul[X] + ((lr[X] - ul[X])//2), ul[Y] + ((lr[Y] - ul[Y])//2))

def valid_rect_old(rect, lines, points):
    for p in rect:
        if p in points:
            continue
        l = len([x for x in lines[p[Y]] if p[X] <= x])
        print(p, l, lines[p[Y]])
        if l % 2 == 0:
            return False

    return True

def valid_rect(rect, lines, points):
    ul, _, lr, _ = rect
    for y in range(ul[Y],lr[Y]+1):
        # Check that rect is fully within the shape
        if lines[y]:
            x1,x2 = lines[y][0], lines[y][-1]
            if ul[X] < x1 or ul[X] > x2 or lr[X] < x1 or lr[X] > x2:
                return False
                
                
            #l = len([x for x in lines[y] if x >= ul[X] and x <= lr[X]])
            #print(y,l, lines[y])
            #if l != 2:
            #    return False

    return True

def solve_part_2(path="day_9/inputs/input.txt"):
    # Go through each polygon, largest first
    # If there are any vertical lines that start or end, invalid
    t = time.time()
    points = []
    with open(path) as f:
        for line in f:
            points.append(tuple([int(x) for x in line.strip().split(',')]))

    #grid = {}
    #for p in points:
    #    grid[p] = '#'
    #print(dump_grid(grid,(15,15)))
    #print()
    
    # Turn into polygon
    polygon = []
    for i in range(0,len(points)-1):
        line = (points[i],points[i+1])
        polygon.append(line)
    polygon.append((points[-1],points[0]))
    # List of lines for each line

    bounds = ((min(p[X] for p in points),min(p[Y] for p in points)),
              (max(p[X] for p in points),min(p[Y] for p in points)),
              (max(p[X] for p in points),max(p[Y] for p in points)),
              (min(p[X] for p in points),max(p[Y] for p in points)))

    lines = []
    for y in range(0, bounds[2][Y]+1):
        line = []
        for p1,p2 in polygon:
            ty,by = p1[Y],p2[Y]
            if by < ty:
                ty, by = by, ty
            if ty == by and ty == y:
                line.append(p1[X])
                line.append(p2[X])
            elif y >= ty and y <= by:
                line.append(p1[X])
                #print(">>>HERE", y, p1[X])
        line = list(set(line))
        line.sort()        
        lines.append(line)
                
    print("Calculated",len(lines))

    #grid = {}
    #for y,ps in enumerate(lines):
    #    for x in ps:
    #        grid[(x,y)] = '#'
    #print(dump_grid(grid,(15,15)))

    # Build rects 
    rects = set()
    for p1, p2 in itertools.combinations(points,2):
        ul = min(p1[X],p2[X]),min(p1[Y],p2[Y])
        lr = max(p1[X],p2[X]),max(p1[Y],p2[Y])
        rect = (ul, (lr[X],ul[Y]), lr, (ul[X],lr[Y]))
        rects.add((area(rect), rect))

    bounds = ((min(p[X] for p in points)-1,min(p[Y] for p in points)-1),
              (max(p[X] for p in points)+1,min(p[Y] for p in points)-1),
              (max(p[X] for p in points)+1,max(p[Y] for p in points)+1),
              (min(p[X] for p in points)-1,max(p[Y] for p in points)+1))

    rects = list(rects)
    rects.sort(key=lambda x:x[0], reverse=True)
    #rects = [(24, ((2,3),(9,3),(9,5),(3,5)))]
    for a, rect in rects:
        #print("Testing:",a)
        if valid_rect(rect, lines, points):
            print(f"Answer: {a} ({rect}) in {time.time() - t:.2f}s")
            return
                
    print("None found")
    return

    # Sort rects by size

    max_area = max(area(rect) for rect in rects)
    print(f"Answer: {max_area} in {time.time() - t:.2f}s")

    """
    print("Points:",len(points))
    print("Points**4:",len(points)**4)    
    print("Rects:",len(rects))
    print("Max area:",max(area(rect) for rect in rects))    
    print("Min area:",min(area(rect) for rect in rects))
    
    print("Max width:",max(abs(rect[0][X] - rect[2][X]) for rect in rects))
    print("Max height:",max(abs(rect[0][Y] - rect[2][Y]) for rect in rects))

    
    print("Min x:",min(rect[0][X] for rect in rects))
    print("Min y:",min(rect[0][Y] for rect in rects))    
    print("Max x:",max(rect[2][X] for rect in rects))
    print("Max y:",max(rect[2][Y] for rect in rects))    
    """

    
    
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

