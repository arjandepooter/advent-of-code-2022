from operator import add, mul
from dataclasses import dataclass
from functools import reduce


OPS = {"+": add, "*": mul}


@dataclass
class Monkey:
    id: int
    items: list[int]
    operator: callable
    operands: tuple[int | None, int | None]
    test: int
    targets: tuple[int, int]
    inspects = 0

    def __repr__(self):
        return f"Monkey {self.id}: {self.items}"


def parse_data(data: str) -> list[Monkey]:
    monkeys = []
    blocks = data.split("\n\n")

    for block in blocks:
        lines = block.splitlines()

        if len(lines) < 6:
            continue

        id = int(lines[0].split()[1][:-1])
        items = [int(i) for i in lines[1].split(": ")[1].split(", ")]
        test = int(lines[3].split(": ")[1].split()[2])
        ops = lines[2].split("= ")[-1].split(" ")
        operator = OPS[ops[1]]
        operands = [
            int(ops[0]) if ops[0] != "old" else None,
            int(ops[2]) if ops[2] != "old" else None,
        ]
        targets = (
            int(lines[4].split(": ")[1].split()[3]),
            int(lines[5].split(": ")[1].split()[3]),
        )

        monkeys.append(Monkey(id, items, operator, operands, test, targets))

    return monkeys


def step(monkeys: list[Monkey], item: tuple[int, int], m: int) -> tuple[int, int]:
    idx, value = item
    monkey = monkeys[idx]

    o1, o2 = monkey.operands
    o1 = value if o1 is None else o1
    o2 = value if o2 is None else o2
    value = monkey.operator(o1, o2) % m
    idx = monkey.targets[0] if value % monkey.test == 0 else monkey.targets[1]

    return idx, value


def run(monkeys: list[Monkey], n_rounds: int):
    items = [(m.id, item) for m in monkeys for item in m.items]
    m = reduce(mul, [m.test for m in monkeys], 1)

    total_visits = [0] * len(monkeys)

    for idx, value in items:
        start, period = calc_period(monkeys, idx, value)
        r = 0

        while (idx, value) != start and r < n_rounds:
            total_visits[idx] += 1
            nxt, value = step(monkeys, (idx, value), m)

            if nxt < idx:
                r += 1

            idx = nxt

        n = (n_rounds - r) // period
        visits = calc_period_visits(monkeys, start)
        total_visits = [t + n * v for t, v in zip(total_visits, visits)]
        r += n * period

        while r < n_rounds:
            total_visits[idx] += 1
            nxt, value = step(monkeys, (idx, value), m)
            if nxt < idx:
                r += 1
            idx = nxt

    total_visits.sort(reverse=True)

    return total_visits[0] * total_visits[1]


def calc_period(monkeys: list[Monkey], idx: int, value: int):
    m = reduce(mul, [m.test for m in monkeys], 1)

    r = 0
    states = {}

    while (idx, value) not in states:
        states[(idx, value)] = r
        nxt, value = step(monkeys, (idx, value), m)

        if nxt < idx:
            r += 1
        idx = nxt

    return (idx, value), r - states[(idx, value)]


def calc_period_visits(monkeys: list[Monkey], start: tuple[int, int]):
    m = reduce(mul, [m.test for m in monkeys], 1)

    idx, value = start
    visits = [0] * len(monkeys)
    states = set()

    while (idx, value) not in states:
        states.add((idx, value))
        visits[idx] += 1
        idx, value = step(monkeys, (idx, value), m)

    return visits


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    monkeys = parse_data(fp.read())

    for n in range(4, 10):
        print(f"n = {10**n}: {run(monkeys, 10**n)}")
