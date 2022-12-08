from typing import Iterator


class Grid:
    def __init__(self, values: list[int], width: int, height: int):
        assert len(values) == width * height

        self.values = values
        self.width = width
        self.height = height

    def iter_row(self, r: int, reverse=False) -> Iterator[tuple[int, int, int]]:
        if reverse:
            for c in range(self.width - 1, -1, -1):
                yield r, c, self[r, c]
        else:
            for c in range(self.width):
                yield r, c, self[r, c]

    def iter_col(self, c: int, reverse=False) -> Iterator[tuple[int, int, int]]:
        if reverse:
            for r in range(self.height - 1, -1, -1):
                yield r, c, self[r, c]
        else:
            for r in range(self.height):
                yield r, c, self[r, c]

    def __getitem__(self, key: tuple[int, int]) -> int:
        r, c = key
        return self.values[r * self.width + c]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        r, c = key
        self.values[r * self.width + c] = value

    def __len__(self) -> int:
        return self.width * self.height

    def __iter__(self) -> Iterator[Iterator[tuple[int, int, int]]]:
        for r in range(self.height):
            yield self.iter_row(r)
            yield self.iter_row(r, reverse=True)
        for c in range(self.width):
            yield self.iter_col(c)
            yield self.iter_col(c, reverse=True)


def parse_data(data: str) -> Grid:
    lines = data.splitlines()
    width = len(lines[0])
    height = len(lines)
    values = [int(n) for line in lines for n in line]
    return Grid(values, width, height)


def part_1(grid: Grid) -> int:
    seen = set()
    for path in grid:
        m = -1
        for r, c, n in path:
            if n > m:
                seen.add((r, c))
                m = n

    return len(seen)


def part_2(grid: Grid) -> int:
    scores = [1] * len(grid)

    for path in grid:
        last_seen = [0] * 10
        for i, (r, c, n) in enumerate(path):
            score = i - max(last_seen[n:])
            scores[r * grid.width + c] *= score
            last_seen[n] = i

    return max(scores)


if __name__ == "__main__":
    import sys

    fp = sys.stdin if len(sys.argv) == 1 else open(sys.argv[1])
    grid = parse_data(fp.read())

    print(part_1(grid))
    print(part_2(grid))
