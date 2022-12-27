import numpy as np
from typing import List, Tuple, Set

def read_data(input_path: str) -> np.array:
    with open(input_path, "r") as f:
        data = [[int(c) for c in s.strip()] for s in [l for l in f.readlines()]]
    data = np.array(data, dtype=int)
    return data

def get_adjacent_indices(idx: Tuple[int, int], shape: Tuple[int, int]) -> List[Tuple[int, int]]:
    adjacent_indices = []
    for xshift, yshift in ((-1, 0), (0, 1), (1, 0), (0, -1)):
        newx, newy = idx[0] + xshift, idx[1] + yshift
        if newx < 0 or newx > shape[0] - 1 or newy < 0 or newy > shape[1] - 1:
            continue
        adjacent_indices.append((newx, newy))
    return adjacent_indices

def find_low_points(data: np.array) -> List[Tuple[int, int]]:
    low_points = []
    for x in range(data.shape[0]):
        for y in range(data.shape[1]):
            adjacent_indices = get_adjacent_indices((x, y), data.shape)
            comparison_vector = [data[idx] for idx in adjacent_indices]
            if all(data[x, y] < c for c in comparison_vector):
                low_points.append((x, y))
    return low_points

def calculate_risk(data: np.array) -> int:
    low_points = find_low_points(data)
    risk = 0
    for idx in low_points:
        risk += data[idx] + 1
    return risk

def find_basins(data: np.array, low_points: List[Tuple[int, int]]) -> List[Set[Tuple[int, int]]]:
    """Each basin has one low point. Search for all the adjacent indices of the low point, and all
    of the adjacents of those indices. Once search has been exhausted excluding 9s, move on to the next basin.
    """
    searched = np.zeros_like(data)
    searched[searched == 9] = 1
    basins = [{(x, y),} for x, y in low_points]
    for basin in basins:
        while any([searched[idx] == 0 for idx in basin]):
            to_search = [idx for idx in basin if searched[idx] == 0]
            for idx in to_search:
                adjacent_indices = get_adjacent_indices(idx, data.shape)
                for adj in adjacent_indices:
                    if data[adj] != 9:
                        basin.add(adj)
                searched[idx] = 1
    return basins

def product_largest_basins(basins: List[Set[Tuple[int, int]]], n_largest: int) -> int:
    sizes = [len(basin) for basin in basins]
    return np.product(sorted(sizes, reverse=True)[:n_largest])

def main():
    data = read_data("data/day9_input.txt")
    print(f"Risk={calculate_risk(data)}")
    low_points = find_low_points(data)
    basins = find_basins(data, low_points)
    print(f"Largest basin sizes product={product_largest_basins(basins, 3)}")

if __name__ == "__main__":
    main()
