import csv
import re
import subprocess
from typing import Literal, TypedDict

import typer
from rich import print

from . import directory, patterns
from .cache_category import CacheCategory

app = typer.Typer()


class DataSchema(TypedDict):
    cache_size_kib: int
    block_size_bytes: int
    associativity: int
    hits: int
    misses: int
    hit_rate: float
    miss_rate: float


@app.command()
def main(
    cache_category: CacheCategory,
    trace: Literal["gcc_ld_trace.txt", "go_ld_trace.txt"] = "gcc_ld_trace.txt",
) -> None:
    input_path_dir = (directory.root / "build" / cache_category).resolve()

    if not input_path_dir.is_dir():
        print(f"Not a directory: {input_path_dir}")
        return

    executables = sorted(
        path
        for path in input_path_dir.iterdir()
        if path.is_file() and path.stat().st_mode & 0o111
    )

    output_result: list[DataSchema] = []
    print(f"Executing binaries in {directory.build / cache_category}...")
    for executable in executables:
        print(f"Running ./build/{executable.relative_to(directory.build)}...")

        result = subprocess.run(
            [str(executable), str(directory.root / trace)],
            check=False,
            capture_output=True,
            text=True,
        )

        regex_match = re.search(patterns.expected_stdout, result.stdout)

        if regex_match:
            data = regex_match.groupdict()
            output_result.append(
                {
                    "cache_size_kib": int(data["cache_kib"]),
                    "block_size_bytes": int(data["block_bytes"]),
                    "associativity": int(data["associativity"]),
                    "hits": int(data["hits"]),
                    "misses": int(data["misses"]),
                    "hit_rate": float(data["hit_rate"]),
                    "miss_rate": 1 - float(data["hit_rate"]),
                }
            )

    output_path = directory.data / f"{cache_category}.csv"
    with open(output_path, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=DataSchema.__annotations__.keys(),
        )

        writer.writeheader()
        print(f"Saved results into {output_path}.")
        writer.writerows(output_result)


if __name__ == "__main__":
    app()
