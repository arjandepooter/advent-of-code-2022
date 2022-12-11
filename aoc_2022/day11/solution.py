from operator import add, mul
from dataclasses import dataclass
from functools import reduce

Data = list["Monkey"]
Return = int

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

    def catch(self, item: int):
        self.items.append(item)

    def distribute(self, monkeys: list["Monkey"], bore_fn=lambda n: n, modulo=None):
        while len(self.items) > 0:
            item = self.items.pop(0)
            self.inspects += 1

            o1, o2 = self.operands
            o1 = item if o1 is None else o1
            o2 = item if o2 is None else o2
            n = self.operator(o1, o2)
            n = bore_fn(n)

            if modulo:
                n = n % modulo

            target = self.targets[0] if n % self.test == 0 else self.targets[1]

            monkeys[target].catch(n)

    def __repr__(self):
        return f"Monkey {self.id}: {self.items}"


def parse_data(data: str) -> Data:
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


def run(monkeys: list[Monkey], n_rounds: int, bore_fn=lambda n: n, modulo=None) -> int:
    for _ in range(n_rounds):
        for monkey in monkeys:
            monkey.distribute(monkeys, bore_fn=bore_fn, modulo=modulo)

    inspects = sorted([monkey.inspects for monkey in monkeys], reverse=True)

    return inspects[0] * inspects[1]


def part_1(input: str) -> Return:
    monkeys = parse_data(input)

    return run(monkeys, 20, bore_fn=lambda n: n // 3)


def part_2(input: str) -> Return:
    monkeys = parse_data(input)

    modulo = reduce(mul, [monkey.test for monkey in monkeys], 1)

    return run(monkeys, 10_000, modulo=modulo)
