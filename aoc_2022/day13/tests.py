import pytest
from .solution import part_1, part_2

# Tuple with sample data, part 1 result, part 2 result. Set result to None to skip
SAMPLES = [
    (
        """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]""",
        13,
        140,
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
