# pyright: reportUnknownMemberType=false
# pyright: reportUnusedCallResult=false
from collections.abc import Iterator
from typing import TYPE_CHECKING

from . import config, units

if TYPE_CHECKING:
    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure


class AssociativeCacheOperations:
    @staticmethod
    def plot(df: pd.DataFrame, fig: Figure, ax: Axes) -> None:
        associativities: list[int] = sorted(df["associativity"].astype(int).unique())

        for cache_size, group in df.groupby("cache_size_kib"):
            group = group.sort_values("associativity")

            ax.plot(
                group["associativity"],
                group["miss_rate"].astype(float) * 100,
                marker="o",
                label=f"{cache_size} KiB",
            )

        ax.set_xticks(
            associativities,
            labels=[f"{n}-way" for n in associativities],
        )

        ax.set_xlabel("Associativity")
        ax.set_ylabel("Miss Rate (%)")

        # Figure-level legend
        handles, labels = ax.get_legend_handles_labels()

        _ = fig.legend(
            handles,
            labels,
            title="Cache Size",
            loc="outside right center",
            ncols=2,
        )

        ax.grid(True)

    @staticmethod
    def configurations() -> Iterator[config.Codegen]:
        for cache_size in units.iterate_kibibytes(4, 8, 16, 32, 512, 1024):
            for associativity in [2, 4]:
                yield config.Codegen(
                    cache_size=cache_size,
                    block_size=units.Bytes(16),
                    associativity=associativity,
                )
