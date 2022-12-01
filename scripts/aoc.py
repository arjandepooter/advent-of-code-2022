import logging
import shutil
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from time import time_ns
from typing import TextIO

import click
import pytest
import requests
from lxml import html
from rich.console import Console
from rich.logging import RichHandler
from rich.prompt import Confirm

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)

console = Console()
work_dir = Path(__file__).parent.parent
aoc_session = requests.Session(
    headers={
        "User-Agent": "github.com/arjandepooter/advent-of-code-2022 by mail@arjandepooter.nl",
    }
)


def submit_solution(day: int, part: int, answer: str) -> None:
    """Submit answer to Advent of Code."""
    with aoc_session.post(
        "https://adventofcode.com/2022/day/{day}/answer".format(day=day),
        data={"level": part, "answer": answer},
    ) as response:
        if response.status_code == 200:
            if "That's the right answer!" in response.text:
                console.log("Answer submitted successfully", style="green")
            else:
                text = html.fromstring(response.text).find(".//main").text_content()
                console.log("Answer not accepted:", text, style="red")
        else:
            console.log(
                f"Failed to submit answer for day {day} part {part}, got status {response.status_code}",
                style="red",
            )


def run_solution(func: callable, input: str) -> str | None:
    """Run solution function and return result."""

    try:
        with console.status(f"Running {func.__name__}..."):
            start = time_ns()
            result = func(input)
            duration = time_ns() - start
        console.log(
            f"Result for {func.__name__} calculated in {duration/10e6:.2f} ms: [bold green]{result}"
        )
        return str(result)
    except NotImplementedError:
        console.log("Part 2 not implemented", style="red")
    except Exception as e:
        console.log(f"Part 2 failed: {e}", style="red")


@click.group()
@click.option("--session_token", envvar="AOC_SESSION_TOKEN")
def cli(session_token):
    aoc_session.cookies.set("session", session_token)


@click.command()
@click.argument("day", type=click.IntRange(1, 25), required=True)
def download(day: int):
    inputs_dir = work_dir / "inputs"
    if not inputs_dir.exists():
        inputs_dir.mkdir()
        console.log("Created inputs directory")

    input_file = inputs_dir / f"day{day}.txt"

    if input_file.exists():
        if not Confirm.ask(f"Input for day {day} already exists. Overwrite?"):
            console.log("Aborted", style="red")
            return

    with aoc_session.get(
        f"https://adventofcode.com/2022/day/{day}/input"
    ) as r, console.status(f"Downloading input file for day {day}") as status:
        status.console.log(f"Status code: {r.status_code}")
        if r.status_code == 200:
            input_file.write_text(r.text)
            console.log(f"Input for day {day} saved in {input_file}", style="green")
        else:
            console.log(f"Request failed with {r.status_code}", style="red")


@click.command()
@click.argument("day", type=click.IntRange(1, 25), required=True)
def create(day: int):
    solution_dir = work_dir / "aoc_2022" / f"day{day:02}"

    if solution_dir.exists():
        console.log(f"Solution for day {day} already exists", style="red")
        return

    solution_dir.mkdir()
    for file in (work_dir / "_template").glob("*"):
        shutil.copy(file, solution_dir / file.name)
        console.log(f"Copied {file.name}")

    console.log(
        f"Created solution directory for day {day} at {solution_dir}", style="green"
    )


@click.command()
@click.argument("day", type=click.IntRange(1, 25), required=True)
@click.argument("input_file", type=click.File(), required=False)
@click.option("--part", type=click.IntRange(1, 2))
@click.option("--submit", is_flag=True)
def run(day: int, input_file: TextIO | None, part: int | None, submit: bool = False):
    solution_dir = work_dir / "aoc_2022" / f"day{day:02}"
    if not solution_dir.exists():
        console.log(f"Solution for day {day} does not exist", style="red")
        return

    console.log(f"Running tests for day {day}")

    test_output = StringIO()
    with console.status("Running tests..."), redirect_stdout(test_output):
        pytest.main(["-q", solution_dir / "tests.py"])
    console.log(test_output.getvalue(), highlight=False)

    if input_file is None:
        input_file = (work_dir / "inputs" / f"day{day}.txt").open()

    input_data = input_file.read()
    solution = __import__(
        f"aoc_2022.day{day:02}.solution", fromlist=["part_1", "part_2"]
    )

    if part is None or part == 1:
        result = run_solution(solution.part_1, input_data)
    if part is None or part == 2:
        result = run_solution(solution.part_2, input_data)

    if submit and part is not None and result is not None:
        submit_solution(day, part, result)


cli.add_command(download)
cli.add_command(create)
cli.add_command(run)


if __name__ == "__main__":
    cli()
