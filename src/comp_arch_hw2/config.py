from dataclasses import dataclass

from . import header_file, units
from .cache_category import CacheCategory


@dataclass(kw_only=True, frozen=True)
class Codegen:
    cache_size: units.Kibibytes
    block_size: units.Bytes
    associativity: int

    def bitwise_log2(self, value: int) -> int:
        if value <= 0 or value & (value - 1):
            raise ValueError(f"{value} must be a positive power of two")

        return value.bit_length() - 1

    def derive_values(self, cache_category: CacheCategory) -> header_file.Schema:
        offset_length = self.bitwise_log2(int(self.block_size))
        index_size = self.cache_size.as_bytes // (self.block_size * self.associativity)
        index_length = self.bitwise_log2(index_size)
        tag_length = 32 - index_length - offset_length

        return {
            "cache_size": self.cache_size.as_bytes,
            "block_size": self.block_size,
            "index_size": index_size,
            "index_length": index_length,
            "offset_length": offset_length,
            "tag_length": tag_length,
            "associativity": self.associativity,
            "use_round_robin": cache_category.use_round_robin,
        }

    def executable_filename(self, cache_category: CacheCategory) -> str:
        match cache_category:
            case CacheCategory.DIRECT_MAPPED:
                return f"cache-{self.cache_size.as_kibibytes:02d}KiB-block-{self.block_size:02d}B.out"

            case CacheCategory.LEAST_RECENTLY_USED | CacheCategory.ROUND_ROBIN:
                return f"{self.associativity}-way-cache-{self.cache_size.as_kibibytes:04d}KiB.out"
