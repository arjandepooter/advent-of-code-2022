Data = list[list[int]]
Return = int


def parse_data(data: str) -> Data:
    blocks = []
    block = []
    for line in data.splitlines():
        if line:
            block.append(int(line.strip()))
        else:
            blocks.append(block)
            block = []

    return blocks


def part_1(input: str) -> Return:
    data = parse_data(input)

    return max(sum(block) for block in data)


def part_2(input: str) -> Return:
    data = parse_data(input)

    sums = list(reversed(sorted([sum(block) for block in data])))

    return sum(sums[:3])
