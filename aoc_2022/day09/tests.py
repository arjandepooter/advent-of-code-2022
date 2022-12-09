import pytest
from .solution import part_1, part_2

# Tuple with sample data, part 1 result, part 2 result. Set result to None to skip
SAMPLES = [
    (
        """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""",
        13,
        1,
    ),
    (
        """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""",
        None,
        36,
    ),
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
