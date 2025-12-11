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

def count_paths_bfs(graph, from_device, to_device):
    counter = 0
    Q = queue.Queue()
    Q.put(from_device)
    while not Q.empty():
        device = Q.get()
        if device == to_device:
            counter += 1
        else:
            for edge in graph.get(device):
                Q.put(edge)
                    
    return counter

            
def solve_part_1(path="day_11/inputs/input.txt"):
    t = time.time()
    graph = load_graph(path)
    a = count_paths_bfs(graph, "you","out")
    print(f"Answer: {a} in {time.time() - t:.2f}s")

def solve_part_2(path="day_11/inputs/input.txt"):
    # Notes:
    # - path from every node to out
    # - 608 devices
    # - break into paths to fft and paths to dac
    # - no point in visiting a path if it doesn't hit out (though i'm not getting there)
    t = time.time()
    graph = load_graph(path)
    graph["out"] = []

    counter = Counter()
    stops = {}
    print(count_paths_bfs(graph, "svr","out"))
    return
    find_paths(graph, "srv","out", counter, ["fft","dac"])
    
    print(f"Answer: {counter.c} in {time.time() - t:.2f}s")


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

