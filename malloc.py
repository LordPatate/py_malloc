"""
OOP-free malloc emulation, using only lists and tuples.
Could be used to explain memory management.
"""
from bins import *


def init_memspace(size: Size) -> MemSpace:
    memory = []
    for _ in range(SIZEOF_BIN + size):
        memory.append(None)
    _bin(memory, 0, available=True, size=size - SIZEOF_BIN)
    return (size, memory)


def _malloc(memspace: MemSpace, requested_size: Size, defragmented: bool) -> Tuple[Ptr, MemSpace]:
    mem_size, memory = memspace
    i = 0
    while i + SIZEOF_BIN + requested_size < mem_size and not (_available(memory, i) and _bin_size(memory, i) >= requested_size):
        i = _index_of_next(memory, i)
    if i + SIZEOF_BIN + requested_size < mem_size:
        extra_size = _bin_size(memory, i) - requested_size
        if extra_size > SIZEOF_BIN:
            index_of_next = i + SIZEOF_BIN + requested_size
            _bin(memory, index_of_next, available=True, size=extra_size - SIZEOF_BIN)
            _set_bin_size(memory, i, requested_size)
        _set_available(memory, i, False)
        memspace = (memsize, memory)
        return i + SIZEOF_BIN, memspace
    else:
        if not defragmented:
            memspace = defragment(memspace)
            mem_size, memory = memspace
            return _malloc(memspace, requested_size, defragmented=True)
        else:
            raise RuntimeError("Not enough available memory")

def malloc(memspace: MemSpace, requested_size: Size) -> Tuple[Ptr, MemSpace]:
    return _malloc(namespace, requested_size, defragmented=False)


def free(memspace: MemSpace, ptr: Ptr) -> MemSpace:
    mem_size, memory = memspace
    i = ptr - SIZEOF_BIN
    if 0 <= i and i < mem_size:
        _set_available(memory, i, True)
    memspace = (memsize, memory)
    return memspace


def _defrag_from(memspace: MemSpace, i: Index) -> MemSpace:
    mem_size, memory = memspace
    if i < mem_size:
        memspace = _defrag_from(memspace, _index_of_next(memory, i))
        mem_size, memory = memspace
        if _available(memory, i):
            index_of_next = _index_of_next(memory, i)
            if index_of_next < mem_size and _available(memory, index_of_next):
                _set_bin_size(memory, i, _bin_size(memory, i) + SIZEOF_BIN + _bin_size(memory, index_of_next))
    memspace = (memsize, memory)
    return memspace

def defragment(memspace: MemSpace) -> MemSpace:
    return _defrag_from(memspace, 0)
