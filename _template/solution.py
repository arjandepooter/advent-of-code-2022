Data = list[str]
Return = int


def parse_data(data: str) -> Data:
    return [n.strip() for n in data.splitlines()]


def part_1(input: str) -> Return:
    data = parse_data(input)

    raise NotImplementedError


def part_2(input: str) -> Return:
    data = parse_data(input)

    raise NotImplementedError


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = fp.read()

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
