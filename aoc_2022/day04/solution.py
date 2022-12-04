Data = list[tuple[tuple[int, int], tuple[int, int]]]
Return = int


def parse_data(data: str) -> Data:
    return [
        tuple(tuple(int(x) for x in y.split("-")) for y in line.split(","))
        for line in data.splitlines()
    ]


def contains(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] <= b[0] <= b[1] <= a[1] or b[0] <= a[0] <= a[1] <= b[1]


def has_overlap(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] <= b[0] <= a[1] or b[0] <= a[0] <= b[1]


def part_1(input: str) -> Return:
    data = parse_data(input)
    acc = 0

    for a, b in data:
        if contains(a, b):
            acc += 1

    return acc


def part_2(input: str) -> Return:
    data = parse_data(input)
    acc = 0

    for a, b in data:
        if has_overlap(a, b):
            acc += 1

    return acc
