from dataclasses import dataclass, replace
from functools import cache
import heapq as hq
import re
from typing import Iterator


@dataclass
class Blueprint:
    id: int
    ore: int  # (ore)
    clay: int  # (ore)
    obsidian: tuple[int, int]  # (ore, clay)
    geode: tuple[int, int]  # (ore, obsidian)


@dataclass
class State:
    time_left: int
    blueprint: Blueprint
    ore: int = 0
    ore_robots: int = 1
    clay: int = 0
    clay_robots: int = 0
    obsidian: int = 0
    obsidian_robots: int = 0
    geode_robots: int = 0

    def __hash__(self):
        return hash(
            (
                self.time_left,
                self.ore,
                self.ore_robots,
                self.clay,
                self.clay_robots,
                self.obsidian,
                self.obsidian_robots,
                self.geode_robots,
            )
        )

    def next_states(self) -> Iterator["State"]:
        next_state = replace(
            self,
            time_left=self.time_left - 1,
            ore=self.ore + self.ore_robots,
            clay=self.clay + self.clay_robots,
            obsidian=self.obsidian + self.obsidian_robots,
        )

        if (
            self.ore >= self.blueprint.geode[0]
            and self.obsidian >= self.blueprint.geode[1]
        ):
            yield replace(
                next_state,
                ore=next_state.ore - self.blueprint.geode[0],
                obsidian=next_state.obsidian - self.blueprint.geode[1],
                geode_robots=next_state.geode_robots + 1,
            )
            return
        if (
            self.ore >= self.blueprint.obsidian[0]
            and self.clay >= self.blueprint.obsidian[1]
            and self.obsidian_robots < self.blueprint.geode[1]
        ):
            yield replace(
                next_state,
                ore=next_state.ore - self.blueprint.obsidian[0],
                clay=next_state.clay - self.blueprint.obsidian[1],
                obsidian_robots=next_state.obsidian_robots + 1,
            )
            return
        if (
            self.ore >= self.blueprint.clay
            and self.clay_robots < self.blueprint.obsidian[1]
        ):
            yield replace(
                next_state,
                ore=next_state.ore - self.blueprint.clay,
                clay_robots=next_state.clay_robots + 1,
            )
        if self.ore >= self.blueprint.ore and self.ore_robots < max(
            self.blueprint.geode[0], self.blueprint.obsidian[0], self.blueprint.clay
        ):
            yield replace(
                next_state,
                ore=next_state.ore - self.blueprint.ore,
                ore_robots=next_state.ore_robots + 1,
            )

        yield next_state


Data = list[Blueprint]
Return = int


def parse_data(data: str) -> Data:
    pattern = r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
    blueprints = []

    for line in data.splitlines():
        match = re.match(pattern, line)
        if match:
            blueprints.append(
                Blueprint(
                    int(match[1]),
                    int(match[2]),
                    int(match[3]),
                    (int(match[4]), int(match[5])),
                    (int(match[6]), int(match[7])),
                )
            )

    return blueprints


def maximize_geodes(time: int, blueprint: Blueprint) -> int:
    @cache
    def wrapped(state: State) -> int:
        if state.time_left == 0:
            return 0

        return max(
            wrapped(next_state) + state.geode_robots
            for next_state in state.next_states()
        )

    state = State(time, blueprint)
    return wrapped(state)


def part_1(input: str) -> Return:
    blueprints = parse_data(input)

    return sum(
        blueprint.id * maximize_geodes(24, blueprint) for blueprint in blueprints
    )


def part_2(input: str) -> Return:
    blueprints = parse_data(input)

    acc = 1
    for blueprint in blueprints[:3]:
        acc *= maximize_geodes(32, blueprint)

    return acc


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = fp.read()

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
