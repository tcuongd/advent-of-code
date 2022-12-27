import itertools
from collections import deque, Counter
from typing import Optional


def read_data() -> list[complex]:
    elves = []
    with open("day23.txt", "r") as f:
        raw = [l.strip() for l in f.readlines()]
    for y, line in enumerate(raw):
        for x, c in enumerate(line):
            if c == "#":
                elves.append(complex(x, -y))
    return elves


def get_proposal_config() -> tuple[deque, deque]:
    """Returns the original (move direction, checks) ordering."""
    return deque([0 + 1j, 0 - 1j, -1 + 0j, 1 + 0j]), deque(
        [
            (0 + 1j, 1 + 1j, -1 + 1j),
            (0 - 1j, 1 - 1j, -1 - 1j),
            (-1 + 0j, -1 + 1j, -1 - 1j),
            (1 + 0j, 1 + 1j, 1 - 1j),
        ]
    )


def all_adjacent_empty(elves: tuple[complex], current_elf: complex) -> bool:
    all_empty = True
    for dx, dy in itertools.product((-1, 0, 1), (-1, 0, 1)):
        if (dx, dy) != (0, 0):
            if current_elf + complex(dx, dy) in elves:
                all_empty = False
                break
    return all_empty


def do_round(
    elves: list[complex],
    proposal_checks: deque[tuple[complex, ...]],
    proposal_directions: deque[complex],
) -> list[complex]:
    """Modifies `elves` in-place."""
    starting_positions = tuple(elves)
    # Proposals
    proposals = {}
    settled = []
    for i, current in enumerate(starting_positions):
        if all_adjacent_empty(starting_positions, current):
            settled.append(current)
            continue
        for deltas, proposal_direction in zip(proposal_checks, proposal_directions):
            found = [current + delta in starting_positions for delta in deltas]
            if any(found):
                continue
            else:
                proposals[i] = current + proposal_direction
                break
    # Movements
    all_proposed = Counter([p for p in proposals.values()])
    for i, proposed in proposals.items():
        if all_proposed[proposed] == 1:
            elves[i] = proposed
    return settled


def do_rounds(data: list[complex], n_rounds: Optional[int] = None) -> tuple[list[complex], int]:
    elves = [e for e in data]
    proposal_directions, proposal_checks = get_proposal_config()
    rounds = 0
    while True:
        snapshot = [e for e in elves]
        _ = do_round(elves, proposal_checks, proposal_directions)
        rounds += 1
        if rounds == n_rounds:
            break
        elif n_rounds is None and snapshot == elves:
            break
        # Change order
        proposal_directions.append(proposal_directions.popleft())
        proposal_checks.append(proposal_checks.popleft())
    return elves, rounds


def get_bounded_area(elves: list[complex]) -> int:
    leftmost = min([coord.real for coord in elves])
    rightmost = max([coord.real for coord in elves])
    downmost = min([coord.imag for coord in elves])
    upmost = max([coord.imag for coord in elves])
    return int((rightmost - leftmost + 1) * (upmost - downmost + 1))


data = read_data()
final, rounds = do_rounds(data, 10)
bounded_area = get_bounded_area(final)
print(bounded_area - len(final))
steady_state, ss_rounds = do_rounds(data)
print(ss_rounds)
