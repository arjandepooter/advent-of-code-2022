Data = list[list[tuple[int, int]]]
Return = int


def parse_data(data: str) -> Data:
    paths = []
    for line in data.splitlines():
        parts = []
        for part in line.split(" -> "):
            x, y = part.split(",")
            x, y = int(x), int(y)
            parts.append((x, y))
        paths.append(parts)
    return paths


def fill_grid(paths: list[list[tuple[int, int]]]) -> set[tuple[int, int]]:
    grid = set()

    for path in paths:
        for (x1, y1), (x2, y2) in zip(path, path[1:]):
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    grid.add((x, y))

    return grid


def flow(grid: set[tuple[int, int]], max_y, floor=None) -> bool:
    x, y = 500, 0
    while y <= max_y and (x, y) not in grid:
        if floor is not None and y + 1 >= floor:
            grid.add((x, y))
            return True

        for dx, dy in (0, 1), (-1, 1), (1, 1):
            if (x + dx, y + dy) not in grid:
                x += dx
                y += dy
                break
        else:
            grid.add((x, y))
            return True

    return False


def part_1(input: str) -> Return:
    data = parse_data(input)
    grid = fill_grid(data)
    max_y = max(y for _, y in grid)

    acc = 0
    while flow(grid, max_y):
        acc += 1

    return acc


def part_2(input: str) -> Return:
    data = parse_data(input)
    grid = fill_grid(data)
    floor = max(y for _, y in grid) + 2

    acc = 0
    while flow(grid, floor, floor):
        acc += 1

    return acc


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = fp.read()

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
