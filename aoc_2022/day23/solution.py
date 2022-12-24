from dataclasses import dataclass
from collections import Counter, defaultdict, deque


@dataclass
class Point:
    x: int
    y: int

    def __eq__(self, other: object) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, other: tuple[int, int]) -> "Point":
        return Point(self.x + other[0], self.y + other[1])

    def neighbours(self) -> list["Point"]:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                yield Point(self.x + dx, self.y + dy)


Data = list[Point]
Return = int


CHECKS = dict(
    [
        ((0, -1), ((0, -1), (-1, -1), (1, -1))),
        ((0, 1), ((0, 1), (-1, 1), (1, 1))),
        ((1, 0), ((1, 0), (1, -1), (1, 1))),
        ((-1, 0), ((-1, 0), (-1, -1), (-1, 1))),
    ]
)


def parse_data(data: str) -> Data:
    points = []
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if char == "#":
                points.append(Point(x, y))
    return points


def tick(
    points: list[Point], checks: list[tuple[int, int]]
) -> tuple[list[Point], bool]:
    proposed_points: defaultdict[Point, list[Point]] = defaultdict(list)
    s_points = set(points)
    next_points = []
    moved = False

    for point in points:
        if all(n not in s_points for n in point.neighbours()):
            next_points.append(point)
            continue

        for check in checks:
            if all((point + d) not in s_points for d in CHECKS[check]):
                proposed_points[point + check].append(point)
                break
        else:
            proposed_points[point].append(point)

    for next_point, points in proposed_points.items():
        if len(points) == 1:
            if next_point != points[0]:
                moved = True
            next_points.append(next_point)
        else:
            for point in points:
                next_points.append(point)

    return next_points, moved


def bounding_box(points: list[Point]) -> tuple[Point, Point]:
    min_x = min(point.x for point in points)
    min_y = min(point.y for point in points)
    max_x = max(point.x for point in points)
    max_y = max(point.y for point in points)
    return Point(min_x, min_y), Point(max_x, max_y)


def part_1(input: str) -> Return:
    points = parse_data(input)
    checks = deque([(0, -1), (0, 1), (-1, 0), (1, 0)])

    for _ in range(10):
        points, _ = tick(points, list(checks))
        checks.rotate(-1)

    min_point, max_point = bounding_box(points)

    return (max_point.x - min_point.x + 1) * (max_point.y - min_point.y + 1) - len(
        points
    )


def part_2(input: str) -> Return:
    points = parse_data(input)
    checks = deque([(0, -1), (0, 1), (-1, 0), (1, 0)])
    rounds = 0

    while True:
        points, moved = tick(points, list(checks))
        checks.rotate(-1)
        rounds += 1
        if not moved:
            break

    return rounds


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = fp.read()

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
