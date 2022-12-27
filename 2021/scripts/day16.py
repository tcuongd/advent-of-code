from typing import List, Tuple
import numpy as np
from collections import deque
import json

from numpy.lib.arraysetops import isin

HEXS = {
    '0' : '0000',
    '1' : '0001',
    '2' : '0010',
    '3' : '0011',
    '4' : '0100',
    '5' : '0101',
    '6' : '0110',
    '7' : '0111',
    '8' : '1000',
    '9' : '1001',
    'A' : '1010',
    'B' : '1011',
    'C' : '1100',
    'D' : '1101',
    'E' : '1110',
    'F' : '1111',
}

def decode_hex(chars: str) -> str:
    bin_str = ''
    for char in chars:
        bin_str += HEXS[char]
    return bin_str

def parse_literal(bin_str: str) -> Tuple[int, int]:
    number_bin = ''
    is_last_group = False
    len_bin = 0
    for i, char in enumerate(bin_str):
        if is_last_group:
            break
        if i % 5 == 0:
            # 0 1 2 3 4  5 6 7 8 9  10 11 12 13 14
            number_bin += bin_str[(i+1):(i+5)]
            len_bin += 5
            if char == '0':
                is_last_group = True
    return int(number_bin, 2), len_bin

def parse_operator(operator: str) -> int:
    if operator[0] == '0':
        bin_length = 15
        sub_packet_length = int(operator[1:(1 + bin_length)], 2)
        sub_packet = operator[(1+bin_length):]
        return sub_packet, sub_packet_length, 'length'
    elif operator[0] == '1':
        bin_length = 11
        n_sub_packets = int(operator[1:(1 + bin_length)], 2)
        sub_packet = operator[(1+bin_length):]
        return sub_packet, n_sub_packets, 'num'

def _values_operation(packet_type: int, values: List[int]):
    if packet_type == 0:
        return int(np.sum(values))
    elif packet_type == 1:
        return int(np.product(values))
    elif packet_type == 2:
        return int(np.min(values))
    elif packet_type == 3:
        return int(np.max(values))
    elif packet_type == 5:
        return 1 if values[0] > values[1] else 0
    elif packet_type == 6:
        return 1 if values[0] < values[1] else 0
    elif packet_type == 7:
        return 1 if values[0] == values[1] else 0

def values_operation(instruction: list):
    for i, elem in enumerate(instruction):
        if isinstance(elem, list):
            if isinstance(elem[0], int) and isinstance(elem[1], list) and all(isinstance(el, int) for el in elem[1]):
                # instruction = [ [0, [1, 2, 3]] , [1, [2, 3, 4]] ]
                # instruction[i] = elem = [0, [1, 2, 3]]
                # one level up = [ 7 , [ [0, [1, 2, 3]] , [1, [2, 3, 4]] ] ]
                # want: [ 7,  [ 6 , 24 ] ]
                instruction[i] = _values_operation(elem[0], elem[1])
            else:
                values_operation(elem)

def parse_message(bin_str: str, versions: List[int], value_tree: list, types: List[int], intermediates: List[int] = None):
    if len(bin_str) < 6 or bin_str == '0'*len(bin_str):
        return ''

    version = int(bin_str[:3], 2)
    versions.append(version)
    bin_str = bin_str[3:]

    packet_type = int(bin_str[:3], 2)
    types.append(packet_type)
    bin_str = bin_str[3:]

    if packet_type == 4:
        decimal, len_bin = parse_literal(bin_str)
        intermediates.append(decimal)
        if len_bin > len(bin_str):
            return ''
        else:
            bin_str = bin_str[len_bin:]
    else:
        bin_str, ind, ind_type = parse_operator(bin_str)
        intermediates = []
        if ind_type == 'num':
            for _ in range(ind):
                bin_str = parse_message(bin_str, versions, value_tree, types, intermediates)
                if not bin_str:
                    break
        elif ind_type == 'length':
            chars_parsed = 0
            while chars_parsed < ind and bin_str:
                len_before = len(bin_str)
                bin_str = parse_message(bin_str, versions, value_tree, types, intermediates)
                len_after = len(bin_str)
                chars_parsed += (len_after - len_before)
        if intermediates:
            value_tree.append([packet_type, intermediates])
        else:
            value_tree.insert(0, [packet_type, value_tree.copy()])
            del value_tree[1:]
    return bin_str

def read_data(input_path) -> np.array:
    with open(input_path, "r") as f:
        hex_code = f.read().strip()
    return hex_code

def main():
    hex_chars = read_data("data/day16_input.txt")
    bin_str = decode_hex(hex_chars)
    versions = []
    types = []
    value_tree = []
    parse_message(bin_str, versions, value_tree, types)
    print(sum(versions))

    for i in range(36):
        print(i)
        print(value_tree)
        values_operation(value_tree)
        # with open("garbage.json", "w") as f:
        #     json.dump(value_tree, f, indent=1)

if __name__ == "__main__":
    main()
