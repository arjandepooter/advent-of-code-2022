from functools import cmp_to_key

Data = list[str]
Return = int


def parse_data(data: str) -> Data:
    blocks = data.strip().split("\n\n")
    pairs = []
    for block in blocks:
        lines = block.splitlines()
        pairs.append((eval(lines[0]), eval(lines[1])))
    return pairs


def compare_signals(s1, s2):
    if type(s1) == int and type(s2) == int:
        return s1 - s2
    if type(s1) == int:
        return compare_signals([s1], s2)
    if type(s2) == int:
        return compare_signals(s1, [s2])

    for c1, c2 in zip(s1, s2):
        cmp = compare_signals(c1, c2)
        if cmp == 0:
            continue
        return cmp

    return len(s1) - len(s2)


def part_1(input: str) -> Return:
    data = parse_data(input)

    acc = 0
    for i, (p1, p2) in enumerate(data, 1):
        if compare_signals(p1, p2) < 0:
            acc += i

    return acc


def part_2(input: str) -> Return:
    data = [d for line in parse_data(input) for d in line]
    data.extend([[[2]], [[6]]])

    data.sort(key=cmp_to_key(compare_signals))

    return (data.index([[2]]) + 1) * (data.index([[6]]) + 1)


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = fp.read()

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
