# If the head is ever two steps directly up, down, left, or right from the tail,
# the tail must also move one step in that direction so it remains close enough:

# Otherwise, if the head and tail aren't touching and aren't in the same row or column,
# the tail always moves one step diagonally to keep up:


def read_data() -> list[tuple[str, int]]:
    with open("day9.txt", "r") as f:
        raw = [l.strip().split(" ") for l in f.readlines()]
    return [(d, int(v)) for d, v in raw]


def is_adjacent(head: list[int], tail: list[int]) -> bool:
    if abs(tail[1] - head[1]) >= 2:
        return False
    elif abs(tail[0] - head[0]) >= 2:
        return False
    return True


def move(data: list[tuple[str, int]]) -> list[tuple[int, int]]:
    """returns a list of coordinates visited by the tail"""
    tail_coords = []
    head = [0, 0]
    tail = [0, 0]
    for direction, number in data:
        if direction == "R":
            for _ in range(number):
                head[1] += 1
                if not is_adjacent(head, tail):
                    tail[1] += 1
                    if tail[0] != head[0]:
                        tail[0] = head[:][0]
                    tail_coords.append(tuple(tail))
        elif direction == "L":
            for _ in range(number):
                head[1] -= 1
                if not is_adjacent(head, tail):
                    tail[1] -= 1
                    if tail[0] != head[0]:
                        tail[0] = head[:][0]
                    tail_coords.append(tuple(tail))
        elif direction == "U":
            for _ in range(number):
                head[0] -= 1
                if not is_adjacent(head, tail):
                    tail[0] -= 1
                    if tail[1] != head[1]:
                        tail[1] = head[:][1]
                    tail_coords.append(tuple(tail))
        elif direction == "D":
            for _ in range(number):
                head[0] += 1
                if not is_adjacent(head, tail):
                    tail[0] += 1
                    if tail[1] != head[1]:
                        tail[1] = head[:][1]
                    tail_coords.append(tuple(tail))
    return tail_coords


def move_position_based(head_coords: list[tuple[int, int]]) -> list[tuple[int, int]]:
    tail_coords = []
    tail = [0, 0]
    for head in head_coords:
        if not is_adjacent(head, tail):
            if head[0] - tail[0] >= 2:
                for _ in range(head[0] - tail[0] - 1):
                    tail[0] += 1
                    if head[1] > tail[1]:
                        tail[1] += 1
                    elif head[1] < tail[1]:
                        tail[1] -= 1
            elif tail[0] - head[0] >= 2:
                for _ in range(tail[0] - head[0] - 1):
                    tail[0] -= 1
                    if head[1] > tail[1]:
                        tail[1] += 1
                    elif head[1] < tail[1]:
                        tail[1] -= 1
            elif head[1] - tail[1] >= 2:
                for _ in range(head[1] - tail[1] - 1):
                    tail[1] += 1
                    if head[0] > tail[0]:
                        tail[0] += 1
                    elif head[0] < tail[0]:
                        tail[0] -= 1
            elif tail[1] - head[1] >= 2:
                for _ in range(tail[1] - head[1] - 1):
                    tail[1] -= 1
                    if head[0] > tail[0]:
                        tail[0] += 1
                    elif head[0] < tail[0]:
                        tail[0] -= 1
            tail_coords.append(tuple(tail))
    return tail_coords


def move_n_knots(data: list[tuple[int, int]], n_knots: int) -> list[tuple[int, int]]:
    for i in range(n_knots - 1):
        if i == 0:
            current_tail = move(data)
        else:
            current_tail = move_position_based(current_tail)
    return current_tail


data = read_data()
coords = move(data)
print(len(set(coords)) + 1)
ten_knots_coords = move_n_knots(data, 10)
print(len(set(ten_knots_coords)) + 1)
