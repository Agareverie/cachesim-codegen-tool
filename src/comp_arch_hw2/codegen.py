import shutil
import subprocess
import tempfile
from pathlib import Path

import typer
from rich import print

from . import cache_types, config, directory, header_file
from .cache_category import CacheCategory


def compile(cache_category: CacheCategory, codegen_config: config.Codegen) -> Path:
    values = codegen_config.derive_values(cache_category)
    executable_filename = codegen_config.executable_filename(cache_category)

    output_dir = directory.build / cache_category
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / executable_filename

    with tempfile.TemporaryDirectory() as tmp:
        staging_dir = Path(tmp)

        # Stage the original source tree.
        _ = shutil.copytree(
            directory.c_source,
            staging_dir,
            dirs_exist_ok=True,
        )

        # Replace the header only in the staging directory.
        generated_header = header_file.template.substitute(**values)

        _ = (staging_dir / cache_category.cachesim.h).write_text(
            generated_header,
            encoding="utf-8",
        )

        # Compile the staged source against the generated header.
        _ = subprocess.run(
            [
                "cc",
                "-std=c11",
                "-O2",
                "-Wall",
                "-Wextra",
                str(staging_dir / cache_category.cachesim.c),
                "-o",
                str(output_path.resolve()),
            ],
            cwd=staging_dir,
            check=True,
        )

    return output_path


app = typer.Typer()


@app.command()
def main(cache_category: CacheCategory) -> None:
    print(f"Generating compilations for a {cache_category} cache...")

    for configuration in cache_types.registry[cache_category].configurations():
        output_path = compile(cache_category, configuration)
        print(f"Compiled ./{output_path.relative_to(directory.root)}.")


if __name__ == "__main__":
    app()
