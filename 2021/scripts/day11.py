import numpy as np
import itertools

def read_data(input_path: str) -> np.array:
    with open(input_path, "r") as f:
        data = [[int(c) for c in s.strip()] for s in [l for l in f.readlines()]]
    data = np.array(data, dtype=int)
    return data

def update_state(grid: np.array) -> None:
    """Modifies in place"""
    grid += 1
    did_flash = np.argwhere(grid > 9)
    has_increased_adjacent = []
    while len(has_increased_adjacent) < did_flash.shape[0]:
        for row, col in did_flash:
            if (row, col) not in has_increased_adjacent:
                for xshift, yshift in itertools.product((-1, 0, 1), (-1, 0, 1)):
                    if (xshift, yshift) == (0, 0):
                        continue
                    newx, newy = row + xshift, col + yshift
                    if newx < 0 or newx > grid.shape[0] - 1 or newy < 0 or newy > grid.shape[1] - 1:
                        continue
                    grid[newx, newy] += 1
                has_increased_adjacent.append((row, col))
        did_flash = np.argwhere(grid > 9)
    grid[grid > 9] = 0

def count_flashes(grid: np.array, n_states: int) -> int:
    count = 0
    for _ in range(n_states):
        update_state(grid)
        count += np.sum(grid == 0)
    return count

def get_first_all_flash(grid: np.array) -> int:
    has_all_flashed = False
    i = 0
    while not has_all_flashed:
        update_state(grid)
        has_all_flashed = np.sum(grid == 0) == np.product(grid.shape)
        i += 1
    return i

def main():
    data = read_data("data/day11_input.txt")
    flashes = count_flashes(data, 100)
    print(f"flashes after 100 steps={flashes}")
    data = read_data("data/day11_input.txt")
    first_all_flash = get_first_all_flash(data)
    print(f"first step all flash={first_all_flash}")

if __name__ == "__main__":
    main()
