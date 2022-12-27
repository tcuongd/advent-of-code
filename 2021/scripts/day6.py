import copy
import numpy as np
from typing import Dict, List

def read_data(input_path: str) -> List[int]:
    with open(input_path, "r") as f:
        data = f.read().strip().split(",")
        data = np.array(data).astype(int)
    return data

def get_groups(data: List[int]) -> Dict[int, int]:
    return {start: np.sum(data == start) for start in np.unique(data)}

def simulate(initial_timer: int, n_days: int) -> List[int]:
    starts = [initial_timer]
    for _ in range(n_days):
        n_new = sum([s == 0 for s in starts])
        new_fish = [8 for _ in range(n_new)]
        for i, t in enumerate(starts):
            if t == 0:
                starts[i] = 6
            else:
                starts[i] -= 1
        starts += new_fish
    return starts

def count_simple(groups: Dict[int, int], n_days: int) -> int:
    n_fish = 0
    for initial_timer, volume in groups.items():
        single_sim = simulate(initial_timer, n_days)
        total = len(single_sim) * volume
        n_fish += total
    return n_fish

def update_state(groups: Dict[int, int]) -> int:
    next_group = {i: 0 for i in range(9)}
    for initial_timer, volume in groups.items():
        single_sim = simulate(initial_timer, n_days=1)
        summary = get_groups(single_sim)
        for t, v in summary.items():
            next_group[t] += v * volume
    return next_group

def count_smart(groups: Dict[int, int], n_days: int) -> int:
    current_state = copy.deepcopy(groups)
    for _ in range(n_days):
        current_state = update_state(current_state)
    return sum(v for v in current_state.values())

def main() -> None:
    data = read_data("data/day6_input.txt")
    groups = get_groups(data)
    fish_80 = count_simple(groups, n_days=80)
    print(fish_80)
    fish_256 = count_smart(groups, n_days=256)
    print(fish_256)

if __name__ == "__main__":
    main()
