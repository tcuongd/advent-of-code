from typing import Dict, Tuple

def columnwise_bits(input_path: str) -> Dict[str, int]:
    with open(input_path, "r") as f:
        N_ones = []
        for i, binary in enumerate(f):
            binary = binary.strip()
            if i == 0:
                N_ones = [0 for _ in binary]
            for j, d in enumerate(binary):
                if d == '1':
                    N_ones[j] += 1
            N = i + 1
    return {'N_ones': N_ones, 'N': N}

def get_gamma_epsilon(columnwise_bits: Dict[str, int]) -> Tuple[str, str]:
    eps = ''
    gamma = ''
    for n in columnwise_bits['N_ones']:
        # If 1 is the most common bit
        if n > columnwise_bits['N'] / 2:
            gamma += '1'
            eps += '0'
        else:
            gamma += '0'
            eps += '1'
    return gamma, eps

def calculate_decimal_product(gamma_eps: Tuple[str, str]) -> int:
    gamma, eps = int(gamma_eps[0], 2), int(gamma_eps[1], 2)
    return gamma * eps

def main():
    c_bits = columnwise_bits("data/day3_input.txt")
    print(c_bits)
    gamma_eps = get_gamma_epsilon(c_bits)
    print(f"gamma: {gamma_eps[0]}, eps: {gamma_eps[1]}")
    power = calculate_decimal_product(gamma_eps)
    print(f"Power: {power}")

if __name__ == "__main__":
    main()
