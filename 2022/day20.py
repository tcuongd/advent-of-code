import numpy as np


def read_data() -> list[int]:
    with open("day20.txt", "r") as f:
        raw = [int(l.strip()) for l in f.readlines()]
    return raw


def mix(
    data: list[int], modified_indices: list[int] = None, multiplier: int = 1, debug: bool = False
) -> list[int]:
    if modified_indices is None:
        modified_indices = [i for i in range(len(data))]
    l = len(data)
    for orig_idx in range(l):
        curr_idx = modified_indices.index(orig_idx)
        movement = data[orig_idx] * multiplier
        new_idx = curr_idx + movement
        if new_idx <= 0:
            new_idx = (l - 1) - abs(new_idx) % (l - 1)
        elif new_idx >= l - 1:
            new_idx = new_idx % (l - 1)
        del modified_indices[curr_idx]
        modified_indices.insert(new_idx, orig_idx)
        if debug:
            print(f"{new_idx=}")
            print(f"{modified_indices=}")
            print(f"final={np.array(data)[modified_indices].tolist()}")
    return modified_indices


def get_original_values(
    modified_indices: list[int], data: list[int], multiplier: int = 1
) -> list[int]:
    return (np.array(data)[modified_indices] * multiplier).tolist()


def get_final_indices(mixed: list[int]) -> list[int]:
    starting = mixed.index(0)
    l = len(data)
    idxs = []
    for offset in [1000, 2000, 3000]:
        idx = starting + offset
        if idx > l - 1:
            idx = idx % l
        idxs.append(idx)
    return idxs


def decrypt(data: list[int], key: int) -> list[int]:
    modified_indices = None
    for _ in range(10):
        modified_indices = mix(data, modified_indices, key)
    return modified_indices


data = read_data()
mixed_idx = mix(data)
mixed = get_original_values(mixed_idx, data)
idxs = get_final_indices(mixed)
print(np.array(mixed)[idxs])
print(sum(np.array(mixed)[idxs]))

KEY = 811589153
decrypted_idx = decrypt(data, KEY)
decrypted = get_original_values(decrypted_idx, data, KEY)
idxs = get_final_indices(decrypted)
print(np.array(decrypted)[idxs])
print(sum(np.array(decrypted)[idxs]))
