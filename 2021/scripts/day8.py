import itertools
from typing import List, Tuple, Dict

MAPPING = {
    0: {'a', 'b', 'c', 'e', 'f', 'g'},
    1: {'c', 'f'},
    2: {'a', 'c', 'd', 'e', 'g'},
    3: {'a', 'c', 'd', 'f', 'g'},
    4: {'b', 'c', 'd', 'f'},
    5: {'a', 'b', 'd', 'f', 'g'},
    6: {'a', 'b', 'd', 'e', 'f', 'g'},
    7: {'a', 'c', 'f'},
    8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
    9: {'a', 'b', 'c', 'd', 'f', 'g'},
}

LENGTHS = {num: len(m) for num, m in MAPPING.items()}

UNIQUES = [LENGTHS[num] for num in (1, 4, 7, 8)]

def read_data(input_path: str) -> List[Tuple[List[str], List[str]]]:
    with open(input_path, "r") as f:
        data = [(i.split(" "), o.split(" ")) for i, o in [l.strip().split(" | ") for l in f.readlines()]]

    return data

def count_outputs_len_unique(data: List[Tuple[List[str], List[str]]]) -> int:
    counts = 0
    for _, outdata in data:
        lengths = [len(s) for s in outdata]
        n_uniques = sum([l in UNIQUES for l in lengths])
        counts += n_uniques
    return counts

def find_mapping(in_data: List[str]) -> Dict[str, str]:
    all_chars = 'abcdefg'
    char_perms = itertools.permutations(all_chars, r=len(all_chars))
    all_mappings = [{c: corrected for c, corrected in zip(all_chars, perm)} for perm in char_perms]
    for correct_mapping in all_mappings:
        checks = []
        for s in in_data:
            mapped = {correct_mapping[char] for char in s}
            found_map = any([mapped == m for m in MAPPING.values()])
            checks.append(found_map)
        if all(checks):
            break
    return correct_mapping

def parse_output(out_data: List[str], correction: Dict[str, str]):
    num_string = ''
    for s in out_data:
        mapped = {correction[char] for char in s}
        number = [mapped == m for m in MAPPING.values()].index(True)
        num_string += str(number)
    return int(num_string)

def sum_outputs(data: List[Tuple[List[str], List[str]]]) -> int:
    total = 0
    for row in data:
        mapping = find_mapping(row[0])
        total += parse_output(row[1], mapping)
    return total

def main():
    data = read_data("data/day8_input.txt")
    print(count_outputs_len_unique(data))
    total_output = sum_outputs(data)
    print(total_output)

if __name__ == "__main__":
    main()
