from typing import Iterator

Data = list[tuple[str, int | None]]
Return = int


def parse_data(data: str) -> Data:
    return [
        ((p := line.split(" "))[0], int(p[1]) if len(p) > 1 else None)
        for line in data.splitlines()
    ]


def iter_cycle(data: Data) -> Iterator[int]:
    reg = 1

    for opcode, arg in data:
        yield reg
        if opcode == "addx":
            yield reg
            reg += arg


def part_1(input: str) -> Return:
    values = list(iter_cycle(parse_data(input)))

    return sum(values[i - 1] * i for i in range(20, len(values), 40))


def part_2(input: str):
    data = parse_data(input)

    for i, value in enumerate(iter_cycle(data)):
        col = i % 40

        if col == 0:
            print()

        print("█" if value - 1 <= col <= value + 1 else " ", end="")
