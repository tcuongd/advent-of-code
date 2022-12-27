import numpy as np
from collections import Counter, deque, defaultdict
import itertools
from typing import Tuple, List, Dict, Set, final

DICE = [i + 1 for i in range(100)]
DICE_Q = [i + 1 for i in range(3)]

def read_data(input_path: str) -> Tuple[Tuple[int, int]]:
    data = {}
    with open(input_path, "r") as f:
        for i, l in enumerate(f):
            data[i] = int(l.split(":")[1].strip())
    return data

def play_deterministic(starting: Dict[int, int]):
    positions = {k: v for k, v in starting.items()}
    scores = {k: 0 for k in starting}
    num_rolls = 0
    while max([v for v in scores.values()]) < 1000:
        player_idx = num_rolls % 2
        total_moves = 0
        for i in range(3):
            dice_idx = (num_rolls + i) % 100
            total_moves += DICE[dice_idx]
        final_position = (positions[player_idx] + total_moves) % 10
        if final_position == 0:
            final_position = 10
        scores[player_idx] += final_position
        positions[player_idx] = final_position
        num_rolls += 3
    return scores, num_rolls

def play_quantum(starting: Dict[int, int], num_rolls: int, wins: Counter, scores: Dict[int, int]):
    for comb in itertools.product(DICE_Q, DICE_Q, DICE_Q):
        player_idx = num_rolls % 2
        total_moves = sum(comb)
        final_position = (starting[player_idx] + total_moves) % 10
        if final_position == 0:
            final_position = 10
        scores[player_idx] += final_position
        starting[player_idx] = final_position
        num_rolls += 3
        if max([v for v in scores.values()]) >= 21:
            wins.update({player_idx: 1})
        else:
            play_quantum(starting.copy(), num_rolls, wins, scores.copy())

def get_quantum_results(starting: Dict[int, int]):
    num_rolls = 0
    wins = Counter({k: 0 for k in starting})
    scores = {k: 0 for k in starting}
    play_quantum(starting, num_rolls, wins, scores)
    return wins

def main():
    data = read_data("data/day21_input.txt")
    scores, num_rolls = play_deterministic(data)
    print(f"Deterministic, at least 1000: {min(v for v in scores.values()) * num_rolls}")
    qr = get_quantum_results(data)
    print(qr)

if __name__ == "__main__":
    main()
