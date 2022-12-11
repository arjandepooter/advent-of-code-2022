import pytest
from .solution import part_1, part_2

# Tuple with sample data, part 1 result, part 2 result. Set result to None to skip
SAMPLES = [
    (
        """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1""",
        10605,
        2713310158,
    )
]


@pytest.mark.parametrize(
    "input,expected",
    [(input, expected) for input, expected, _ in SAMPLES],
)
def test_sample_part_1(input, expected):
    if expected is None:
        return pytest.skip("Part 1 not implemented")

    assert part_1(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    [(input, expected) for input, _, expected in SAMPLES],
)
def test_sample_part_2(input, expected):
    if expected is None:
        return pytest.skip("Part 2 not implemented")

    assert part_2(input) == expected
