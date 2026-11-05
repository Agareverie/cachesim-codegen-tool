from dataclasses import dataclass
from enum import StrEnum
from typing import Literal, cast


@dataclass(frozen=True)
class CacheSimFile:
    filename: Literal["CacheSim", "CacheSimAssociative"]

    @property
    def c(self) -> Literal["CacheSim.c", "CacheSimAssociative.c"]:
        return cast(
            Literal["CacheSim.c", "CacheSimAssociative.c"], f"{self.filename}.c"
        )

    @property
    def h(self) -> Literal["CacheSim.h", "CacheSimAssociative.h"]:
        return cast(
            Literal["CacheSim.h", "CacheSimAssociative.h"], f"{self.filename}.h"
        )


class CacheCategory(StrEnum):
    DIRECT_MAPPED = "direct-mapped"
    LEAST_RECENTLY_USED = "least-recently-used"
    ROUND_ROBIN = "round-robin"

    @property
    def use_round_robin(self) -> Literal["true", "false"]:
        if self == CacheCategory.ROUND_ROBIN:
            return "true"

        return "false"

    @property
    def cachesim(self) -> CacheSimFile:
        if self == CacheCategory.DIRECT_MAPPED:
            return CacheSimFile("CacheSim")

        return CacheSimFile("CacheSimAssociative")
