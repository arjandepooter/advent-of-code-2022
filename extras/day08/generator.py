#!/usr/bin/env python3
import random

random.seed = 1337


def generate():
    for r in range(2000):
        c = random.choices(range(10), range(10, 0, -1), k=2000)
        print("".join(str(n) for n in c))


if __name__ == "__main__":
    generate()
