from itertools import cycle

Data = list[tuple[str, int | None]]
Return = int


def parse_data(data: str) -> Data:
    instructions = []

    for line in data.splitlines():
        opcode, *args = line.split()
        args = int(args[0]) if args else None
        instructions.append((opcode, args))

    return instructions


def part_1(input: str) -> Return:
    data = parse_data(input)

    s = [20, 60, 100, 140, 180, 220]
    c = 1
    acc = 0
    reg = 1
    instructions = cycle(data)

    while len(s) > 0:
        opcode, arg = next(instructions)
        arg = arg or 0

        if opcode == "noop":
            c += 1
        if opcode == "addx":
            c += 2

        if c == s[0]:
            reg += arg
            acc += reg * s.pop(0)
        elif c > s[0]:
            acc += reg * s.pop(0)
            reg += arg
        else:
            reg += arg

    return acc


def part_2(input: str):
    data = parse_data(input)

    reg = 1
    c = 0

    values = []
    instructions = cycle(data)

    while c < 240:
        opcode, arg = next(instructions)

        if opcode == "noop":
            values.append(reg)
            c += 1
        if opcode == "addx":
            values.append(reg)
            values.append(reg)
            c += 2
            reg += arg

    for i, value in enumerate(values):
        col = i % 40
        if col == 0:
            print()

        if value - 1 <= col <= value + 1:
            print("#", end="")
        else:
            print(" ", end="")
