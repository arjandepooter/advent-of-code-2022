Data = list[tuple[str, int]]
Return = int


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def zero(cls):
        return cls(0, 0)

    def move(self, direction) -> "Point":
        point = Point(self.x, self.y)

        if direction == "U":
            point.y += 1
        elif direction == "D":
            point.y -= 1
        elif direction == "L":
            point.x -= 1
        elif direction == "R":
            point.x += 1

        return point

    def is_touching(self, other: "Point"):
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1

    def move_towards(self, other: "Point") -> "Point":
        dx = (other.x - self.x) // abs(other.x - self.x) if self.x != other.x else 0
        dy = (other.y - self.y) // abs(other.y - self.y) if self.y != other.y else 0

        return Point(self.x + dx, self.y + dy)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


def parse_data(data: str) -> Data:
    moves = []
    for line in data.splitlines():
        direction, distance = line.split()
        moves.append((direction, int(distance)))
    return moves


def part_1(input: str) -> Return:
    moves = parse_data(input)

    start = Point.zero()
    head = start
    tail = start
    visited = {tail}

    for direction, distance in moves:
        for _ in range(distance):
            head = head.move(direction)

            if not head.is_touching(tail):
                tail = tail.move_towards(head)

            visited.add(tail)

    return len(visited)


def part_2(input: str) -> Return:
    moves = parse_data(input)

    knots = [Point.zero() for _ in range(10)]
    visited = set()

    for direction, distance in moves:
        for _ in range(distance):
            knots[0] = knots[0].move(direction)

            for i, (head, tail) in enumerate(zip(knots, knots[1:])):
                if not head.is_touching(tail):
                    knots[i + 1] = tail.move_towards(head)

            visited.add(knots[-1])

    return len(visited)
