from collections.abc import Iterator
from typing import TYPE_CHECKING, Protocol

from .associative import AssociativeCacheOperations
from .cache_category import CacheCategory
from .direct_mapped import DirectMappedCacheOperations

if TYPE_CHECKING:
    import pandas as pd
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure

    from . import config


class CacheOperations(Protocol):
    @staticmethod
    def plot(df: pd.DataFrame, fig: Figure, ax: Axes): ...

    @staticmethod
    def configurations() -> Iterator[config.Codegen]: ...


type CacheRegistry = dict[CacheCategory, CacheOperations]

registry: CacheRegistry = {
    CacheCategory.DIRECT_MAPPED: DirectMappedCacheOperations,
    CacheCategory.LEAST_RECENTLY_USED: AssociativeCacheOperations,
    CacheCategory.ROUND_ROBIN: AssociativeCacheOperations,
}
