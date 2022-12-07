Return = int


class Dir:
    name: str
    dirs: list["Dir"]
    files: list[tuple[str, int]]
    parent: "Dir"

    def __init__(self, name: str, parent: "Dir" = None):
        self.name = name
        self.parent = parent
        self.dirs = []
        self.files = []

    def add_file(self, file: str, size: int):
        self.files.append((file, size))

    def add_dir(self, dir: "Dir"):
        self.dirs.append(dir)

    @property
    def size(self) -> int:
        return sum(size for _, size in self.files) + sum(dir.size for dir in self.dirs)

    @property
    def root(self) -> "Dir":
        if self.parent:
            return self.parent.root
        return self

    def __iter__(self):
        yield self
        for d in self.dirs:
            yield from d

    def __repr__(self):
        parent_name = self.parent.name if self.parent else ""
        return f"{parent_name}/{self.name}"


def parse_data(data: str) -> Dir:
    cwd = None

    for line in data.splitlines():
        if line.startswith("$ cd .."):
            cwd = cwd.parent
        elif line.startswith("$ cd"):
            d = Dir(line[5:].strip(), cwd)
            if cwd:
                cwd.add_dir(d)
            cwd = d
        elif line.startswith("$ ls"):
            continue
        elif line.startswith("dir"):
            continue
        else:
            size, name = line.split(" ")
            cwd.add_file(name, int(size))

    return cwd.root


def part_1(input: str) -> Return:
    root = parse_data(input)

    return sum([d.size for d in root if d.size <= 100000])


def part_2(input: str) -> Return:
    root = parse_data(input)

    to_free = 30_000_000 - (70_000_000 - root.size)
    sorted_dirs = sorted(list(root), key=lambda d: d.size, reverse=True)

    return min([d.size for d in sorted_dirs if d.size >= to_free])
