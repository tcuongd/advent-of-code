from itertools import cycle
from functools import lru_cache
from string import ascii_uppercase


class Rock:
    def __init__(self, order: int):
        self.order = order
        if order == 0:
            self.coords_relative = [3 + 4j, 4 + 4j, 5 + 4j, 6 + 4j]
        elif order == 1:
            self.coords_relative = [4 + 6j, 3 + 5j, 4 + 5j, 5 + 5j, 4 + 4j]
        elif order == 2:
            self.coords_relative = [5 + 6j, 5 + 5j, 3 + 4j, 4 + 4j, 5 + 4j]
        elif order == 3:
            self.coords_relative = [3 + 7j, 3 + 6j, 3 + 5j, 3 + 4j]
        elif order == 4:
            self.coords_relative = [3 + 5j, 4 + 5j, 3 + 4j, 4 + 4j]

    def __repr__(self) -> str:
        return str(self.coords)

    def spawn(self, surface_heights: list[int]) -> None:
        self.coords = [c + complex(0, max(surface_heights)) for c in self.coords_relative]

    def move_lr(self, direction: str, rocks: tuple["Rock"], grid_width: int) -> bool:
        """Move the rock left/right if possible. Returns whether the rock moved left/right or not."""
        moveable = []
        for coord in self.coords:
            filled = get_row(rocks, coord.imag, grid_width)
            blockers = [idx + 1 for idx, v in enumerate(filled) if v == 1]
            if direction == "<":
                if coord.real - 1 < 1:
                    moveable.append(False)
                elif blockers:
                    if any([coord.real - 1 == b for b in blockers]):
                        moveable.append(False)
                    else:
                        moveable.append(True)
                else:
                    moveable.append(True)
            elif direction == ">":
                if coord.real + 1 > grid_width:
                    moveable.append(False)
                elif blockers:
                    if any([coord.real + 1 == b for b in blockers]):
                        moveable.append(False)
                    else:
                        moveable.append(True)
                else:
                    moveable.append(True)
        if not all(moveable):
            return False
        else:
            if direction == "<":
                self.coords = [c - (1 + 0j) for c in self.coords]
            elif direction == ">":
                self.coords = [c + (1 + 0j) for c in self.coords]
            else:
                raise ValueError
            return True

    def move_down(self, rocks: tuple["Rock"]) -> bool:
        """Moves the rock down if possible. Returns whether the rock moved down or not"""
        moveable = []
        for coord in self.coords:
            underneath = get_underneath(rocks, coord.real, coord.imag)
            if coord.imag - 1 == underneath:
                moveable.append(False)
            else:
                moveable.append(True)
        if not all(moveable):
            return False
        else:
            self.coords = [c - (0 + 1j) for c in self.coords]
            return True


@lru_cache(maxsize=5000)
def get_underneath(rocks: tuple[Rock], column: int, current_height: int) -> int:
    greatest_underneath = 0
    for rock in rocks:
        for coord in rock.coords:
            if (
                coord.real == column
                and coord.imag < current_height
                and coord.imag > greatest_underneath
            ):
                greatest_underneath = coord.imag
    return greatest_underneath


@lru_cache(maxsize=5000)
def get_row(rocks: tuple[Rock], row: int, grid_width: int) -> list[int]:
    blocked = [0 for _ in range(grid_width)]
    for i in range(grid_width):
        detected = False
        for rock in rocks:
            if detected:
                break
            for coord in rock.coords:
                if coord.imag == row:
                    if coord.real == i + 1:
                        blocked[i] = 1
                        detected = True
                        break
    return blocked


def get_surface_heights(rocks: list[Rock], grid_width: int) -> list[int]:
    surface = [0 for _ in range(grid_width)]
    for i in range(1, grid_width + 1):
        heights = []
        for rock in rocks:
            for coord in rock.coords:
                if int(coord.real) == i:
                    heights.append(coord.imag)
        if heights:
            surface[i - 1] = int(max(heights))
    return surface


def read_data() -> str:
    with open("day17.txt", "r") as f:
        raw = f.readlines()[0].strip()
    return raw


def play(instructions: str, n_rounds: int, debug: bool = False) -> tuple[list[Rock], list[int]]:
    WIDTH = 7
    rocks = []
    lr_idx_generator = cycle(range(len(instructions)))
    for i in cycle(range(5)):
        surface = get_surface_heights(rocks, WIDTH)
        if len(rocks) > 0 and i == 0 and lr_idx == len(instructions) - 1:
            return rocks, surface
        if debug:
            print(f"{surface=}")
        rock = Rock(i)
        rock.spawn(surface)
        if debug:
            print(f"--- PIECE {ascii_uppercase[i]} ---")
            print(rock.coords)
        while True:
            lr_idx = next(lr_idx_generator)
            did_move_across = rock.move_lr(instructions[lr_idx], tuple(rocks), WIDTH)
            did_move_down = rock.move_down(tuple(rocks))
            if debug:
                print(instructions[lr_idx])
                print(did_move_across, did_move_down)
                print(rock.coords)
            if not did_move_down:
                rocks.append(rock)
                break
        if len(rocks) == n_rounds:
            return rocks, get_surface_heights(rocks, WIDTH)


def render_grid(rocks: list[Rock], grid_width: int) -> None:
    import numpy as np

    heights = get_surface_heights(rocks, grid_width)
    max_height = max(heights)
    grid = np.full((max_height, grid_width), dtype=int, fill_value=-1)
    for rock in rocks:
        for coord in rock.coords:
            grid[grid.shape[0] - int(coord.imag), int(coord.real) - 1] = rock.order
    str_grid = np.full_like(grid, dtype=str, fill_value=".")
    for i in range(5):
        str_grid[grid == i] = ascii_uppercase[i]
    with open("day17_grid.txt", "w") as f:
        for row in str_grid:
            f.write(" ".join(row))
            f.write("\n")


instructions = read_data()

rocks, surface = play(instructions, 2022)
print(f"{len(rocks)=}")
print(surface)
print(max(surface))
# 1000000000000
rocks, surface = play(instructions, 1000000000000)
