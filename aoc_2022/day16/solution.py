from collections import deque
from dataclasses import dataclass
from functools import cache
from itertools import product

import heapq as hq
import re


@dataclass
class Valve:
    rate: int
    id: str
    edges: list[str]


Data = dict[str, Valve]
Return = int


def parse_data(data: str) -> Data:
    valves = {}

    for line in data.splitlines():
        if m := re.match(
            r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)", line
        ):
            valve = Valve(int(m[2]), m[1], m[3].split(", "))
            valves[valve.id] = valve
        else:
            print("No match")

    return valves


def max_flow(valves: dict[str, Valve], max_t: int, cur="AA", t=0) -> int:
    @dataclass
    class State:
        valve_1: Valve
        valve_2: Valve
        rate: int = 0
        opened: frozenset = frozenset()
        time: int = 0
        total: int = 0

        def __hash__(self):
            return hash(
                (self.valve_1.id, self.valve_2.id, self.time, self.rate, self.opened)
            )

        def __eq__(self, other):
            return (
                (
                    (
                        self.valve_1.id == other.valve_1.id
                        and self.valve_2.id == other.valve_2.id
                    )
                    or (
                        self.valve_1.id == other.valve_2.id
                        and self.valve_2.id == other.valve_1.id
                    )
                )
                and self.time == other.time
                and self.rate == other.rate
                and self.opened == other.opened
            )

        @property
        def score(self):
            if hasattr(self, "_score"):
                return self._score

            score = self.total + self.rate * (max_t - self.time)
            rates = sorted([valves[n].rate for n in set(valves.keys()) - self.opened])
            for i in range(self.time + 1, max_t, 2):
                score += (max_t - i) * sum(rates[-2:])
                rates = rates[:-2]

            self._score = score
            return score

        def neighbours(self):
            can_be_opened_1 = (
                self.valve_1.id not in self.opened and self.valve_1.rate > 0
            )
            can_be_opened_2 = (
                self.valve_2.id not in self.opened
                and self.valve_2.rate > 0
                and self.valve_2.id != self.valve_1.id
            )

            for edge_1 in self.valve_1.edges + (
                [self.valve_1.id] if can_be_opened_1 else []
            ):
                for edge_2 in self.valve_2.edges + (
                    [self.valve_2.id] if can_be_opened_2 else []
                ):
                    opens = set()
                    if edge_1 == self.valve_1.id:
                        opens.add(self.valve_1.id)
                    if edge_2 == self.valve_2.id:
                        opens.add(self.valve_2.id)

                    rate = self.rate
                    if edge_1 == self.valve_1.id:
                        rate += self.valve_1.rate
                    if edge_2 == self.valve_2.id:
                        rate += self.valve_2.rate

                    yield State(
                        valves[edge_1],
                        valves[edge_2],
                        rate,
                        self.opened | opens,
                        self.time + 1,
                        self.total + self.rate,
                    )

        def __lt__(self, other):
            return self.score > other.score

    queue = [State(valves[cur], valves[cur])]
    hq.heapify(queue)
    visited = set()

    n = 0

    while queue:
        n += 1
        state = hq.heappop(queue)

        if state.time == max_t:
            print(n)
            return state.total
        if state in visited:
            continue
        visited.add(state)

        for neighbour in state.neighbours():
            hq.heappush(queue, neighbour)


def part_1(input: str) -> Return:
    valves = parse_data(input)
    # butchered part 2 in part 1 implementation so need to rewrite
    raise NotImplementedError


def part_2(input: str) -> Return:
    valves = parse_data(input)

    return max_flow(valves, 26)


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = fp.read()

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
