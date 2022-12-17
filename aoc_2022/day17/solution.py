from itertools import count, cycle
from math import lcm

Data = list[str]
Return = int


def parse_data(data: str) -> Data:
    return [c for n in data.splitlines() for c in n.strip()]


ROCKS = (
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),
    ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 0), (1, 0), (0, 1), (1, 1)),
)


def process_rock(rock, grid, moves, move_idx):
    max_y = max(y for _, y in grid)
    rock = set((x + 2, y + max_y + 4) for x, y in rock)

    while True:
        move = moves[move_idx]
        move_idx = (move_idx + 1) % len(moves)

        if move == "<" and not any(x == 0 for x, _ in rock):
            next_rock = set((x - 1, y) for x, y in rock)
        elif move == ">" and not any(x == 6 for x, _ in rock):
            next_rock = set((x + 1, y) for x, y in rock)
        else:
            next_rock = rock

        if not (next_rock & grid):
            rock = next_rock

        next_rock = set((x, y - 1) for x, y in rock)
        if next_rock & grid:
            grid |= rock
            return move_idx
        rock = next_rock


def print_grid(grid):
    max_y = max(y for _, y in grid)

    for y in range(max_y, -1, -1):
        for x in range(7):
            if (x, y) in grid:
                print("#", end="")
            else:
                print(".", end="")
        print()

    print()


def part_1(input: str) -> Return:
    moves = parse_data(input)
    move_idx = 0
    grid = set((x, 0) for x in range(7))

    for _, rock in zip(range(2022), cycle(ROCKS)):
        move_idx = process_rock(rock, grid, moves, move_idx)

    return max(y for x, y in grid)


def part_2(input: str) -> Return:
    N = 1_000_000_000_000
    n = 0

    moves = parse_data(input)
    move_idx = 0
    grid = set((x, 0) for x in range(7))
    height = 0

    states = {}

    while n < N:
        rock_idx = n % len(ROCKS)
        rock = ROCKS[rock_idx]

        move_idx = process_rock(rock, grid, moves, move_idx)

        if height == 0:
            max_y = max(y for _, y in grid)
            snapshot = frozenset((x, max_y - y) for x, y in grid if y >= max_y - 10)
            state = (rock_idx, move_idx, snapshot)
            if state in states:
                prev_max_y, prev_n = states[state]
                period = n - prev_n
                dy = max_y - prev_max_y
                height = (N - n) // period * dy
                n += (N - n) // period * period
            states[state] = (max_y, n)

        n += 1

    return height + max(y for _, y in grid)


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = fp.read()

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
