import string

lowers = {c: points for c, points in zip(string.ascii_lowercase, range(1, 27))}
uppers = {c: points for c, points in zip(string.ascii_uppercase, range(27, 53))}
SCORES = {**lowers, **uppers}


def read_data() -> list[list[set]]:
    data = []
    with open("day3.txt", "r") as f:
        for l in f.readlines():
            items = l.strip()
            size = len(items)
            data.append([set(items[: int(size / 2)]), set(items[-int(size / 2) :])])
    return data


def read_data_groups() -> list[list[set]]:
    data = []
    with open("day3.txt", "r") as f:
        current_group = []
        for l in f.readlines():
            items = l.strip()
            current_group.append(set(items))
            if len(current_group) == 3:
                data.append(current_group)
                current_group = []
    return data


def get_common(data: list[list[set]]) -> list[str]:
    return [c1.intersection(c2).pop() for c1, c2 in data]


def get_group_common(data_groups: list[list[set]]) -> list[str]:
    return [c1.intersection(c2).intersection(c3).pop() for c1, c2, c3 in data_groups]


data = read_data()
commons = get_common(data)
print(sum(SCORES[c] for c in commons))
data_groups = read_data_groups()
commons_groups = get_group_common(data_groups)
print(sum(SCORES[c] for c in commons_groups))
