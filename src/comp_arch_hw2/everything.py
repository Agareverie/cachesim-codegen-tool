import typer

from . import codegen, execute_all, plot
from .cache_category import CacheCategory

app = typer.Typer()


@app.command()
def main(cache_category: CacheCategory, show: bool = False) -> None:
    codegen.main(cache_category)
    execute_all.main(cache_category)
    plot.main(cache_category, show)


if __name__ == "__main__":
    app()
