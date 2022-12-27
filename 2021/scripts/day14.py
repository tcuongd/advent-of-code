from collections import Counter
from typing import List, Dict, Tuple

def read_data(input_path) -> Tuple[str, Dict[str, str]]:
    insertion_rules = {}
    with open(input_path, "r") as f:
        for l in f:
            line = l.strip()
            if line == '':
                continue
            elif line[3] != "-":
                template = line
            elif "->" in line:
                nodes = line.split(" -> ")
                insertion_rules[nodes[0]] = nodes[1]
    return template, insertion_rules

def insert_polymer(pair: str, insertion_rules: Dict[str, str]) -> str:
    val = insertion_rules[pair]
    return f"{pair[0]}{val}{pair[1]}"

def get_new_str(current_str: str, insertion_rules: Dict[str, str]) -> str:
    new_str = ''
    for i, s in enumerate(current_str):
        if i + 2 > len(current_str):
            break
        pair = current_str[i:i+2]
        new_str += insert_polymer(pair, insertion_rules)
        if i + 2 < len(current_str):
            new_str = new_str[:-1]
    return new_str

def get_pairs(current_str: str) -> Counter:
    pairs = []
    for i, _ in enumerate(current_str):
        if i + 2 > len(current_str):
            break
        pairs.append(current_str[i:i+2])
    pairs_count = Counter(pairs)
    return pairs_count

def get_pairs_after(pairs_count: Counter, insertion_rules: Dict[str, str]) -> Counter:
    new_counts = Counter()
    for pair, cnt in pairs_count.items():
        newstr = insert_polymer(pair, insertion_rules)
        new_counts.update({newstr[:2]: cnt, newstr[1:]: cnt})
    return new_counts

def main():
    template, insertion_rules = read_data("data/day14_input.txt")
    new_str = template
    for _ in range(10):
        new_str = get_new_str(new_str, insertion_rules)
    counter = Counter(new_str)
    print(counter.most_common()[0][1] - counter.most_common()[-1][1])

    new_str2 = template
    pairs = get_pairs(new_str2)
    for _ in range(40):
        pairs = get_pairs_after(pairs, insertion_rules)
    final = Counter({new_str2[-1]: 1})
    for pair, cnt in pairs.items():
        final.update({pair[0]: cnt})
    print(final.most_common()[0][1] - final.most_common()[-1][1])

if __name__ == "__main__":
    main()
