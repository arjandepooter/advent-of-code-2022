from itertools import permutations

Data = list[tuple[str, str]]
Return = int


def parse_data(data: str) -> Data:
    return [n.strip().split(" ") for n in data.splitlines()]


def calculate_score(a: str, b: str) -> int:
    score = 1 + ["A", "B", "C"].index(b)

    if a == b:
        score += 3

    if (a, b) in (("A", "B"), ("B", "C"), ("C", "A")):
        score += 6

    return score


def part_1(input: str) -> Return:
    mapping = {
        "X": "A",
        "Y": "B",
        "Z": "C",
    }

    return sum(calculate_score(a, mapping[b]) for a, b in parse_data(input))


def part_2(input: str) -> Return:
    mapping = {
        ("A", "X"): "C",
        ("A", "Y"): "A",
        ("A", "Z"): "B",
        ("B", "X"): "A",
        ("B", "Y"): "B",
        ("B", "Z"): "C",
        ("C", "X"): "B",
        ("C", "Y"): "C",
        ("C", "Z"): "A",
    }

    return sum(calculate_score(a, mapping[(a, b)]) for a, b in parse_data(input))
