from math import gcd
import re
from typing import Literal

Instruction = int | Literal["L", "R"]


class Board:
    def __init__(self, rows: list[tuple[int, list[bool]]]):
        self.rows = rows

    def next(self, x: int, y: int, direction: tuple[int, int]) -> tuple[int, int]:
        dx, dy = direction
        assert dx == 0 or dy == 0

        if dx != 0:
            offset, row = self.rows[y]
            if x == offset and dx == -1:
                # We're at the start of the row and check if we can wrap around
                if not row[-1]:
                    return offset + len(row) - 1, y
            elif x == offset + len(row) - 1 and dx == 1:
                # We're at the end of the row and check if we can wrap around
                if not row[0]:
                    return offset, y
            else:
                # We're in the middle of the row
                if not row[x - offset + dx]:
                    return x + dx, y
        if dy != 0:
            if dy == -1 and (
                y == 0
                or self.rows[y - 1][0] > x
                or x >= self.rows[y - 1][0] + len(self.rows[y - 1][1])
            ):
                # We're at the top of a column and check if we can wrap around
                ny = y
                while ny < len(self.rows) and self.rows[ny][0] < x < self.rows[ny][
                    0
                ] + len(self.rows[ny][1]):
                    ny += 1
                ny -= 1

                if not self.rows[ny][1][x - self.rows[ny][0]]:
                    return x, ny

            elif dy == 1 and (
                y == len(self.rows) - 1
                or self.rows[y + 1][0] > x
                or x >= self.rows[y + 1][0] + len(self.rows[y + 1][1])
            ):
                # We're at the bottom of a column and check if we can wrap around
                ny = y

                while ny >= 0 and self.rows[ny][0] < x < self.rows[ny][0] + len(
                    self.rows[ny][1]
                ):
                    ny -= 1
                ny += 1

                if not self.rows[ny][1][x - self.rows[ny][0]]:
                    return x, ny
            else:
                # We're in the middle of the column
                if not self.rows[y + dy][1][x - self.rows[y + dy][0]]:
                    return x, y + dy

        return x, y

    def process(
        self, instructions: list[Instruction]
    ) -> tuple[int, int, tuple[int, int]]:
        x, y = self.rows[0][0], 0
        direction = (1, 0)

        for instruction in instructions:
            match instruction:
                case "L":
                    direction = (direction[1], -direction[0])
                case "R":
                    direction = (-direction[1], direction[0])
                case int():
                    for _ in range(instruction):
                        x, y = self.next(x, y, direction)

        return x, y, direction

    def print(self, seen: dict[tuple[int, int], tuple[int, int]]):
        for y, (offset, row) in enumerate(self.rows):
            for x in range(offset):
                print(" ", end="")
            for x, tile in enumerate(row):
                if (x + offset, y) in seen:
                    match seen[(x + offset, y)]:
                        case (1, 0):
                            print(">", end="")
                        case (0, 1):
                            print("v", end="")
                        case (-1, 0):
                            print("<", end="")
                        case (0, -1):
                            print("^", end="")
                if tile:
                    print("#", end="")
                else:
                    print(".", end="")
            print()


Data = tuple[Board, list[Instruction]]
Return = int

SCORE = {
    (1, 0): 0,
    (0, 1): 1,
    (-1, 0): 2,
    (0, -1): 3,
}


def parse_data(data: str) -> Data:
    blocks = data.split("\n\n")

    rows = []
    for line in blocks[0].splitlines():
        l = len(line)
        tiles = [c == "#" for c in line.strip()]
        rows.append((int(l - len(tiles)), tiles))

    board = Board(rows)

    instructions = [
        c if c in ("L", "R") else int(c)
        for c in re.findall(r"(\d+|L|R)", blocks[1].strip())
    ]

    return board, instructions


def calc_score(x, y, direction):
    return 1000 * (y + 1) + 4 * (x + 1) + SCORE[direction]


