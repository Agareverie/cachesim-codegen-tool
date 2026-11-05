# pyright: reportUnknownMemberType=false
# pyright: reportUnusedCallResult=false
from collections.abc import Iterator
from typing import TYPE_CHECKING

from . import config, units

if TYPE_CHECKING:
    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure


class DirectMappedCacheOperations:
    @staticmethod
    def plot(df: pd.DataFrame, fig: Figure, ax: Axes) -> None:
        for cache_size, group in df.groupby("cache_size_kib"):
            group = group.sort_values("block_size_bytes")

            ax.plot(
                group["block_size_bytes"],
                group["miss_rate"].astype(float) * 100,
                marker="o",
                label=f"{cache_size} KiB",
            )

        ax.set_xscale("log", base=2)
        ax.set_xticks(sorted(df["block_size_bytes"].astype(int).unique()))

        ax.set_xlabel("Block Size (Bytes)")
        ax.set_ylabel("Miss Rate (%)")

        fig.legend(
            title="Cache Size",
            loc="outside right center",
        )

        ax.grid(True)

    @staticmethod
    def configurations() -> Iterator[config.Codegen]:
        for cache_size in units.iterate_kibibytes(4, 8, 16, 32):
            for block_size in units.iterate_bytes(4, 8, 16, 32):
                yield config.Codegen(
                    cache_size=cache_size, block_size=block_size, associativity=1
                )
