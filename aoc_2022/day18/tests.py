import pytest
from .solution import part_1, part_2

# Tuple with sample data, part 1 result, part 2 result. Set result to None to skip
SAMPLES = [
    (
        """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""",
        64,
        58,
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
