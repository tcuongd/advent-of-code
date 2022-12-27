import copy
from typing import Union, Optional
import math


def read_data() -> list[tuple[Union[list, int]]]:
    data = []
    current_pair = []
    with open("day13.txt", "r") as f:
        for l in f.readlines():
            l = l.strip()
            if l == "":
                data.append(tuple(current_pair))
                current_pair = []
            else:
                current_pair.append(eval(l))
    return data


def read_data_all() -> list[Union[list, int]]:
    data = []
    with open("day13.txt", "r") as f:
        for l in f.readlines():
            l = l.strip()
            if l == "":
                continue
            else:
                data.append(eval(l))
    data.append([[2]])
    data.append([[6]])
    return data


def evaluate(left: Union[list, int], right: Union[list, int]) -> Optional[bool]:
    if isinstance(left, int) and isinstance(right, int):
        if right < left:
            return False
        elif right > left:
            return True
        else:
            return None
    if isinstance(left, list) and isinstance(right, int):
        right = [right]
    elif isinstance(left, int) and isinstance(right, list):
        left = [left]
    if len(left) == 0 and len(right) == 0:
        return None
    i = 0
    while i < min(len(left), len(right)):
        result = evaluate(left[i], right[i])
        if result in [True, False]:
            return result
        i += 1
    if len(left) < len(right):
        return True
    elif len(right) < len(left):
        return False


def get_trues(pairs: list[tuple[Union[list, int]]]) -> list[int]:
    trues = []
    for i, (left, right) in enumerate(pairs):
        if evaluate(left, right):
            trues.append(i + 1)
    return trues


def sort_packets(data_all: list[Union[list, int]]) -> list[Union[list, int]]:
    ordered = copy.deepcopy(data_all)
    for i in range(1, len(ordered)):
        item = ordered[i]
        j = i - 1
        while j >= 0 and evaluate(item, ordered[j]):
            ordered[j + 1] = ordered[j]
            j -= 1
        ordered[j + 1] = item
    return ordered


def decode(ordered: list[Union[list, int]]) -> int:
    codes = []
    for i, packet in enumerate(ordered):
        if packet in ([[2]], [[6]]):
            codes.append(i + 1)
    print(codes)
    return math.prod(codes)


data = read_data()
print(sum(get_trues(data)))

data_all = read_data_all()
ordered = sort_packets(data_all)
print(decode(ordered))
