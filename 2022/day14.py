import numpy as np


def read_data() -> list[tuple[tuple[int, int]]]:
    lines = []
    with open("day14.txt", "r") as f:
        for l in f.readlines():
            l = l.strip()
            arrows = [c for c in l.split(" -> ")]
            points = [tuple([int(num) for num in a.split(",")]) for a in arrows]
            for i in range(len(points) - 1):
                lines.append((points[i], points[i + 1]))
    return lines


def draw_grid(lines: list[tuple[tuple[int, int]]], start: tuple[int, int]) -> np.ndarray:
    max_across = start[0]
    max_down = start[1]
    for pair in lines:
        for coord in pair:
            across = coord[0]
            down = coord[1]
            if across > max_across:
                max_across = across
            if down > max_down:
                max_down = down
    grid = np.zeros((max_down + 1, max_across + 1))
    for (x_from, y_from), (x_to, y_to) in lines:
        if x_from == x_to:
            if y_from < y_to:
                grid[y_from : (y_to + 1), x_from] = -1
            else:
                grid[y_to : (y_from + 1), x_from] = -1
        elif y_from == y_to:
            if x_from < x_to:
                grid[y_from, x_from : (x_to + 1)] = -1
            else:
                grid[y_from, x_to : (x_from + 1)] = -1

    return grid


def drop_sand(grid: np.ndarray, start: tuple[int, int]) -> np.ndarray:
    grid = grid.copy()
    while True:
        final_x, final_y = start
        move_is_possible = True
        while move_is_possible:
            if final_y + 1 > grid.shape[0] - 1:
                break
            elif grid[final_y + 1, final_x] == 0:
                final_y += 1
            elif grid[final_y + 1, final_x - 1] == 0:
                final_y += 1
                final_x -= 1
            elif final_x + 1 < grid.shape[1] - 1:
                if grid[final_y + 1, final_x + 1] == 0:
                    final_y += 1
                    final_x += 1
                else:
                    move_is_possible = False
            else:
                move_is_possible = False
        if final_y == grid.shape[0] - 1:
            break
        elif grid[final_y, final_x] == 0:
            grid[final_y, final_x] = 1
    return grid


def extend_floor(grid: np.ndarray) -> np.ndarray:
    extension = np.vstack([np.zeros((1, grid.shape[1])), np.full((1, grid.shape[1]), -1)])
    return np.vstack([grid, extension])


def extend_sides(grid: np.ndarray, direction: str) -> np.ndarray:
    extension = np.vstack([np.zeros((grid.shape[0] - 1, 1)), np.full((1, 1), -1)])
    if direction == "left":
        return np.hstack([extension, grid])
    elif direction == "right":
        return np.hstack([grid, extension])


def drop_sand_infinite(grid: np.ndarray, start: tuple[int, int]) -> np.ndarray:
    grid = grid.copy()
    left_extensions = 0
    while True:
        final_y = start[1]
        final_x = start[0] + left_extensions
        move_is_possible = True
        while move_is_possible:
            if final_y + 1 > grid.shape[0] - 1:
                break
            elif grid[final_y + 1, final_x] == 0:
                final_y += 1
            else:
                if final_x - 1 < 0:
                    grid = extend_sides(grid, "left")
                    left_extensions += 1
                    final_x += 1
                elif final_x + 1 > grid.shape[1] - 1:
                    grid = extend_sides(grid, "right")

                if grid[final_y + 1, final_x - 1] == 0:
                    final_y += 1
                    final_x -= 1
                elif grid[final_y + 1, final_x + 1] == 0:
                    final_y += 1
                    final_x += 1
                else:
                    move_is_possible = False
        if grid[final_y, final_x] == 0:
            grid[final_y, final_x] = 1
        if (final_x - left_extensions, final_y) == start:
            break
    return grid


def print_grid(data: np.ndarray, fname: str) -> None:
    printer = np.full(data.shape, ".", dtype=str)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i, j] == -1:
                printer[i, j] = "#"
            if data[i, j] == 0:
                printer[i, j] = "."
            if data[i, j] == 1:
                printer[i, j] = "o"
    starting_across = min([coord[1] for coord in np.argwhere(data == -1)])
    with open(fname, "w") as f:
        for row in printer:
            f.write(" ".join(row[starting_across:]))
            f.write("\n")


START = 500, 0
lines = read_data()
grid = draw_grid(lines, START)
final_grid = drop_sand(grid, START)
print(np.sum(final_grid == 1))
print_grid(final_grid, "day14_grid_1.txt")

extended = extend_floor(grid)
infinite_grid = drop_sand_infinite(extended, START)
print(np.sum(infinite_grid == 1))
print_grid(infinite_grid, "day14_grid_2.txt")
