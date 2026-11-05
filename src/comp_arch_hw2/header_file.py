import string
from typing import Final, Literal, TypedDict, Unpack, override

from . import units


class Schema(TypedDict):
    cache_size: units.Bytes
    block_size: units.Bytes
    index_size: int
    index_length: int
    offset_length: int
    tag_length: int
    associativity: int
    use_round_robin: Literal["true", "false"]


class TemplateType(string.Template):
    @override
    def substitute(self, **kwargs: Unpack[Schema]) -> str:  # pyright: ignore[reportIncompatibleMethodOverride]
        return super().substitute(**kwargs)

    @override
    def safe_substitute(self, **kwargs: Unpack[Schema]) -> str:  # pyright: ignore[reportIncompatibleMethodOverride]
        return super().safe_substitute(**kwargs)


template: Final[TemplateType] = TemplateType("""
#ifndef CACHESIM_H_INCLUDED
#define CACHESIM_H_INCLUDED
#include <stdbool.h>

/* Please adjust parameters here */
#define INDEXLEN   $index_length
#define OFFSETLEN  $offset_length
#define INDEX_SIZE $index_size
#define BLOCK_SIZE $block_size
#define CACHE_SIZE $cache_size
#define TAGLEN     $tag_length

#define ASSOCIATIVITY $associativity
#define USE_ROUND_ROBIN $use_round_robin

typedef unsigned char Byte;
typedef struct Cache {
    bool valid;
    bool dirty;
    unsigned long tag;
	Byte data[BLOCK_SIZE];
} Cache;

#endif // CACHESIM_H_INCLUDED
""")
