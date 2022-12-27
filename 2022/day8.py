import numpy as np


def read_data() -> np.ndarray:
    with open("day8.txt", "r") as f:
        raw = [[int(i) for i in l.strip()] for l in f.readlines()]
    return np.array(raw)


def get_edges(data: np.ndarray) -> list[list[float, float]]:
    edges = set()
    for i in range(data.shape[1]):
        for j in range(data.shape[0]):
            if i == 0 or i == data.shape[1] - 1 or j == 0 or j == data.shape[0] - 1:
                edges.add((i, j))
    return edges


def count_visible(data: np.ndarray) -> int:
    edges = get_edges(data)
    n_visible = len(edges)
    for i in range(data.shape[1]):
        for j in range(data.shape[0]):
            if (i, j) in edges:
                continue
            else:
                tallest_left = max(data[i, :j])
                tallest_right = max(data[i, (j + 1) :])
                tallest_up = max(data[:i, j])
                tallest_down = max(data[(i + 1) :, j])
                if min([tallest_left, tallest_right, tallest_up, tallest_down]) < data[i, j]:
                    n_visible += 1
    return n_visible


def count_trees_seen(data: np.ndarray, i, j) -> int:
    left_seen = 0
    for m in range(1, i + 1):
        left_seen +=1
        if data[i - m, j] >= data[i, j]:
            break

    right_seen = 0
    for m in range(1, data.shape[1] - i):
        right_seen += 1
        if data[i + m, j] >= data[i, j]:
            break

    up_seen = 0
    for m in range(1, j + 1):
        up_seen += 1
        if data[i, j - m] >= data[i, j]:
            break

    down_seen = 0
    for m in range(1, data.shape[0] - j):
        down_seen += 1
        if data[i, j + m] >= data[i, j]:
            break
    return left_seen * right_seen * up_seen * down_seen


def get_best_view(data: np.ndarray) -> int:
    edges = get_edges(data)
    best_score = 0
    for i in range(data.shape[1]):
        for j in range(data.shape[0]):
            if (i, j) in edges:
                continue
            else:
                view_score = count_trees_seen(data, i, j)
                if view_score > best_score:
                    best_score = view_score
    return best_score


data = read_data()
print(count_visible(data))
print(get_best_view(data))
