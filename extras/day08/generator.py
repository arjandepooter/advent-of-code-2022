#!/usr/bin/env python3
import random

random.seed = 1337


def generate(rows: int, cols: int):
    for r in range(rows):
        c = random.choices(range(10), range(10, 0, -1), k=cols)
        print("".join(str(n) for n in c))


if __name__ == "__main__":
    import sys

    rows = int(sys.argv[1])
    cols = int(sys.argv[2])

    generate()
