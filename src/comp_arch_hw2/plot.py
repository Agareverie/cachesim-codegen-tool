# pyright: reportUnknownMemberType=false
# pyright: reportUnusedCallResult=false

import matplotlib.pyplot as plt
import pandas as pd
import typer
from rich import print

from . import cache_types, directory
from .cache_category import CacheCategory

plt.style.use("seaborn-v0_8-whitegrid")
app = typer.Typer()


@app.command()
def main(cache_category: CacheCategory, show: bool = False):
    print(f"Plotting miss rate of a {cache_category} cache...")
    df = pd.read_csv(directory.data / f"{cache_category}.csv")

    fig, ax = plt.subplots(constrained_layout=True)
    cache_types.registry[cache_category].plot(df, fig, ax)
    ax.set_title(f"Miss rates of a {cache_category} cache")

    output_path = directory.plots / f"{cache_category}.png"
    fig.savefig(output_path, dpi=300)
    print(f"Saved figure at {output_path}.")

    if show:
        plt.show()
        plt.close(fig)


if __name__ == "__main__":
    app()
