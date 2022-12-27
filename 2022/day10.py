import numpy as np


def read_data() -> list[tuple[str, int]]:
    cleaned = []
    with open("day10.txt", "r") as f:
        raw = [l.strip().split(" ") for l in f.readlines()]
    for l in raw:
        if l[0] == "noop":
            cleaned.append((l[0], 0))
        else:
            cleaned.append((l[0], int(l[1])))
    return cleaned


def values_during(data: list[tuple[str, int]], cycles_for_addx: int):
    X = 1
    X_tracker = []
    for instruction, value in data:
        if instruction == "noop":
            X_tracker.append(X)
        elif instruction == "addx":
            for j in range(cycles_for_addx):
                X_tracker.append(X)
                if j == cycles_for_addx - 1:
                    X += value
    return X_tracker


def get_strengths(X_tracker: list[int], indices: list[int]) -> int:
    strength = 0
    for i, v in enumerate(X_tracker):
        if i + 1 in indices:
            strength += (i + 1) * v
    return strength


def draw(X_tracker, grid_size: tuple[int, int]) -> np.ndarray:
    crt = np.zeros(grid_size)
    coords = []
    for i in range(crt.shape[0]):
        for j in range(crt.shape[1]):
            coords.append((i, j))
    for coord, X_position in zip(coords, X_tracker):
        if coord[1] in [X_position - 1, X_position, X_position + 1]:
            crt[coord] = 1
    return crt


def render(crt: np.ndarray) -> None:
    crt_strings = np.where(crt == 1, "#", ".")
    for row in crt_strings:
        print(" ".join(row))


INDICES = [20, 60, 100, 140, 180, 220]
data = read_data()
X_tracker = values_during(data, 2)
print(get_strengths(X_tracker, INDICES))
GRID_SIZE = 6, 40
crt = draw(X_tracker, GRID_SIZE)
render(crt)