def part_1(input: str) -> Return:
    board, instructions = parse_data(input)

    x, y, direction = board.process(instructions)

    return calc_score(x, y, direction)


def part_2(input: str) -> Return:
    board, instructions = parse_data(input)

    faces = {}

    line_lengths = [len(row) for _, row in board.rows]
    size = gcd(*line_lengths)

    for i in range(0, len(board.rows), size):
        offset, row = board.rows[i]
        for j in range(0, len(row), size):
            face = []
            for k in range(size):
                face.append(board.rows[i + k][1][j : j + size])
            faces[((offset + j) // size, i // size)] = face

    # freaking hardcoded
    edges = {
        (1, 0): [("A", "B"), ("B", "D"), ("C", "D"), ("A", "C")],
        (2, 0): [("B", "H"), ("H", "F"), ("D", "F"), ("B", "D")],
        (1, 1): [("C", "D"), ("D", "F"), ("E", "F"), ("C", "E")],
        (1, 2): [("E", "F"), ("F", "H"), ("G", "H"), ("E", "G")],
        (0, 2): [("C", "E"), ("E", "G"), ("A", "G"), ("C", "A")],
        (0, 3): [("A", "G"), ("G", "H"), ("B", "H"), ("A", "B")],
    }
    # edges = {
    #     (2, 0): [("A", "B"), ("B", "D"), ("C", "D"), ("A", "C")],
    #     (2, 1): [("C", "D"), ("D", "F"), ("E", "F"), ("C", "E")],
    #     (1, 1): [("A", "C"), ("C", "E"), ("G", "E"), ("A", "G")],
    #     (0, 1): [("B", "A"), ("A", "G"), ("H", "G"), ("B", "H")],
    #     (2, 2): [("E", "F"), ("F", "H"), ("G", "H"), ("E", "G")],
    #     (3, 2): [("F", "D"), ("D", "B"), ("H", "B"), ("F", "H")],
    # }

    current_face = (2, 0)
    current_position = (0, 0)
    direction = (1, 0)

    for instruction in instructions:
        match instruction:
            case "L":
                direction = (direction[1], -direction[0])
            case "R":
                direction = (-direction[1], direction[0])
            case int():
                for _ in range(instruction):
                    x, y = current_position
                    dx, dy = direction
                    if x + dx >= size or x + dx < 0 or y + dy >= size or y + dy < 0:
                        idx = {
                            (0, -1): 0,
                            (1, 0): 1,
                            (0, 1): 2,
                            (-1, 0): 3,
                        }[direction]
                        a, b = edges[current_face][idx]

                        for face, edge_list in edges.items():
                            if face == current_face:
                                continue
                            if (a, b) in edge_list:
                                edge_idx = edge_list.index((a, b))
                                offset = y if dy == 0 else x
                            elif (b, a) in edge_list:
                                edge_idx = edge_list.index((b, a))
                                offset = size - (y if dy == 0 else x) - 1
                            else:
                                continue
                            if edge_idx == 0:
                                next_position = (offset, 0)
                                next_direction = (0, 1)
                            elif edge_idx == 1:
                                next_position = (size - 1, offset)
                                next_direction = (-1, 0)
                            elif edge_idx == 2:
                                next_position = (offset, size - 1)
                                next_direction = (0, -1)
                            elif edge_idx == 3:
                                next_position = (0, offset)
                                next_direction = (1, 0)

                            if not faces[face][next_position[1]][next_position[0]]:
                                current_face = face
                                current_position = next_position
                                direction = next_direction
                            break

                    else:
                        if not faces[current_face][y + dy][x + dx]:
                            current_position = (x + dx, y + dy)

    x, y = current_position
    edge_x, edge_y = current_face
    x += edge_x * size
    y += edge_y * size
    return calc_score(x, y, direction)


if __name__ == "__main__":
    import sys

    fp = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    data = fp.read()

    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
