from random import randint
from functools import reduce
from typing import Optional

from commands import Cmd
from logger import Logger
import numpy as np


BINARY_PIECE_SIZE = 8
WORD_SIZE = 64
PIECES_NUMBER = int(WORD_SIZE / BINARY_PIECE_SIZE)
PIECES_TABLE_SIZE = 2 ** PIECES_NUMBER


def _get_binary_piece(n: np.int64, index: int) -> np.int8:
    offset = WORD_SIZE - (index + 1) * BINARY_PIECE_SIZE
    return np.int8(n << offset >> (WORD_SIZE - BINARY_PIECE_SIZE))


def _split_in_binary_pieces(n: np.int64) -> (np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8, np.int8):
    return tuple([_get_binary_piece(n, i) for i in range(0, 8)][::-1])


class RandomTable:
    def __init__(self, table_size=10):
        self.table = [np.int64(randint(0, 2 ** 63 - 1)) for _ in range(table_size)]

    def get(self, n):
        return self.table[n]


class Element:
    def __init__(self, value: Optional[np.int64] = None):
        self.value = value
        self.removed = False

    def is_defined(self) -> bool:
        return self.value is not None

    def remove(self):
        self.value = None
        self.removed = True


def _init_table(n):
    return [Element() for _ in range(n)]


class Hashtable:
    def __init__(self, table_size: int, logger: Logger, grow_threshold=0.75, shrink_threshold=0.25):
        logger.cmd(Cmd.TAM, table_size)
        self.logger = logger
        self._table_size = table_size
        self._filled = 0
        self._removed_count = 0
        self._removed_clean_threshold = 0.25
        self._table = _init_table(table_size)
        self._grow_threshold = grow_threshold
        self._shrink_threshold = shrink_threshold
        self._pieces_tables = [RandomTable(PIECES_TABLE_SIZE) for _ in range(PIECES_NUMBER)]

    def _hash_fn(self, x: np.int64) -> int:
        pieces = _split_in_binary_pieces(x)
        positions = [self._pieces_tables[i].get(piece) for i, piece in enumerate(pieces)]
        return reduce(lambda a, b: a ^ b, positions)

    def apply(self, cmd: Cmd, value: np.int64) -> None:
        if cmd == Cmd.INC:
            self.add(value)
        elif cmd == Cmd.BUS:
            self.get(value)
        elif cmd == Cmd.REM:
            self.remove(value)

    def _internal_add(self, value: np.int64) -> (int, int):
        hash_result = self._hash_fn(value)
        offset = 0
        position = (hash_result + offset) % self._table_size
        while self._table[position].is_defined():
            offset += 1
            position = (hash_result + offset) % self._table_size
        self._table[position] = Element(value)

        return hash_result, position

    def add(self, value: np.int64) -> int:
        hash_result, position = self._internal_add(value)

        self.logger.input((Cmd.INC, value), hash_result, position)
        self._filled += 1

        if (self._filled / self._table_size) > self._grow_threshold:
            self._doubling()

        return position

    def remove(self, value: np.int64) -> None:
        hash_result, position = self._internal_get(value)

        self.logger.input((Cmd.REM, value), hash_result, position)

        if position >= 0:
            self._table[position].remove()
            self._removed_count += 1
            self._filled -= 1

            if (self._removed_count / self._table_size) > self._removed_clean_threshold:
                self._clean_removed()

            if (self._filled / self._table_size) < self._shrink_threshold:
                self._halving()

    def _internal_get(self, value: np.int64) -> (int, int):
        hash_result = self._hash_fn(value)
        offset = 0
        position = (hash_result + offset) % self._table_size
        element = self._table[position]

        while (element.removed or element.value != value) and offset < self._table_size:
            position = (hash_result + offset) % self._table_size
            element = self._table[position]
            offset += 1

        return (hash_result, position) if element.value == value else (hash_result, -1)

    def get(self, value: np.int64) -> (int, int):
        hash_result, position = self._internal_get(value)
        self.logger.input((Cmd.BUS, value), hash_result, position)
        return hash_result, position

    def _copy(self, old_table):
        for el in old_table:
            if el.value is not None:
                self._internal_add(el.value)
        self._removed_count = 0

    def _doubling(self):
        old_table = self._table.copy()
        self._table_size = self._table_size * 2
        self._table = _init_table(self._table_size)
        self._copy(old_table)

        self.logger.cmd(Cmd.DOBRAR_TAM, self._table_size)

    def _halving(self):
        old_table = self._table.copy()
        self._table_size = int(self._table_size / 2)
        self._table = _init_table(self._table_size)
        self._copy(old_table)

        self.logger.cmd(Cmd.METADE_TAM, self._table_size)

    def _clean_removed(self):
        def clean(i=0):
            removed_start = None
            removed_end = None

            if i >= self._table_size:
                return

            while i < self._table_size:
                if self._table[i].removed:
                    self._table[i] = Element()
                    if removed_start is None:
                        removed_start = i
                if self._table[i].is_defined() and removed_start is not None:
                    removed_end = i
                    break
                i += 1

            if removed_end is not None and removed_start is not None:
                removed_size = removed_end - removed_start
                while i < self._table_size:
                    if self._table[i].is_defined():
                        self._table[i - removed_size] = self._table[i]
                        self._table[i] = Element()
                        i += 1
                    else:
                        break

                clean(i)

        clean()

        self._removed_count = 0

        self.logger.cmd(Cmd.LIMPAR)
