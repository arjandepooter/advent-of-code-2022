Data = list[any]
Return = str


def part_1(data: str) -> Return:
    for n in range(0, len(data)):
        if len(set(data[n : n + 4])) == 4:
            return n + 4


def part_2(data: str) -> Return:
    for n in range(0, len(data)):
        if len(set(data[n : n + 14])) == 14:
            return n + 14
