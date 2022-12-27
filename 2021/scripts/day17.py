import numpy as np
from collections import Counter, deque, defaultdict
import itertools
from typing import Tuple, List, Dict, Set

def read_data(input_path: str) -> Tuple[Tuple[int, int]]:
    with open(input_path, "r") as f:
        line = f.read().strip()
    line = line.replace("target area: ", "")
    data = [c.replace("x=","").replace("y=","").split("..") for c in (d.strip() for d in line.split(","))]
    xd = [int(c) for c in data[0]]
    yd = [int(c) for c in data[1]]
    return xd, yd

def get_target(xd, yd) -> np.array:
    xs = np.arange(xd[0], xd[1] + 1, 1)
    ys = np.arange(yd[0], yd[1] + 1, 1)
    coords = []
    for x, y in itertools.product(xs, ys):
        coords.append((x, y))
    return coords

def check_trajectory(start: Tuple[int, int], initv: Tuple[int, int], xd: Tuple[int, int], yd: Tuple[int, int]) -> Tuple[bool, int]:
    current_position = list(start)
    v = list(initv)
    i = 0
    all_ys = [start[1]]
    target_area = get_target(xd, yd)
    is_valid = False
    while True:
        next_x = current_position[0] + v[0]
        next_y = current_position[1] + v[1]
        if (next_x, next_y) in target_area:
            is_valid = True
        if start[0] < xd[0]:
            if next_x > xd[1]:
                break
        if start[0] > xd[1]:
            if next_x < xd[0]:
                break
        if start[1] > yd[1]:
            if next_y < yd[0]:
                break
        if start[1] < yd[0]:
            if next_y > yd[1]:
                break
        i += 1
        current_position[0] = next_x
        current_position[1] = next_y
        all_ys.append(next_y)
        if v[0] < 0:
            v[0] += 1
        elif v[0] > 0:
            v[0] -= 1
        v[1] -= 1

    return is_valid, np.max(all_ys)

def find_highest_init_y(start, xd, yd):
    best = (0, 0)
    highest_y = start[1]
    # assume x positive
    for i in range(xd[1] + 1):
        # assume y negative
        for j in range(-yd[1] * 2):
            init = (i, j)
            is_valid, max_height = check_trajectory(start, init, xd, yd)
            if is_valid and max_height > highest_y:
                highest_y = max_height
                best = init
    return best, highest_y

def find_all_inits(start, xd, yd):
    all_inits = set()
    # assume x positive
    for i in range(xd[1] + 1):
        # assume y negative
        for j in range(yd[0], -yd[1] * 2):
            init = (i, j)
            is_valid, _ = check_trajectory(start, init, xd, yd)
            if is_valid:
                all_inits.add(init)
    return all_inits

def main():
    xd, yd = read_data("data/day17_input.txt")
    start = (0, 0)
    highest_y = find_highest_init_y(start, xd, yd)
    print(highest_y)
    all_inits = find_all_inits(start, xd, yd)
    print(len(all_inits))

if __name__ == "__main__":
    main()
