import numpy as np
from typing import Callable, List, Tuple

def read_data(input_path: str) -> List[int]:
    with open(input_path, "r") as f:
        data = f.read().strip().split(",")
        data = np.array(data).astype(int)
    return data

def get_differences(data: List[int], x: int) -> np.array:
    return np.abs(np.array(data) - np.array(x))

def get_differences_expensive(data: List[int], x: int) -> np.array:
    """
    Series sum from 1 to n: n(n+1) / 2
    """
    diffs = get_differences(data, x)
    return (diffs * (diffs + 1) / 2).astype(int)

def get_min_fuel(data: List[int], fuel_fn: Callable) -> Tuple[int, int]:
    data = np.array(data, dtype=int)
    fuels = []
    for i in range(max(data) + 1):
        diffs = fuel_fn(data, i)
        fuels.append(np.sum(diffs))
    return np.min(fuels), np.argmin(fuels)

def main() -> None:
    data = read_data("data/day7_input.txt")
    mins = get_min_fuel(data, get_differences)
    print(f"Linear fuel: Total fuel={mins[0]}, Position={mins[1]}")
    mins_growth = get_min_fuel(data, get_differences_expensive)
    print(f"Growing fuel: Total fuel={mins_growth[0]}, Position={mins_growth[1]}")

if __name__ == "__main__":
    main()
