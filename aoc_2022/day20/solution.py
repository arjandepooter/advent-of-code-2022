from collections import deque
from itertools import chain, repeat

Data = list[int]
Return = int


def parse_data(data: str) -> Data:
    return [int(n.strip()) for n in data.splitlines()]


def mix(ct: list[int], n=1) -> list[int]:
    q = deque((i, v) for i, v in enumerate(ct))

    for _ in range(n):
        for i, v in enumerate(ct):
            d = q.index((i, v))
            q.rotate(-d)
            q.popleft()
            q.rotate(-v)
            q.appendleft((i, v))

    return [v for _, v in q]


def align(ct: list[int]) -> list[int]:
    q = deque(ct)
    while q[0] != 0:
        q.rotate(1)
    return list(q)


def get_result(ct: list[int]) -> int:
    acc = 0
    for i in (1000, 2000, 3000):
        acc += ct[i % len(ct)]
    return acc


def part_1(input: str) -> Return:
    data = parse_data(input)

    return get_result(align(mix(data)))


def part_2(input: str) -> Return:
    key = 811589153
    data = [n * key for n in parse_data(input)]

    return get_result(align(mix(data, 10)))


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = fp.read()

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
