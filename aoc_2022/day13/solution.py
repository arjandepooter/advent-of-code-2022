from functools import cmp_to_key, reduce

Signal = list["Signal"] | int
Return = int


def parse_signal(signal: str) -> tuple[Signal, int]:
    c = signal[0]
    if c.isdigit():
        for i in range(1, len(signal)):
            if not signal[i].isdigit():
                return int(signal[:i]), i
    if c == "[":
        acc = []
        i = 1
        while signal[i] != "]":
            if signal[i] == ",":
                i += 1
                continue
            s, t = parse_signal(signal[i:])
            acc.append(s)
            i += t
        return acc, i + 1


def parse_data(data: str) -> list[tuple[Signal, Signal]]:
    blocks = data.strip().split("\n\n")
    pairs = []
    for block in blocks:
        signals = [parse_signal(line)[0] for line in block.splitlines()[:2]]
        pairs.append(tuple(signals))
    return pairs


def compare_signals(s1, s2):
    match s1, s2:
        case int(), int():
            return s1 - s2
        case int(), _:
            return compare_signals([s1], s2)
        case _, int():
            return compare_signals(s1, [s2])
        case list(), list():
            for c1, c2 in zip(s1, s2):
                if (cmp := compare_signals(c1, c2)) != 0:
                    return cmp
            return len(s1) - len(s2)


def part_1(input: str) -> Return:
    data = parse_data(input)

    return sum(i for i, (p1, p2) in enumerate(data, 1) if compare_signals(p1, p2) < 0)


def part_2(input: str) -> Return:
    data = [d for line in parse_data(input) for d in line]
    dividers = [[[2]], [[6]]]

    data.extend(dividers)
    data.sort(key=cmp_to_key(compare_signals))

    return reduce(
        lambda a, b: a * b, (i for i, d in enumerate(data, 1) if d in dividers)
    )


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = fp.read()

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
