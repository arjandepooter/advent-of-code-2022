from dataclasses import dataclass
from operator import add, floordiv as div, mul, sub
from typing import Callable

Data = list[str]
Return = int


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


def binsearch(monkeys: Data, monkey_id: str, goal: int, reverse=False) -> int:
    low = 0
    high = 2**64
    while low <= high:
        mid = (low + high) // 2
        monkeys["humn"] = Monkey("humn", value=mid)
        result = evaluate(monkeys, monkey_id)
        if result == goal:
            return mid
        elif (reverse and result > goal) or (not reverse and result < goal):
            low = mid + 1
        else:
            high = mid - 1

    return binsearch(monkeys, monkey_id, goal, not reverse)


def part_1(input: str) -> Return:
    monkeys = parse_data(input)

    return evaluate(monkeys, "root")


def part_2(input: str) -> Return:
    monkeys = parse_data(input)

    left = monkeys["root"].left
    right = monkeys["root"].right

    l = evaluate(monkeys, left)
    r = evaluate(monkeys, right)

    monkeys["humn"] = Monkey("humn", value=0)
    n = evaluate(monkeys, left)
    monkey_id = right if n == l else left
    goal = l if n == l else r

    return binsearch(monkeys, monkey_id, goal)


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = fp.read()

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
