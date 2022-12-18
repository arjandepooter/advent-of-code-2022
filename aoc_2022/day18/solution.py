from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int
    z: int

    def neighbors(self):
        for dx, dy, dz in [
            (1, 0, 0),
            (-1, 0, 0),
            (0, 1, 0),
            (0, -1, 0),
            (0, 0, 1),
            (0, 0, -1),
        ]:
            yield Point(self.x + dx, self.y + dy, self.z + dz)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)


Data = list[str]
Return = int


def parse_data(data: str) -> Data:
    points = []
    for line in data.strip().splitlines():
        points.append(Point(*[int(p) for p in line.split(",")]))

    return points


def part_1(input: str) -> Return:
    points = set(parse_data(input))

    acc = 0
    for point in points:
        for neighbor in point.neighbors():
            if neighbor not in points:
                acc += 1

    return acc


def part_2(input: str) -> Return:
    points = set(parse_data(input))

    min_bound = Point(
        min(point.x for point in points),
        min(point.y for point in points),
        min(point.z for point in points),
    )
    max_bound = Point(
        max(point.x for point in points),
        max(point.y for point in points),
        max(point.z for point in points),
    )

    acc = 0
    for point in points:
        for neighbor in point.neighbors():
            if neighbor not in points:
                acc += 1

    adjacents = set()
    for point in points:
        for neighbor in point.neighbors():
            if neighbor not in points:
                adjacents.add(neighbor)

    for neighbor in adjacents:
        seen = set(points)
        queue = [neighbor]
        for p in queue:
            if p in seen or p in points:
                continue
            if (
                p.x < min_bound.x
                or p.x > max_bound.x
                or p.y < min_bound.y
                or p.y > max_bound.y
                or p.z < min_bound.z
                or p.z > max_bound.z
            ):
                break

            seen.add(p)
            queue.extend(p.neighbors())

        else:
            for n in neighbor.neighbors():
                if n in points:
                    acc -= 1

    return acc


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = fp.read()

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
