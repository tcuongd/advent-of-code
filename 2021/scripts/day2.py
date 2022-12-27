from typing import Tuple

def calculate_position(input_path: str) -> Tuple[int, int]:
    horizontal = 0
    depth = 0
    with open(input_path, "r") as f:
        for instruction_raw in f:
            instruction = instruction_raw.split(" ")
            instruction[1] = int(instruction[1])
            if instruction[0] == "forward":
                horizontal += instruction[1]
            elif instruction[0] == "down":
                depth += instruction[1]
            elif instruction[0] == "up":
                depth -= instruction[1]
    return horizontal, depth

def calculate_position_corrected(input_path: str) -> Tuple[int, int]:
    horizontal = 0
    depth = 0
    aim = 0
    with open(input_path, "r") as f:
        for instruction_raw in f:
            instruction = instruction_raw.split(" ")
            instruction[1] = int(instruction[1])
            if instruction[0] == "forward":
                horizontal += instruction[1]
                depth += aim * instruction[1]
            elif instruction[0] == "down":
                aim += instruction[1]
            elif instruction[0] == "up":
                aim -= instruction[1]
    return horizontal, depth

def main():
    final_position_1 = calculate_position("data/day2_input.txt")
    print(f"Instructions 1 product: {final_position_1[0] * final_position_1[1]}")
    final_position_2 = calculate_position_corrected("data/day2_input.txt")
    print(f"Instructions 2 product: {final_position_2[0] * final_position_2[1]}")

if __name__ == "__main__":
    main()
