from typing import List, Tuple
import numpy as np

def read_data(input_path) -> np.array:
    with open(input_path, "r") as f:
        lines = [[int(x) for x in l.strip()] for l in f]
    grid = np.array(lines).astype(int)
    return grid

def get_adjacent_indices(idx: Tuple[int, int], shape: Tuple[int, int]) -> List[Tuple[int, int]]:
    adjacent_indices = []
    for xshift, yshift in ((0, -1), (-1, 0), (0, 1), (1, 0)):
        newx, newy = idx[0] + xshift, idx[1] + yshift
        if newx < 0 or newx > shape[0] - 1 or newy < 0 or newy > shape[1] - 1:
            continue
        adjacent_indices.append((newx, newy))
    return adjacent_indices

def find_lowest_path(grid: np.array, start: Tuple[int, int], end: Tuple[int, int]) -> int:
    risks = {start: 0}
    to_analyse = set([start])
    was_analysed = set()
    while to_analyse.difference(was_analysed):
        for coord in to_analyse.difference(was_analysed):
            adjs = get_adjacent_indices(coord, grid.shape)
            for adj in adjs:
                total_risk = risks[coord] + grid[adj]
                if adj not in risks:
                    risks[adj] = total_risk
                elif total_risk < risks[adj]:
                    risks[adj] = total_risk
                    # If the lowest cost of a point has been updated, we need to re-analyse that point.
                    was_analysed.discard(adj)
                if adj != end:
                    to_analyse.add(adj)
            was_analysed.add(coord)
    return risks[end]

def extend_grid(grid: np.array) -> np.array:
    horizontals = [grid]
    for _ in range(1, 5):
        newgrid = horizontals[-1] + 1
        newgrid[newgrid > 9] = 1
        horizontals.append(newgrid)
    h_large = np.vstack(horizontals)
    verticals = [h_large]
    for _ in range(1, 5):
        newgrid = verticals[-1] + 1
        newgrid[newgrid > 9] = 1
        verticals.append(newgrid)
    large = np.hstack(verticals)
    return large

def main():
    grid = read_data("data/day15_input.txt")
    end = (grid.shape[0] - 1, grid.shape[1] - 1)
    print(find_lowest_path(grid, (0, 0), end))
    big_grid = extend_grid(grid)
    big_end = (big_grid.shape[0] - 1, big_grid.shape[1] - 1)
    print(find_lowest_path(big_grid, (0, 0), big_end))

if __name__ == "__main__":
    main()
