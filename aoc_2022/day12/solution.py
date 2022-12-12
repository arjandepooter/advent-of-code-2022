from collections import deque
from itertools import product
from typing import Iterator

Data = list[list[int]]
Return = int


def parse_data(data: str) -> tuple[Data, tuple[int, int], tuple[int, int]]:
    grid = []
    row = []
    start = end = None

    for r, line in enumerate(data.splitlines()):
        row = []
        for c, cur in enumerate(line):
            if cur == "S":
                row.append(0)
                start = (r, c)
            elif cur == "E":
                row.append(25)
                end = (r, c)
            else:
                row.append(ord(cur) - ord("a"))

        grid.append(row)

    return grid, start, end


def iter_neighbors(grid: Data, pos: tuple[int, int]) -> Iterator[tuple[int, int]]:
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        r, c = pos[0] + dr, pos[1] + dc
        if not (
            r < 0
            or c < 0
            or r >= len(grid)
            or c >= len(grid[0])
            or grid[pos[0]][pos[1]] + 1 < grid[r][c]
        ):
            yield (r, c)


def get_path(
    grid: list[list[int]], starts: list[tuple[int, int]], end: tuple[int, int]
) -> int | None:
    queue = deque((0, start) for start in starts)
    visited = set()

    while queue:
        dist, (r, c) = queue.popleft()

        if (r, c) == end:
            return dist
        if (r, c) in visited:
            continue

        visited.add((r, c))

        for rn, rc in iter_neighbors(grid, (r, c)):
            queue.append((dist + 1, (rn, rc)))


def part_1(input: str) -> Return:
    grid, start, end = parse_data(input)

    path = get_path(grid, [start], end)

    return path


def part_2(input: str) -> Return:
    grid, _, end = parse_data(input)

    starts = [
        (r, c)
        for r, c in product(range(len(grid)), range(len(grid[0])))
        if grid[r][c] == 0
    ]

    return get_path(grid, starts, end)
