Grid = list[list[int]]
Data = Grid
Return = int


def parse_data(data: str) -> Data:
    grid = []

    for line in data.splitlines():
        grid.append([int(n) for n in line])

    return grid


def get_paths(
    grid: Grid, r: int, c: int
) -> tuple[list[int], list[int], list[int], list[int]]:
    return (
        [grid[r][i] for i in range(c + 1, len(grid[0]))],
        [grid[r][i] for i in range(c - 1, -1, -1)],
        [grid[i][c] for i in range(r + 1, len(grid))],
        [grid[i][c] for i in range(r - 1, -1, -1)],
    )


def part_1(input: str) -> Return:
    grid = parse_data(input)

    acc = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            paths = get_paths(grid, r, c)
            if any([len(path) == 0 or grid[r][c] > max(path) for path in paths]):
                acc += 1

    return acc


def part_2(input: str) -> Return:
    grid = parse_data(input)

    scores = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            score = 1
            val = grid[r][c]
            for path in get_paths(grid, r, c):
                sub_score = 0
                for n in path:
                    sub_score += 1
                    if n >= val:
                        break
                score *= sub_score
            scores.append(score)

    return max(scores)
