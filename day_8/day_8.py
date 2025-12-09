import math
import time
import argparse
import re
import itertools
from dataclasses import dataclass

def load(path):
    points = []
    
    with open(path) as f:
        for line in f:
            line = line.strip()
            points.append(tuple([int(x) for x in line.split(',')]))

    return points

def calc_distances(points):
    distances = {}

    for p1 in points:
        for p2 in points:
            if p1 != p2:
                distances[(p1,p2)] = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)



    return distances

def calc_distance(p,c, distances):
    shortest = None

    for tp in c:
        if p != tp:
            d = distances.get((p,tp)) 
            if d is not None:
                if shortest is None or d < shortest[0]:
                    shortest = d, tp
                
    return shortest

def solve_part_1(path="day_8/inputs/input.txt",connections=1000):
    t = time.time( )

    connected = 0

    points = load(path)
    distances = calc_distances(points)
    circuits = [{p} for p in points]

    # Find point with shortest distance to a circuit
    # Find circuit that contains that point
    # Join circuits
    for i in range(0,connections):
        print(i)
        shortest = None

        for p1 in points:
            for c in circuits:
                d_p = calc_distance(p1,c, distances)
                if d_p:
                    d,p2 = d_p
                    if shortest is None or d < shortest[0]:
                        shortest = (d,p1,p2)                        

        _, p1, p2 = shortest
        c1 = [c for c in circuits if p1 in c][0]
        c2 = [c for c in circuits if p2 in c][0]
        #print("Connecting",c1,"and",c2,"with distance",shortest,"via",p1,"->",p2)
        if distances.get((p1,p2)):
            del distances[(p1,p2)]
        if distances.get((p2,p1)):
            del distances[(p2,p1)]
            
        circuits = [c for c in circuits if c not in (c1,c2)]
        circuits.append(c1.union(c2))
    
    results = [(len(list(c)), c) for c in circuits]
    results.sort()
    results = list(reversed(results))


    #print("Connections:",connected)
    #for l,c in results:
    #    print(l,c)

    
    a = results[0][0] * results[1][0] * results[2][0]
    print(f"Answer: {a} in {time.time() - t:.2f}s")    


def solve_part_2(path="day_8/inputs/input.txt"):
    t = time.time( )

    connected = 0

    points = load(path)
    distances = calc_distances(points)
    circuits = [{p} for p in points]

    # Find point with shortest distance to a circuit
    # Find circuit that contains that point
    # Join circuits
    while True:
        connected += 1
        if connected % 10 == 0:
            print("...",connected)
        shortest = None

        for p1 in points:
            for c in circuits:
                d_p = calc_distance(p1,c, distances)
                if d_p:
                    d,p2 = d_p
                    if shortest is None or d < shortest[0]:
                        shortest = (d,p1,p2)                        

        _, p1, p2 = shortest
        c1 = [c for c in circuits if p1 in c][0]
        c2 = [c for c in circuits if p2 in c][0]
        #print("Connecting",c1,"and",c2,"with distance",shortest,"via",p1,"->",p2)
        if distances.get((p1,p2)):
            del distances[(p1,p2)]
        if distances.get((p2,p1)):
            del distances[(p2,p1)]
            
        circuits = [c for c in circuits if c not in (c1,c2)]
        circuits.append(c1.union(c2))
        if len(circuits) == 1:
            answer = p1,p2
            break
    
    print(p1,"->",p2)
    a = p1[0] * p2[0]
    print(f"Answer: {a} in {time.time() - t:.2f}")

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

