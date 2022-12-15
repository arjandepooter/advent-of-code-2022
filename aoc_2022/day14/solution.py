Point = tuple[int, int]
Data = set[Point]
Return = int


def parse_data(data: str) -> Data:
    points = set()
    for line in data.splitlines():
        parts = []
        for part in line.split(" -> "):
            x, y = part.split(",")
            x, y = int(x), int(y)
            parts.append((x, y))
        for (x1, y1), (x2, y2) in zip(parts, parts[1:]):
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    points.add((x, y))
    return points


def flow(grid: set[Point], max_y: int) -> int:
    x, y = 500, 0
    seen = set()
    stack = []

    while y != max_y:
        for dx, dy in (0, 1), (-1, 1), (1, 1):
            if (nx := x + dx, ny := y + dy) not in grid and (nx, ny) not in seen:
                stack.append((x, y))
                x, y = nx, ny
                break
        else:
            seen.add((x, y))
            x, y = stack.pop()

    return len(seen)


def dfs(grid: set[Point], floor: int) -> int:
    queue = [(500, 0)]
    visited = set()

    for x, y in queue:
        if (x, y) in visited:
            continue

        visited.add((x, y))
        for dx, dy in (0, 1), (-1, 1), (1, 1):
            if (x + dx, y + dy) not in grid and y + dy < floor:
                queue.append((x + dx, y + dy))

    return len(visited)


def part_1(input: str) -> Return:
    grid = parse_data(input)
    max_y = max(y for _, y in grid)

    return flow(grid, max_y)


def part_2(input: str) -> Return:
    grid = parse_data(input)
    floor = max(y for _, y in grid) + 2

    return dfs(grid, floor)


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = fp.read()

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
