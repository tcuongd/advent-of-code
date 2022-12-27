import numpy as np
from collections import Counter, deque, defaultdict
import itertools
from typing import Tuple, List, Dict, Set

CONV = 3  # Assume square convolution
PAD = 2  # How many pixels to pad on each of the four sides
T_OFFSET = 1  # The starting point in the padded image to perform transformations

def read_data(input_path: str) -> Tuple[Tuple[int, int]]:
    with open(input_path, "r") as f:
        lines = f.readlines()
    mapping = np.array([m.replace('.', '0').replace('#', '1') for m in lines[0].strip()]).astype(int)
    image = []
    for l in lines[2:]:
        row = [int(c.replace('.', '0').replace('#', '1')) for c in l.strip()]
        image.append(row)
    image = np.array(image, dtype=int)
    return mapping, image

def get_adjacents(coord: Tuple[int, int]):
    adjs = []
    for dx in range(-T_OFFSET, T_OFFSET + 1):
        for dy in range(-T_OFFSET, T_OFFSET + 1):
            adjs.append((coord[0] + dx, coord[1] + dy))
    return adjs

def pad_image(image: np.array, default_value: int):
    padded = np.full(
        shape=(image.shape[0] + PAD * 2, image.shape[1] + PAD * 2),
        fill_value=default_value,
        dtype=int
    )
    padded[PAD:-PAD, PAD:-PAD] = image
    return padded

def convolve(image: np.array, default_value: int, mapping: np.array):
    padded = pad_image(image, default_value)
    new_default = mapping[int(str(default_value) * CONV ** 2, 2)]
    output = np.full_like(padded, new_default)
    for i, j in itertools.product(range(T_OFFSET, padded.shape[0] - T_OFFSET), range(T_OFFSET, padded.shape[1] - T_OFFSET)):
        bin_str = ''
        adjs = get_adjacents((i, j))
        for adj in adjs:
            bin_str += str(padded[adj])
        mapped = mapping[int(bin_str, 2)]
        output[i, j] = mapped
    return output, new_default

def main():
    mapping, image = read_data("data/day20_input.txt")
    convolved = image.copy()
    default = 0
    for i in range(50):
        convolved, default = convolve(convolved, default, mapping)
        if i == 1:
            print(f"After 2 enhances: {np.sum(convolved)}")
        if i == 49:
            print(f"After 50 enhances: {np.sum(convolved)}")

if __name__ == "__main__":
    main()
