from string import ascii_lowercase, ascii_uppercase

Data = list[str]
Return = int

PRIOS = ascii_lowercase + ascii_uppercase


def parse_data(data: str) -> Data:
    return data.splitlines()


def part_1(input: str) -> Return:
    acc = 0

    for line in parse_data(input):
        mid = len(line) // 2
        p1, p2 = line[:mid], line[mid:]

        for c1 in p1:
            if c1 in p2:
                acc += PRIOS.index(c1) + 1
                break

    return acc


def part_2(input: str) -> Return:
    lines = parse_data(input)
    acc = 0

    for i in range(0, len(lines), 3):
        l1, l2, l3 = lines[i : i + 3]

        for c in l1:
            if c in l2 and c in l3:
                acc += PRIOS.index(c) + 1
                break

    return acc
