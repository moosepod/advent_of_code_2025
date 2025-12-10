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

def valid_rect_size(grid, ul, lr): 
    a = 0
    for x in range(ul[X],lr[X]+1):
        for y in range(ul[Y],lr[Y]+1):
            if grid.get((x,y)) in ('#','X'):
                a+=1
            else:
                return 0

    return a

# https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/

def count_intersections(polygon, p):
    count = 0

    for p1,p2 in polygon:
        if p1[X] == p2[X]:
            if p[Y] >= p1[Y] and p[Y] <= p2[Y]:
                count += 1
                print(p,"intersects on Y",p1,p2)
        else:
            if p1[Y] == p2[Y]:
                if p[X] >= p1[X] and p[X] <= p2[X]:
                    count += 1
                    print(p,"intersects on X",p1,p2)                    
    
    return count

def is_horizontal(line):
    return line[0][Y] == line[1][Y]

def is_vertical(line):
    return line[0][X] == line[1][X]

def point_on_line(p, line):
    if is_vertical(line):
        y1,y2 = line[0][Y],line[1][Y]
        if y2 < y1:
            y1,y2 = y2,y1
            
        if p[X] == line[0][X] and p[Y] >= y1 and p[Y] <= y2:
            return True
        
        return False

    if is_horizontal(line):    
        x1,x2 = line[0][X],line[1][X]
        if x2 < x1:
            x1,x2 = x2,x1
            
        if p[Y] == line[0][Y] and p[X] >= x1 and p[X] <= x2:
            return True
        
        return False
    
    return False

def point_to_right(p, line):
    if is_horizontal(line):
        return False # only check vertical

    if p[X] < line[0][X]:
        return False # point to left of line

    y1,y2 = line[0][Y],line[1][Y]
    if y2 < y1:
        uy1,y2 = y2,y1
    
    if p[Y] < y1 or p[Y] > y2:
        return False # Above/below

    return True

def check_point_in_polygon(p,polygon):
    intersection_count = 0
    for line in polygon:
        if point_on_line(p,line):
            return 1

        if point_to_right(p, line):
            intersection_count += 1

    return intersection_count > 0 and intersection_count % 2 == 1    
        
def solve_part_2(path="day_9/inputs/test.txt"):
    # Treat lines as a polygon
    # From each edge of the space, find the first intersection with a line
    # TRY THIS IDEA: does any line from UL to LR intersect any line of the polygon. If so, throw it out!
    grid = {}
    size = (0,0)

    # Load points
    points = []
    with open(path) as f:
        for line in f:
            points.append(tuple([int(x) for x in line.strip().split(',')]))

    # Reset origin to 0,0
    origin = (min(p[X] for p in points),min(p[Y] for p in points))
    points = [(p[X]-origin[X], p[Y]-origin[Y]) for p in points]
    bounds = ((min(p[X] for p in points),min(p[Y] for p in points)),(max(p[X] for p in points),max(p[Y] for p in points)))
    print("Bounds:",bounds)

    # Turn into polygon
    polygon = []
    for i in range(0,len(points)-1):
        polygon.append((points[i],points[i+1]))

    polygon.append((points[0],points[-1]))
    size = padd((1,1),bounds[1])
    for p1,p2 in polygon:
        draw_line(grid, size, p1,p2)
        grid[p1] = '#'
        grid[p2] = '#'

    print(dump_grid(grid,size))

    # Remove the edges on the bounds
    new_polygon = []
    for p1,p2 in polygon:    
        if p1[X] == p2[X]:
            if p1[X] == 0 or p1[X] == size[X]:
                continue
        if p1[Y] == p2[Y]:
            if p1[Y] == 0 or p1[Y] == size[Y]:
                continue
        new_polygon.append((p1,p2))

    print()
    grid = {}
    for p1,p2 in new_polygon:
        draw_line(grid, size, p1,p2)
        grid[p1] = '#'
        grid[p2] = '#'
    print(dump_grid(grid,size))
    return

    #print("Generating rects from",len(points),"points")    
    rects = set()
    for p1, p2 in itertools.combinations(points,2):
        ul = (min(p1[X],p2[X]), min(p1[Y],p2[Y]))
        lr = (max(p1[X],p2[X]), max(p1[Y],p2[Y]))
        rects.add((ul,(ul[X], lr[Y]), lr, (lr[X], ul[Y])))

    #rects = [((2,3), (9,3), (2,5),(9,5))]

    # Check "winning" rect and see if it makes sense?
    #print("Checking intersections for",len(rects),"rects")
    # Too high: 3044300328
    # Too high 2970174461
    # too large
    max_area = 0
    for idx,verticies in enumerate(rects):
        if idx % 1000 == 0:
            print("Checking",idx,"of",len(rects))
        expected_area = (abs(verticies[0][X]-verticies[2][X])+1) * (abs(verticies[0][Y]-verticies[2][Y])+1)
        fill_area = flood_fill_count(verticies, polygon)
        if fill_area == expected_area:
            if expected_area > max_area:
                max_area = expected_area

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

