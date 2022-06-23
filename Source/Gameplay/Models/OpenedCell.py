from Source.Gameplay.Models.Cell import Cell
from typing import TypeVar


class OpenedCell: pass


T = TypeVar("T", OpenedCell, OpenedCell)


class OpenedCell(Cell):
    def GetAs(self) -> T:
        if type(self) != T:
            return None
        return self
