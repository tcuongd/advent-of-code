import copy

# from bottom (left) to top (right)
STACKS = [
    ["Z", "N"],
    ["M", "C", "D"],
    ["P"],
]

STACKS = [
    ["S", "Z", "P", "D", "L", "B", "F", "C"],
    ["N", "V", "G", "P", "H", "W", "B"],
    ["F", "W", "B", "J", "G"],
    ["G", "J", "N", "F", "L", "W", "C", "S"],
    ["W", "J", "L", "T", "P", "M", "S", "H"],
    ["B", "C", "W", "G", "F", "S"],
    ["H", "T", "P", "M", "Q", "B", "W"],
    ["F", "S", "W", "T"],
    ["N", "C", "R"],
]


def read_instructions() -> list[tuple[int, int, int]]:
    with open("day5.txt", "r") as f:
        raw = [l.strip().split(" ") for l in f.readlines()]
    return [(int(l[1]), int(l[3]), int(l[5])) for l in raw]


def adjust_stack(
    instructions: list[tuple[int, int, int]], stacks: list[list[str]]
) -> list[list[str]]:
    stacks = copy.deepcopy(stacks)
    for n_move, from_stack, to_stack in instructions:
        for _ in range(n_move):
            target_letter = stacks[from_stack - 1].pop()
            stacks[to_stack - 1].append(target_letter)
    return stacks


def adjust_stack_simul(
    instructions: list[tuple[int, int, int]], stacks: list[list[str]]
) -> list[list[str]]:
    stacks = copy.deepcopy(stacks)
    for n_move, from_stack, to_stack in instructions:
        target_letters = stacks[from_stack - 1][-n_move:]
        stacks[to_stack - 1].extend(target_letters)
        del stacks[from_stack - 1][-n_move:]
    return stacks


def get_tops(stacks: list[list[str]]) -> str:
    return "".join([s[-1] for s in stacks])


instructions = read_instructions()
final_stack = adjust_stack(instructions, STACKS)
print(get_tops(final_stack))
final_stack_simul = adjust_stack_simul(instructions, STACKS)
print(get_tops(final_stack_simul))
