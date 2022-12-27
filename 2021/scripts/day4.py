import numpy as np
from typing import Tuple, List

def read_data(input_path: str) -> Tuple[List[int], List[np.array]]:
    with open(input_path, "r") as f:
        matrices = []
        for i, line in enumerate(f):
            if i == 0:
                numbers = line.strip().split(",")
                numbers = np.array(numbers).astype(int)
            else:
                board_row = line.strip().split(" ")
                board_row = [b for b in board_row if b != '']
                if len(board_row) > 1:
                    board_row = np.array(board_row).astype(int)
                    matrices[-1].append(board_row)
                else:
                    matrices.append([])
        matrices = [np.vstack(m) for m in matrices]
    return numbers, matrices

def find_winning_score(numbers: List[int], matrices: List[np.array]) -> int:
    matrices = [m for m in matrices]
    flags = [np.ones_like(m) for m in matrices]
    score = 0
    for number in numbers:
        for base, flag in zip(matrices, flags):
            idx = base == number
            flag[idx] = 0
            if np.any(flag.sum(axis=0) == 0) or np.any(flag.sum(axis=1) == 0):
                total = np.sum(base * flag)
                score = number * total
                break
        if score > 0:
            break
    return score

def find_all_scores(numbers: List[int], matrices: List[np.array]) -> Tuple[List[int], List[int]]:
    matrices = [m for m in matrices]
    flags = [np.ones_like(m) for m in matrices]
    time_to_win = []
    board_scores = []
    for base, flag in zip(matrices, flags):
        for t, number in enumerate(numbers):
            idx = base == number
            flag[idx] = 0
            if np.any(flag.sum(axis=0) == 0) or np.any(flag.sum(axis=1) == 0):
                total = np.sum(base * flag)
                score = number * total
                board_scores.append(score)
                time_to_win.append(t)
                break
    return time_to_win, board_scores

def main() -> None:
    numbers, matrices = read_data("data/day4_input.txt")
    winning_score = find_winning_score(numbers, matrices)
    print(f"winning_score={winning_score}")
    time_to_win, all_scores = find_all_scores(numbers, matrices)
    last_score = all_scores[np.argmax(time_to_win)]
    print(f"last_score={last_score}")

if __name__ == "__main__":
    main()
