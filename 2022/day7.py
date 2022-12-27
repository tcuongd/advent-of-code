from collections import Counter, defaultdict


def read_data():
    with open("day7.txt", "r") as f:
        raw = [l.strip() for l in f.readlines()]
    return raw


def find_sizes(instructions: list[str]) -> list[int]:
    dirs = defaultdict(list)
    current_tree = []
    for i, ins in enumerate(instructions):
        if ins.startswith("$ cd ..") and len(current_tree) > 0:
            current_tree.pop()
        elif ins.startswith("$ cd") and not ins.startswith("$ cd .."):
            dirname = ins.split(" ")[2]
            current_tree.append(dirname)
        else:
            try:
                size = int(ins.split(" ")[0])
            except Exception:
                continue
            for i, dirname in enumerate(current_tree):
                fullpath = "-".join(current_tree[: (i + 1)])
                dirs[fullpath].append(size)
    return dirs


def get_sum(dirs: dict[str, list[int]], max_total_size: int) -> int:
    total = 0
    for _, sizes in dirs.items():
        if sum(sizes) <= max_total_size:
            total += sum(sizes)
    return total


def get_optimal_delete(dirs: dict[str, list[int]], capacity: int, required_unused: int) -> int:
    current_usued = capacity - sum(dirs["/"])
    required_delete = required_unused - current_usued
    total_sizes = Counter()
    for directory, values in dirs.items():
        total_sizes[directory] = sum(values)
    for directory, total in reversed(total_sizes.most_common()):
        if total > required_delete:
            return total


data = read_data()
dirs = find_sizes(data)
print(get_sum(dirs, 100000))
print(get_optimal_delete(dirs, 70000000, 30000000))
