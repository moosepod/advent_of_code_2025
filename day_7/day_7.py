
import math
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

def propogate(grid, size, beam_x, beam_y,seen):
    if beam_x < 0 or beam_x > size[WIDTH] or beam_y >= size[HEIGHT]:
        return 0
    
    p = (beam_x, beam_y)
    if seen.get(p):
        return 0
    
    seen[p] = True
    
    if grid[p] == '^':
        return propogate(grid, size, beam_x-1, beam_y+1,seen) + propogate(grid, size, beam_x+1, beam_y+1,seen) + 1

    return propogate(grid, size, beam_x, beam_y+1,seen)    


def draw_beams(grid, size, beam_x, beam_y,seen):
    if beam_x < 0 or beam_x > size[WIDTH] or beam_y >= size[HEIGHT]:
        return 1
    
    p = (beam_x, beam_y)
    if seen.get(p):
        return 0
    
    seen[p] = True
    
    if grid[p] == '^':
        grid[(beam_x-1,beam_y)] = '|'
        grid[(beam_x+1,beam_y)] = '|'        
        draw_beams(grid, size, beam_x-1, beam_y+1,seen)
        draw_beams(grid, size, beam_x+1, beam_y+1,seen)
    else:
        grid[(beam_x,beam_y)] = '|'                
        draw_beams(grid, size, beam_x, beam_y+1,seen)

def count_timelines(grid, size, x,y, visited={}):
    count = 0

    if visited.get((x,y)) is not None:
        return visited[(x,y)]

    if grid.get((x-1,y)) == '^':
        count += count_timelines(grid, size, x-1,y-1)
    if grid.get((x+1,y)) == '^':
        count += count_timelines(grid, size, x+1,y-1)
    if grid.get((x,y-1)) == '|':
        count += count_timelines(grid, size, x,y-1)        
    elif grid.get((x,y-1)) == 'S':
        count +=1

    visited[(x,y)] = count
    
    return count

def solve_part_1(grid,size,start,max_y=0):
    seen = {}
    a = propogate(grid,size,start[X], 1, seen)
    #print(dump_grid(grid,size))
    return a

def solve_part_2(grid,size,start,max_y=0):
    seen = {}
    grid[start] = 'S'
    draw_beams(grid,size,start[X], 1,seen)
    count = 0
    for x in range(0, size[WIDTH]):
        if grid[(x,size[HEIGHT]-1)] == '|':
            count += count_timelines(grid, size, x,size[HEIGHT]-1)
    
    return count

def solve(solve_f, path="day_7/inputs/input.txt"):
    grid, size = load_grid(path)
    start = [p for p,c in grid.items() if c == 'S']
    
    lines = []
    t = time.time()
    a = solve_f(grid,size, start[0])
    
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

