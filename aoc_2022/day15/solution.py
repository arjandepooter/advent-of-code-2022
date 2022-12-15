from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int

    def distance(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


Data = list[tuple[Point, Point]]
Return = int


def parse_data(data: str) -> Data:
    pairs = []

    for line in data.splitlines():
        parts = line.split(" ")
        x1 = int(parts[2].strip(",")[2:])
        y1 = int(parts[3].strip(":")[2:])
        x2 = int(parts[8].strip(",")[2:])
        y2 = int(parts[9].strip(":")[2:])
        pairs.append((Point(x1, y1), Point(x2, y2)))

    return pairs


def clamp(x: int, _min: int, _max: int):
    return max(min(x, _max), _min)


def part_1(input: str, row=10_000) -> Return:
    sensors = parse_data(input)
    points = {}

    for sensor, beacon in sensors:
        reach = sensor.distance(beacon)
        dist = abs(sensor.y - row)
        for x in range(sensor.x - reach + dist, sensor.x + reach - dist + 1):
            if x not in points:
                points[x] = False

        if beacon.y == row:
            points[beacon.x] = True

    return len([x for x in points.values() if x == False])


def part_2(input: str, bound=4_000_000) -> Return:
    sensors = parse_data(input)
    reaches = [sensor.distance(beacon) for sensor, beacon in sensors]

    for row in range(bound):
        lines = []
        for (sensor, beacon), reach in zip(sensors, reaches):
            dist = abs(sensor.y - row)
            lines.append(
                (
                    clamp(sensor.x - (reach - dist), 0, bound),
                    clamp(sensor.x + (reach - dist), 0, bound) + 1,
                )
            )
        lines.sort()
        x = 0
        for start, end in lines:
            if start > x:
                return x * 4_000_000 + row
            x = max(x, end)


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = fp.read()

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
