def read_data() -> list[list[tuple[int, int]]]:
    with open("day4.txt", "r") as f:
        raw = [l.strip().split(",") for l in f.readlines()]
    bounds = [[[int(c) for c in a.split("-")] for a in pair] for pair in raw]
    return bounds

def fully_overlaps(b1: tuple[int, int], b2: tuple[int, int]) -> bool:
    if b1[0] >= b2[0] and b1[1] <= b2[1]:
        return True
    if b2[0] >= b1[0] and b2[1] <= b1[1]:
        return True
    return False

def partial_overlaps(b1: tuple[int, int], b2: tuple[int, int]) -> bool:
    if b1[1] >= b2[0] and b1[0] <= b2[0]:
        return True
    if b2[1] >= b1[0] and b2[0] <= b1[0]:
        return True
    return False

def any_overlaps(b1: tuple[int, int], b2: tuple[int, int]) -> bool:
    if fully_overlaps(b1, b2) or partial_overlaps(b1, b2):
        return True
    else:
        return False

def count_overlaps(bounds: list[list[tuple[int, int]]]) -> int:
    return sum([fully_overlaps(b1, b2) for b1, b2 in bounds])

def count_any_overlaps(bounds: list[list[tuple[int, int]]]) -> int:
    return sum([any_overlaps(b1, b2) for b1, b2 in bounds])

data = read_data()
n_overlaps = count_overlaps(data)
print(n_overlaps)
n_any_overlaps = count_any_overlaps(data)
print(n_any_overlaps)
