from dataclasses import dataclass, replace
from operator import add, floordiv as div, mul, sub
from typing import Callable


@dataclass
class Monkey:
    id: str
    value: int | None = None
    left: str | None = None
    right: str | None = None
    op: Callable | None = None

    def __eq__(self, other: object) -> bool:
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


class X:
    def __init__(self, stack=None):
        self.stack = stack or []

    def push(self, item):
        return X(self.stack + [item])

    def evaluate(self, value) -> int:
        for op in self.stack[::-1]:
            value = op(value)
        return value

    def __eq__(self, other) -> int:
        return self.evaluate(other)

    def __add__(self, other):
        return self.push(lambda x: x - other)

    def __radd__(self, other):
        return self.push(lambda x: x - other)

    def __sub__(self, other):
        return self.push(lambda x: x + other)

    def __rsub__(self, other):
        return self.push(lambda x: other - x)

    def __mul__(self, other):
        return self.push(lambda x: x // other)

    def __rmul__(self, other):
        return self.push(lambda x: x // other)

    def __floordiv__(self, other):
        return self.push(lambda x: x * other)

    def __rfloordiv__(self, other):
        return self.push(lambda x: other // x)

    def __str__(self):
        return f"X({len(self.stack)})"


Data = dict[str, Monkey]
Return = int


def parse_data(data: str) -> Data:
    monkeys = {}

    for line in data.splitlines():
        id, value = line.split(": ")
        if value.isnumeric():
            monkeys[id] = Monkey(id, value=int(value))
        else:
            left, op, right = value.split(" ")
            op = {"+": add, "-": sub, "*": mul, "/": div}[op]
            monkeys[id] = Monkey(id, left=left, right=right, op=op)

    return monkeys


def evaluate(monkeys: Data, monkey_id: str) -> int:
    monkey = monkeys[monkey_id]
    if monkey.value is not None:
        return monkey.value

    return monkey.op(
        evaluate(monkeys, monkey.left),
        evaluate(monkeys, monkey.right),
    )


def part_1(input: str) -> Return:
    monkeys = parse_data(input)

    return evaluate(monkeys, "root")


def part_2(input: str) -> Return:
    monkeys = parse_data(input)

    monkeys["root"] = replace(monkeys["root"], op=lambda x, y: x == y)
    monkeys["humn"] = replace(monkeys["humn"], value=X())

    return evaluate(monkeys, "root")


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = fp.read()

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
