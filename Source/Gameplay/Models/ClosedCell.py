from typing import Type

import pygame

from Source.Core.Vector2i import Vector2i
from Source.Gameplay.Models.Cell import Cell
from Source.Gameplay.Models.OpenedCell import OpenedCell


class IClosedCellDelegate:
    def on_cell_opened(self, at: Vector2i, content: OpenedCell):
        pass

    def on_cell_flag_changed(self, at: Vector2i, value: bool):
        pass


class ClosedCell(Cell):
    def __init__(self, content: OpenedCell, position: Vector2i, delegate: IClosedCellDelegate):  # TODO add delegate
        self._content = content
        self._position = position
        self._delegate = delegate
        self._opened = False
        self._flagged = False

    def open(self):
        if self._opened:
            raise Exception("Already opened")
        self._delegate.on_cell_opened(self._position, self._content)
        self._opened = True

    def set_flag(self, value: bool):
        if self._opened:
            raise Exception("Unable to flag opened cell")
        self._flagged = value
        self._delegate.on_cell_flag_changed(self._position, value)
        print(f"FLAG SET to {value}")

    def is_flagged(self) -> bool:
        return self._flagged

    def get_content_type(self) -> Type:
        return type(self._content)
