Data = list[any]
Return = str


def parse_data(data: str) -> Data:
    """Input format:
                [M]     [W] [M]
                [L] [Q] [S] [C] [R]
                [Q] [F] [F] [T] [N] [S]
        [N]     [V] [V] [H] [L] [J] [D]
        [D] [D] [W] [P] [G] [R] [D] [F]
    [T] [T] [M] [G] [G] [Q] [N] [W] [L]
    [Z] [H] [F] [J] [D] [Z] [S] [H] [Q]
    [B] [V] [B] [T] [W] [V] [Z] [Z] [M]
     1   2   3   4   5   6   7   8   9
    """
    # parse stacks
    lines = data.splitlines()
    l = (len(lines[0]) + 1) // 4

    stacks = []
    for i in range(l):
        stacks.append([])

    it = iter(lines)

    while "1" not in (line := next(it)):
        for i in range(0, len(line), 4):
            c = line[i + 1]
            if c != " ":
                stacks[i // 4].insert(0, c)

    # skip empty line
    next(it)

    # parse moves: move 1 from 9 to 4
    moves = []
    for line in it:
        parts = line.split(" ")
        w = int(parts[1])
        f = int(parts[3])
        t = int(parts[5])

        moves.append((w, f, t))

    return stacks, moves


def part_1(input: str) -> Return:
    stacks, moves = parse_data(input)

    for w, f, t in moves:
        items = stacks[f - 1][-w:][::-1]
        stacks[f - 1] = stacks[f - 1][:-w]
        stacks[t - 1] += items

    return "".join(stack[-1] for stack in stacks)


def part_2(input: str) -> Return:
    stacks, moves = parse_data(input)

    for w, f, t in moves:
        items = stacks[f - 1][-w:]
        stacks[f - 1] = stacks[f - 1][:-w]
        stacks[t - 1] += items

    return "".join(stack[-1] for stack in stacks)
