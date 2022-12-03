#!/usr/bin/env python3
import random
import sys
from string import ascii_letters

random.seed(1337)

NUMBER_OF_SETS = 100
LIMITS = [100_000, 500_000]


def generate():
    part_1 = 0
    part_2 = 0

    for n in range(NUMBER_OF_SETS):
        chars = list(ascii_letters)
        random.shuffle(chars)
        common = chars.pop()

        for i in range(3):
            char_set = chars[i * 17 : i * 17 + 17]
            char_set_common = char_set.pop()
            k = random.randint(*LIMITS)
            parts = [
                random.choices(char_set[:8], k=k) + [char_set_common],
                random.choices(char_set[8:], k=k - 1) + [char_set_common, common],
            ]
            random.shuffle(parts[0])
            random.shuffle(parts[1])
            random.shuffle(parts)
            part_1 += ascii_letters.index(char_set_common) + 1
            print("".join(parts[0] + parts[1]))

        part_2 += ascii_letters.index(common) + 1

    print(f"Expected part 1: {part_1}", file=sys.stderr)
    print(f"Expected part 2: {part_2}", file=sys.stderr)


if __name__ == "__main__":
    generate()
