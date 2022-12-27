import numpy as np
from collections import Counter, deque, defaultdict
import itertools
from typing import Tuple, List, Dict, Set, final

def read_data(input_path: str) -> np.array:
    with open(input_path, "r") as f:
        data = [[c for c in l.strip()] for l in f.readlines()]
    data = np.array(data, dtype="str")
    return data

def get_next(coord: Tuple[int, int], grid: np.array):
    if grid[coord] == ">":
        if coord[1] < grid.shape[1] - 1:
            next_coord = (coord[0], coord[1] + 1)
        else:
            next_coord = (coord[0], 0)
    elif grid[coord] == 'v':
        if coord[0] < grid.shape[0] - 1:
            next_coord = (coord[0] + 1, coord[1])
        else:
            next_coord = (0, coord[1])
    else:
        return None
    return next_coord

def update(current: np.array) -> np.array:
    previous = current.copy()
    # First pass: east bois
    for i, j in np.argwhere(previous == ">"):
        next_coord = get_next((i, j), previous)
        if previous[next_coord] == ".":
            current[i, j] = "."
            current[next_coord] = ">"
    previous = current.copy()
    # Second pass: south bois
    for i, j in np.argwhere(previous == "v"):
        next_coord = get_next((i, j), previous)
        if previous[next_coord] == ".":
            current[i, j] = "."
            current[next_coord] = "v"

def check_terminal(data: np.array) -> int:
    steps = 0
    while True:
        ref = data.copy()
        update(data)
        steps += 1
        if np.all(data == ref):
            break
    return steps

def main():
    data = read_data("data/day25_input.txt")
    n_steps = check_terminal(data)
    print(n_steps)

if __name__ == "__main__":
    main()
