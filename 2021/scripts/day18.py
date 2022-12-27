import numpy as np
from collections import Counter, deque, defaultdict
import itertools
from typing import Tuple, List, Dict, Set

def read_data(input_path: str) -> Tuple[Tuple[int, int]]:
    data = []
    with open(input_path, "r") as f:
        for line in f:
            data.append(eval(line.strip()))
    return data

def parse_line(line: list, current_depth: int = None, has_mutated: bool = False):
    if current_depth is None:
        current_depth = 0
    i = 0
    for i, elem in enumerate(line):
        if has_mutated:
            break
        if isinstance(elem, list):
            current_depth += 1
            if current_depth >= 4 and all(isinstance(el, int) for el in elem):
                if i > 0:
                    line[i - 1] += elem[0]
                if i < len(line) - 1:
                    line[i + 1] += elem[1]
                line[i] = 0
                has_mutated = True
                return line
            else:
                line[i] = parse_line(elem, current_depth, has_mutated)
        elif isinstance(line[i], int) and elem >= 10:
            line[i] = [int(np.floor(elem / 2)), int(np.ceil(elem / 2))]
            has_mutated = True
            return line
        i += 1
    return line


def main():
    data = read_data("data/day18_input.txt")
    parse_line(data[0])
    print(data[0])

if __name__ == "__main__":
    main()
