from dataclasses import dataclass, replace
from math import lcm
from typing import Iterator

import heapq

Data = list[str]
Return = int


@dataclass
class Point:
    x: int
    y: int

    def neighbors(self, max_x: int, max_y: int) -> Iterator["Point"]:
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            next_x = self.x + dx
            next_y = self.y + dy

            if (
                (0 <= next_x < max_x and 0 <= next_y < max_y)
                or (next_x, next_y)
                == (
                    0,
                    -1,
                )
                or (next_x, next_y) == (max_x - 1, max_y)
            ):
                yield Point(next_x, next_y)

    def __add__(self, other: tuple[int, int]):
        return Point(self.x + other[0], self.y + other[1])

    def __eq__(self, other: "Point"):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class Blizzard:
    start: Point
    direction: tuple[int, int]
    width: int
    height: int

    def position_at(self, time: int) -> Point:
        next_x = (self.start.x + self.direction[0] * time) % self.width
        next_y = (self.start.y + self.direction[1] * time) % self.height

        return Point(next_x, next_y)

    def __hash__(self):
        return hash((self.start, self.direction, self.width, self.height))


@dataclass
class State:
    time: int
    position: Point

    def cost(self) -> int:
        return self.time - self.position.x - self.position.y

    def __lt__(self, other: "State"):
        return self.cost() < other.cost()

    def __hash__(self):
        return hash((self.time, self.position))


def parse_data(data: str) -> tuple[int, int, list[Blizzard]]:
    lines = data.splitlines()

    width = len(lines[0]) - 2
    height = len(lines) - 2
    blizzards = []

    for i, line in enumerate(lines[1:]):
        for j, char in enumerate(line[1:-1]):
            if char == ">":
                direction = (1, 0)
            elif char == "<":
                direction = (-1, 0)
            elif char == "^":
                direction = (0, -1)
            elif char == "v":
                direction = (0, 1)
            else:
                continue

            start = Point(j, i)
            blizzards.append(Blizzard(start, direction, width, height))

    return width, height, blizzards


def get_state(
    width: int, height: int, blizzards: list[Blizzard], time: int
) -> set[Point]:
    state = set()
    for blizzard in blizzards:
        state.add(blizzard.position_at(time))
    return state


def get_states(
    width: int, height: int, blizzards: list[Blizzard]
) -> Iterator[set[Point]]:
    max_time = lcm(width, height)
    for time in range(max_time):
        yield get_state(width, height, blizzards, time)


def astar(
    start: Point,
    goal: Point,
    width: int,
    height: int,
    blizzards: list[Blizzard],
    t=0,
) -> int:
    queue = []
    seen = set()
    heapq.heapify(queue)
    states = list(get_states(width, height, blizzards))
    heapq.heappush(queue, State(t, start))

    while queue:
        current = heapq.heappop(queue)
        if current.position == goal:
            return current.time
        if replace(current, time=current.time % len(states)) in seen:
            continue
        seen.add(replace(current, time=current.time % len(states)))

        for neighbor in current.position.neighbors(width, height):
            blizzard_positions = states[(current.time + 1) % len(states)]

            if neighbor not in blizzard_positions:
                heapq.heappush(queue, State(current.time + 1, neighbor))
        if current.position not in blizzard_positions:
            heapq.heappush(queue, State(current.time + 1, current.position))


def part_1(input: str) -> Return:
    width, height, blizzards = parse_data(input)
    start = Point(0, -1)
    goal = Point(width - 1, height)

    return astar(start, goal, width, height, blizzards)


def part_2(input: str) -> Return:
    width, height, blizzards = parse_data(input)
    start = Point(0, -1)
    goal = Point(width - 1, height)

    t1 = astar(start, goal, width, height, blizzards)
    t2 = astar(goal, start, width, height, blizzards, t1)
    return astar(start, goal, width, height, blizzards, t2)


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = fp.read()

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
