import math
import queue
import time
import argparse
import re
import itertools
from dataclasses import dataclass

def load_graph(path):
    graph = {}
    with open(path) as f:
        for line in f:
            m = re.match(r"^(.+): (.+)$", line.strip())
            if m:
                device = m.group(1)
                graph[device] = m.group(2).split(" ")

    return graph

def count_paths_bfs(graph, from_device, to_device, valid=None):
    if not valid:
        valid = {k:True for k in graph.keys()}
    valid[to_device]=True
    counter = 0
    Q = queue.Queue()
    Q.put(from_device)
    while not Q.empty():
        device = Q.get()
        if device == to_device:
            counter += 1
        else:
            for edge in graph.get(device):
                if valid.get(edge):
                    Q.put(edge)
                    
    return counter

def find_paths_bfs(graph, from_device, to_device, valid=None):
    if not valid:
        valid = {k:True for k in graph.keys()}
    valid[to_device]=True
    
    paths = []
    counter = 0
    Q = queue.Queue()
    Q.put((from_device, [from_device]))
    while not Q.empty():
        device, path = Q.get()
        if device == to_device:
            paths.append(path)
        else:
            for edge in graph.get(device):
                if valid.get(edge):
                    Q.put((edge, path+[edge]))
                    
    return paths

def path_exists(graph, from_device, to_device, valid=None):
    visited = set()
    visited.add(from_device)
    Q = queue.Queue()
    Q.put(from_device)
    while not Q.empty():
        device = Q.get()
        if device == to_device:
            return True
        else:
            for edge in graph.get(device):
                if not edge in visited:
                    visited.add(edge)
                    if not valid or not valid.get(edge):
                        Q.put(edge)
                    
    return False

            
def solve_part_1(path="day_11/inputs/input.txt"):
    t = time.time()
    graph = load_graph(path)
    a = count_paths_bfs(graph, "you","out")
    print(f"Answer: {a} in {time.time() - t:.2f}s")

def solve_part_2(path="day_11/inputs/test.txt"):
    # Notes:
    # - path from every node to out
    # - 608 devices
    # - break into paths to fft and paths to dac
    # - no point in visiting a path if it doesn't hit out (though i'm not getting there)
    # - Finding paths to fft limits to only 93
    # - After research no paths visit dac before fft
    
    t = time.time()
    graph = load_graph(path)
    graph["out"] = []

    # Identify nodes that lead fft
    valid_fft = {}
    for device in graph.keys():
        fft = path_exists(graph, device, "fft")
        if fft:
            valid_fft[device] = True    

    # Find all paths to fft
    fft_paths = find_paths_bfs(graph, "svr","fft",valid_fft)
    print(len(fft_paths),"fft paths found")

    # Find valid paths to dac
    valid_dac = {}
    for device in graph.keys():
        if path_exists(graph, device, "dac"):
            valid_dac[device] = True    
    
    # Remove any previously visited devices from valid_dac
    valid_dac = {d:True for d in valid_dac.keys() if d not in fft_paths}
    
    # Find how many of these have already visited dac
    dac_paths = find_paths_bfs(graph,"fft","dac", valid_dac)        
    print(len(dac_paths),"fft/dac paths found")    


    # Finally, find paths to out, excluding any previously visited nodes
    valid = {k: True for k in graph.keys()}
    valid = {d:True for d in valid.keys() if d not in fft_paths}
    valid = {d:True for d in valid.keys() if d not in dac_paths}

    paths = find_paths_bfs(graph,"dac","out", valid)
    print(len(paths),"fft/dac.out paths found")        

    return

    valid = {}
    for device in graph.keys():
        fft = path_exists(graph, device, "fft")
        #dac = path_exists(graph, device, "dac")
        if fft:
            valid[device] = True

    print(len(valid),"of",len(graph), "have path")

    print(count_paths_bfs(graph, "svr","fft",valid))
    #print(count_paths_bfs(graph, "fft","out",None))

    c = 0
    print(f"Answer: {c} in {time.time() - t:.2f}s")


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

