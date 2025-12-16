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

def find_paths_bfs(graph, from_device, to_device):
    paths = []
    counter = 0
    Q = queue.Queue()
    Q.put((from_device, [from_device]))
    while not Q.empty():
        device, path = Q.get()
        if device == to_device:
            paths.append(path)
        else:
            assert graph.get(device) is not None,f"{device} not found in graph"            
            for edge in graph.get(device):
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
            for edge in graph[device]:
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

def solve_part_2(path="day_11/inputs/input.txt"):    
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
    fft_graph = {k:v for k,v in graph.items() if valid_fft.get(k)}
    for k,v in fft_graph.items():
        fft_graph[k] = [d for d in v if fft_graph.get(d)]
    fft_paths = find_paths_bfs(fft_graph, "svr","fft")
    print(len(fft_paths),"fft paths found")

    # Find valid paths to dac
    valid_dac = {}
    for device in graph.keys():
        if path_exists(graph, device, "dac"):
            valid_dac[device] = True
    
    # Remove any previously visited devices from valid_dac
    for p in fft_paths:
        for d in p:
            if valid_dac.get(d):
                del valid_dac[d]

    valid_dac["fft"] = True
    dac_graph = {k:v for k,v in graph.items() if valid_dac.get(k)}
    for k,v in dac_graph.items():
        dac_graph[k] = [d for d in v if dac_graph.get(d)]
    
    # Find how many of these have already visited dac
    dac_paths = find_paths_bfs(dac_graph,"fft","dac")
    print(len(dac_paths),"fft->dac paths found")

    # Finally, find paths to out, excluding any previously visited nodes
    valid = {k: True for k in graph.keys()}
    for p in fft_paths:
        for d in p:
            if valid.get(d):
                del valid[d]
    for p in dac_paths:
        for d in p:
            if valid.get(d):
                del valid[d]
    valid["fft"] = True
    valid["dac"] = True
    valid["out"] = True

    out_graph = {k:v for k,v in graph.items() if valid.get(k)}
    for k,v in out_graph.items():
        out_graph[k] = [d for d in v if out_graph.get(d) is not None]

    paths = find_paths_bfs(out_graph,"dac","out")
    print(len(paths),"fft->dac->out paths found")
    c = len(fft_paths) * len(dac_paths) * len(paths)
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

