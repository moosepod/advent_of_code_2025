import time
import argparse
import re
import itertools

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

###
### POINTS
###
def padd(p1: Point, p2: Point) -> Point:
    return (p1[X] + p2[X], p1[Y] + p2[Y])

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

# Cardinal directions and their reverse
NESW = (DIRECTIONS["N"], DIRECTIONS["E"], DIRECTIONS["S"], DIRECTIONS["W"])
SWNE = (DIRECTIONS["S"], DIRECTIONS["W"], DIRECTIONS["N"], DIRECTIONS["E"])

# Misc constant
LABEL_OFFSET = -2

def load_grid(path: str) -> SizedGrid:
    g = {}
    width = 0
    height = 0
    with open(path) as f:
        s = f.read()
        for y, row in enumerate(s.split("\n")):
            if row:
                height += 1
                for x, c in enumerate(row):
                    g[(x,y)] = c
                    if x > width:
                        width = x
    return g, (width+1,height)

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

def solve_silver(grid,size):
    locations = []
    for x in range(0,size[WIDTH]):
        for y in range(0,size[HEIGHT]):
            p: Point = (x,y)
            if grid.get(p) == '@':
                locations.append((p, len([p2 for p2 in DIRECTIONS.values() if grid.get(padd(p,p2)) == '@'])))

    return [location for location in locations if location[1] < 4]

def solve_gold(grid,size):
    removed = []
    while True:
        locations = [(p,c) for p,c in solve_silver(grid,size) if c < 4]
        if not locations:
            return removed
        p,_ = locations[0]
        grid[p] = '.'
        removed.append(p)
    
    return []

def solve(solve_f, path="day_4/inputs/input.txt"):
    grid, size = load_grid(path)
    lines = []
    t = time.time()
    locations = solve_f(grid,size)
    a = len(locations)
    
    print(f"Answer: {a} in {time.time() - t:.2f}s")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("star")
    args = parser.parse_args()
    if args.star == "silver":
        solve(solve_silver)
    elif args.star == "gold":
        solve(solve_gold)
    else:
        print("First argument must be silver or gold")

