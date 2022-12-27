from collections import deque
import numpy as np
from string import ascii_lowercase


VALUES = {l: v for l, v in zip(ascii_lowercase, range(len(ascii_lowercase)))}
VALUES["S"] = 0
VALUES["E"] = 25


def read_data() -> tuple[np.ndarray, tuple[int, int], tuple[int, int]]:
    with open("day12.txt", "r") as f:
        raw = np.array([[c for c in l.strip()] for l in f.readlines()])
    start = tuple(np.argwhere(raw == "S")[0])
    end = tuple(np.argwhere(raw == "E")[0])
    heights = np.array([[VALUES[c] for c in row] for row in raw])
    return heights, start, end


def get_adjacent(
    coord: tuple[int, int], values: np.ndarray, max_diff: int = 1
) -> list[tuple[int, int]]:
    i, j = coord
    adjs = []
    for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if (
            i + di >= 0
            and i + di <= values.shape[0] - 1
            and j + dj >= 0
            and j + dj <= values.shape[1] - 1
        ):
            diff = values[i + di, j + dj] - values[i, j]
            if diff <= max_diff:
                adjs.append(((i + di, j + dj), diff))
    adjs_sorted = sorted(adjs, key=lambda x: x[1], reverse=True)
    return [coord for coord, _ in adjs_sorted]


def do_bfs(
    heights: np.ndarray, start: tuple[int, int], end: tuple[int, int]
) -> dict[tuple[int, int], tuple[int, int]]:
    q = deque([start])
    visited = np.zeros_like(heights)
    visited[start] = 1
    links = {}
    while q:
        parent = q.popleft()
        if parent == end:
            return links
        children = get_adjacent(parent, heights)
        for child in children:
            if visited[child] == 0:
                visited[child] = 1
                links[child] = parent
                q.append(child)
    return links


def get_path(
    links: dict[tuple[int, int], tuple[int, int]], start: tuple[int, int], end: tuple[int, int]
) -> list[tuple[int, int]]:
    path = [end]
    while path[-1] != start:
        parent = links[path[-1]]
        path.append(parent)
    return list(reversed(path))


def get_possible_starts(heights: np.ndarray) -> list[tuple[int, int]]:
    return [tuple(coord) for coord in np.argwhere(heights == 0)]


def get_all_path_lengths(heights: np.ndarray, end: tuple[int, int]) -> list[int]:
    starts = get_possible_starts(heights)
    path_lengths = []
    for start in starts:
        links = do_bfs(heights, start, end)
        if end not in links:
            continue
        path = get_path(links, start, end)
        path_lengths.append(len(path) - 1)
    return path_lengths


def print_path(path: list[tuple[int, int]], data: np.ndarray) -> None:
    printer = np.zeros(data.shape)
    for coord in path:
        printer[coord] = 1
    printer = np.where(printer == 1, "#", ".")
    for row in printer:
        print(" ".join(row))


heights, start, end = read_data()
links = do_bfs(heights, start, end)
path = get_path(links, start, end)
print(len(path) - 1)
print(min(get_all_path_lengths(heights, end)))
