from collections.abc import Iterable
from dataclasses import dataclass
from typing import NewType


@dataclass
class Kibibytes:
    """
    Bytes type wrapper for Kibibytes that convert back to Bytes
    """

    as_kibibytes: int

    @property
    def as_bytes(self) -> Bytes:
        return Bytes(1024 * self.as_kibibytes)


Bytes = NewType(
    "Bytes", int
)  # bytes is built-in, so UnitBytes is named like this to keep them separate


def iterate_bytes(*ints: int) -> Iterable[Bytes]:
    return map(Bytes, ints)


def iterate_kibibytes(*ints: int) -> Iterable[Kibibytes]:
    return map(Kibibytes, ints)
