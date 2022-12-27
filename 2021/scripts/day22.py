import numpy as np
from collections import Counter, deque, defaultdict
import itertools
from typing import Tuple, List, Dict, Set, final

def read_data(input_path: str) -> Tuple[Tuple[int, int]]:
    data = []
    with open(input_path, "r") as f:
        lines = f.readlines()
    for i, l in enumerate(lines):
        instruction = l.strip().split(" ")[0]
        x, y, z = l.strip().split(" ")[1].split(",")
        x = [int(n) for n in x.replace("x=", "").split("..")]
        y = [int(n) for n in y.replace("y=", "").split("..")]
        z = [int(n) for n in z.replace("z=", "").split("..")]
        data.append((1 if instruction == 'on' else 0, x, y, z))
    return data

def convert_coords(coord: List[int], min_x: int, min_y: int, min_z: int):
    new_coord = coord.copy()
    if min_x < 0:
        new_coord[0] -= min_x
    if min_y < 0:
        new_coord[1] -= min_y
    if min_z < 0:
        new_coord[2] -= min_z
    return new_coord

def get_grid(xb, yb, zb) -> np.ndarray:
    shape = (
        (xb[1] - xb[0] + 1),
        (yb[1] - yb[0] + 1),
        (zb[1] - zb[0] + 1),
    )
    return np.zeros(shape, dtype=bool)

def turn_on(grid: np.ndarray, data: List[tuple]) -> None:
    """Modifies grid in-place"""
    for i, ins in enumerate(data):
        if i >= 20:
            break
        min_x, min_y, min_z = convert_coords([ins[1][0], ins[2][0], ins[3][0]], -50, -50, -50)
        max_x, max_y, max_z = convert_coords([ins[1][1], ins[2][1], ins[3][1]], -50, -50, -50)
        grid[min_x:(max_x+1), min_y:(max_y+1), min_z:(max_z+1)] = ins[0]

def get_max_shape(data: List[tuple]) -> Tuple[int, int, int]:
    min_x = min([l[1][0] for l in data])
    min_y = min([l[2][0] for l in data])
    min_z = min([l[3][0] for l in data])
    max_x = max([l[1][1] for l in data])
    max_y = max([l[2][1] for l in data])
    max_z = max([l[3][1] for l in data])
    return (min_x, max_x), (min_y, max_y), (min_z, max_z)

def main():
    data = read_data("data/day22_input.txt")
    # Part 1
    xb = [-50, 50]
    yb = [-50, 50]
    zb = [-50, 50]
    grid_init = get_grid(xb, yb, zb)
    turn_on(grid_init, data[:20])
    print(int(np.sum(grid_init)))

if __name__ == "__main__":
    main()
