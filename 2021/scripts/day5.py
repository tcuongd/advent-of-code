import numpy as np
from typing import Tuple, List

def read_data(input_path: str) -> List[List[Tuple[int, int]]]:
    data = []
    with open(input_path, "r") as f:
        for line in f:
            coords = line.strip().split(" -> ")
            parsed = []
            for coord in coords:
                x, y = np.array(coord.split(",")).astype(int)
                parsed.append((x, y))
            data.append(parsed)
    return data

def create_grid(data: list) -> np.array:
    y_max = max([max([coord[1] for coord in pair]) for pair in data])
    x_max = max([max([coord[0] for coord in pair]) for pair in data])
    return np.zeros((x_max + 1, y_max + 1), dtype=int)

def analyse_lines(data: list, straights_only: bool) -> int:
    grid = create_grid(data)
    for (x1, y1), (x2, y2) in data:
        v_start, v_end = sorted((x1, x2))
        h_start, h_end = sorted((y1, y2))
        # Horizontal
        if x1 == x2:
            grid[x1, h_start:(h_end+1)] += 1
        # Vertical
        elif y1 == y2:
            grid[v_start:(v_end+1), y1] += 1
        elif not straights_only:
            steps = v_end - v_start
            for i in range(steps + 1):
                if x1 < x2 and y1 < y2:
                    grid[x1 + i, y1 + i] += 1
                elif x1 < x2 and y1 > y2:
                    grid[x1 + i, y1 - i] += 1
                elif x1 > x2 and y1 < y2:
                    grid[x2 + i, y2 - i] += 1
                elif x1 > x2 and y1 > y2:
                    grid[x2 + i, y2 + i] += 1
    return np.sum(grid >= 2)

def main() -> None:
    data = read_data("data/day5_input.txt")
    total_straights_only = analyse_lines(data, straights_only=True)
    print(f"Straight lines only: {total_straights_only}")
    total = analyse_lines(data, straights_only=False)
    print(f"Total: {total}")

if __name__ == "__main__":
    main()
