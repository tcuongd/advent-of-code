def read_data():
    with open("day18.txt", "r") as f:
        raw = [tuple([int(c) for c in l.strip().split(",")]) for l in f.readlines()]
    return raw

def get_taxi_distance(c1: tuple[int, int, int], c2: tuple[int, int, int]) -> int:
    return abs(c2[0] - c1[0]) + abs(c2[1] - c1[1]) + abs(c2[2] - c1[2])

def get_n_adjacent(data: list[tuple[int, int, int]]) -> list[int]:
    counts = [0 for _ in range(len(data))]
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            is_adj = get_taxi_distance(data[i], data[j]) == 1
            if is_adj:
                counts[i] += 1
                counts[j] += 1
    return counts

data = read_data()
n_adjs = get_n_adjacent(data)
print(6 * len(data) - sum(n_adjs))
