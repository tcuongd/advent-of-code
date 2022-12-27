import numpy as np
from typing import List, Tuple

def read_data(input_path: str):
    coords = []
    folds = []
    with open(input_path, "r") as f:
        for line in f:
            if line.startswith("fold"):
                instruction = line.strip().replace("fold along ", "").split("=")
                folds.append((instruction[0], int(instruction[1])))
            elif line.strip():
                coords.append([int(s) for s in line.strip().split(",")])
            else:
                continue
    return coords, folds

def get_grid_shape(coords: List[List[int]]) -> Tuple[int, int]:
    return max(c[1] for c in coords) + 1, max(c[0] for c in coords) + 1

def set_dots(coords: List[List[int]]) -> np.array:
    grid_shape = get_grid_shape(coords)
    grid = np.zeros(grid_shape, dtype=int)
    for col_offset, row_offset in coords:
        grid[row_offset, col_offset] = 1
    return grid

def fold_along(grid: np.array, fold_instruction: Tuple[str, int]) -> np.array:
    """
    y = bring the bottom part _up_
    x = bring the right part to the _left_
    """
    if fold_instruction[0] == 'y':
        top, bottom = grid[:fold_instruction[1], :], grid[(fold_instruction[1] + 1):, :]
        if top.shape[0] >= bottom.shape[0]:
            folded = np.zeros(top.shape, dtype=int)
            folded += top
            folded[-bottom.shape[0]:, :] += np.flipud(bottom)
        else:
            folded = np.zeros(bottom.shape, dtype=int)
            folded += np.flipud(bottom)
            folded[-top.shape[0]:, :] += top
    if fold_instruction[0] == 'x':
        left, right = grid[:, :fold_instruction[1]], grid[:, (fold_instruction[1] + 1):]
        if left.shape[1] >= right.shape[1]:
            folded = np.zeros(left.shape, dtype=int)
            folded += left
            folded[:, -right.shape[1]:] += np.fliplr(right)
        else:
            folded = np.zeros(right.shape, dtype=int)
            folded += np.fliplr(right)
            folded[:, -left.shape[1]:] += left
    folded[folded > 1] = 1
    return folded

def print_output(grid: np.array) -> str:
    outstr = ''
    for line in grid:
        outstr += ''.join(line.astype(str))
        outstr += '\n'
    outstr = outstr.replace('1', '#').replace('0', '.')
    return outstr

def main():
    coords, folds = read_data("data/day13_input.txt")
    print(folds)
    grid = set_dots(coords)
    print(grid.shape)
    folded = fold_along(grid, folds[0])
    print(np.sum(folded))
    # Part 2
    letter = np.copy(grid)
    for fold_instruction in folds:
        letter = fold_along(letter, fold_instruction)
    with open("scripts/day13_output.txt", "w") as out:
        out.write(print_output(letter))

if __name__ == "__main__":
    main()
