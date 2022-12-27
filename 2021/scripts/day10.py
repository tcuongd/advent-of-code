import numpy as np
from typing import List
from dataclasses import dataclass

BRACKETS = [
    {'start': '(', 'end': ')', 'pts_corrupt': 3, 'pts_completion': 1},
    {'start': '[', 'end': ']', 'pts_corrupt': 57, 'pts_completion': 2},
    {'start': '{', 'end': '}', 'pts_corrupt': 1197, 'pts_completion': 3},
    {'start': '<', 'end': '>', 'pts_corrupt': 25137, 'pts_completion': 4},
]

@dataclass
class LineSummary:
    is_corrupt: bool
    first_illegal: int
    remaining_open: List[int]

def get_id(bracket: str) -> int:
    for i, b in enumerate(BRACKETS):
        if bracket == b['start'] or bracket == b['end']:
            return i

def summarise_line(line: str) -> LineSummary:
    starts = []
    for bracket in line:
        idx = get_id(bracket)
        if bracket == BRACKETS[idx]['start']:
            starts.append(idx)
        elif bracket == BRACKETS[idx]['end']:
            if not starts or starts[-1] != idx:
                return LineSummary(is_corrupt=True, first_illegal=idx, remaining_open=starts)
            else:
                del starts[-1]
    return LineSummary(is_corrupt=False, first_illegal=-1, remaining_open=starts)

def calculate_corrupt_score(data):
    score = 0
    for line in data:
        ls = summarise_line(line)
        if ls.is_corrupt:
            score += BRACKETS[ls.first_illegal]['pts_corrupt']
    return score

def calculate_completion_score(data):
    scores = []
    for line in data:
        ls = summarise_line(line)
        if ls.is_corrupt:
            continue
        completions = ls.remaining_open[::-1]
        completion_score = 0
        for b_id in completions:
            completion_score *= 5
            completion_score += BRACKETS[b_id]['pts_completion']
        scores.append(completion_score)
    return int(np.median(np.array(scores)))

def main():
    with open("data/day10_input.txt", "r") as f:
        data = [s.strip() for s in f.readlines()]
    corrupt_score = calculate_corrupt_score(data)
    print(f"corrupt_score={corrupt_score}")
    completion_score = calculate_completion_score(data)
    print(f"completion_score={completion_score}")

if __name__ == "__main__":
    main()
