from math import ceil, log

Data = list[str]
Return = str


def from_snafu(s: str) -> int:
    acc = 0
    for i, c in enumerate(reversed(s)):
        match c:
            case "-":
                m = -1
            case "=":
                m = -2
            case _:
                m = int(c)
        acc += m * 5**i

    return acc


def to_snafu(n: int) -> str:
    if n == 0:
        return "0"

    acc = []

    n_digits = ceil(log(abs(n), 5))
    if abs(n) <= 5**n_digits // 2:
        n_digits -= 1

    for l in range(n_digits, -1, -1):
        m = abs(n) // 5**l * (-1 if n < 0 else 1)
        n -= m * 5**l
        if abs(n) > 5**l // 2:
            m += 1 if n > 0 else -1
            n -= 5**l if n > 0 else -(5**l)

        match m:
            case -2:
                c = "="
            case -1:
                c = "-"
            case _:
                c = str(m)

        acc.append(c)

    return "".join(acc)


def parse_data(data: str) -> Data:
    return [n.strip() for n in data.splitlines()]


def part_1(input: str) -> Return:
    data = parse_data(input)

    total = sum(from_snafu(n) for n in data)

    return to_snafu(total)


def part_2(input: str) -> Return:
    return "50 STARS"


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = fp.read()

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
