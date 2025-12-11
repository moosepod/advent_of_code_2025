import math
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

def bfs(graph, device, to, seen, path, paths):
    if device == to:
        paths.add(",".join(path))
        return

    #if device in path:
    #    return

    seen[device] = True

    for device in graph[device]:
        bfs(graph, device, to, seen, path + [device], paths)

def solve_part_1(path="day_11/inputs/input.txt"):
    t = time.time()
    graph = load_graph(path)

    paths = set()
    bfs(graph, "you","out", {}, ["you"], paths)
    #for path in paths:
    #    print(path)
    a = len(paths)
    print(f"Answer: {a} in {time.time() - t:.2f}s")

def solve_part_2(path="day_11/inputs/test.txt"):
    t = time.time()
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

