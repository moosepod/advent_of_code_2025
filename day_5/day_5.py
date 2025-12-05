import argparse

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

