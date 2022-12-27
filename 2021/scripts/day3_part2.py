import numpy as np
from typing import List

def load_all_data(input_path: str) -> np.array:
    with open(input_path, "r") as f:
        data = f.readlines()
    data = [[int(d) for d in r.strip()] for r in data]
    return np.array(data).astype(int)

def extract_special_bit(data: np.array, col_index: int, return_most_common: bool, tiebreaker: int) -> int:
    N = data.shape[0]
    sum_bits = np.sum(data[:, col_index])
    if sum_bits > N / 2:
        bit_value = 1 if return_most_common else 0
    elif sum_bits == N / 2:
        bit_value = tiebreaker
    else:
        bit_value = 0 if return_most_common else 1
    return bit_value

def filter_rows(data: np.array, col_index: int, bit_value: int) -> np.array:
    """
    Filter `data` to keep only the rows where the value of `col_index` is equal to `bit_value`.
    """
    return data[data[:, col_index] == bit_value, :]

def find_o2_rating(data: np.array) -> List[int]:
    solution = np.copy(data)
    # Assume we will get a solution on first pass
    for col_index in range(data.shape[1]):
        special_bit = extract_special_bit(solution, col_index, return_most_common=True, tiebreaker=1)
        solution = filter_rows(solution, col_index, special_bit)
        if solution.shape[0] == 1:
            break
    if solution.shape[0] != 1:
        raise ValueError(
            "did not find unique solution to O2 rating after first pass." +
            f"still {solution.shape[0]} binary numbers to consider."
        )
    return solution[0]

def find_co2_rating(data: np.array) -> List[int]:
    solution = np.copy(data)
    # Assume we will get a solution on first pass
    for col_index in range(data.shape[1]):
        special_bit = extract_special_bit(solution, col_index, return_most_common=False, tiebreaker=0)
        solution = filter_rows(solution, col_index, special_bit)
        if solution.shape[0] == 1:
            break
    if solution.shape[0] != 1:
        raise ValueError(
            "did not find unique solution to CO2 rating after first pass." +
            f" still {solution.shape[0]} binary numbers to consider."
        )
    return solution[0]

def calculate_decimal_product(o2_rating: np.array, co2_rating: np.array) -> int:
    o2_binary_string = ''.join(o2_rating.astype(str))
    co2_binary_string = ''.join(co2_rating.astype(str))
    o2_decimal, co2_decimal = int(o2_binary_string, 2), int(co2_binary_string, 2)
    return o2_decimal * co2_decimal

def main() -> None:
    data = load_all_data("data/day3_input.txt")
    o2, co2 = find_o2_rating(data), find_co2_rating(data)
    print(f"o2: {o2}, co2: {co2}")
    product = calculate_decimal_product(o2, co2)
    print(f"life support rating: {product}")

if __name__ == "__main__":
    main()
