from typing import Any, Tuple

Availability = bool
Size = int
Index = int
Memory = list[Any]
MemSpace = Tuple[Size, Memory]

SIZEOF_BIN = 2

def _bin(mem: Memory, i: Index, available: Availability, size: Size) -> None:
    mem[i] = available
    mem[i + 1] = size

def _available(mem: Memory, i: Index) -> Availability:
    return mem[i]

def _bin_size(mem: Memory, i: Index) -> Size:
    return mem[i + 1]

def _index_of_next(mem: Memory, i: Index) -> Index:
    return i + SIZEOF_BIN + _bin_size(mem, i)

def _set_available(mem: Memory, i: Index, available: Availability) -> None:
    mem[i] = available

def _set_bin_size(mem: Memory, i: Index, size: Size) -> None:
    mem[i + 1] = size
