import pygame

from Source.Core.Vector2i import Vector2i, INT_EIGHT_DIRECTIONS
from Source.Gameplay.Models.OpenedCell import OpenedCell
from Source.Gameplay.Models.MineCell import MineCell
from Source.Gameplay.Models.ClosedCell import ClosedCell
from typing import List


class SafeCell(OpenedCell):
    def __init__(self, position : Vector2i, fieldWithMines : List[List[ClosedCell]]):
        self._mines_around = self._count_mines_around(position, fieldWithMines)

    def get_mines_around(self):
        return self._mines_around

    def _count_mines_around(self, position : Vector2i, fieldWithMines : List[List[ClosedCell]]) -> int:
        count = 0
        for direction in INT_EIGHT_DIRECTIONS:
            position_for_check = Vector2i(position.x - direction.x,
                                          position.y - direction.y)
            y_out_of_field = position_for_check.y >= len(fieldWithMines)  or position_for_check.y < 0
            if y_out_of_field:
                continue
            line = fieldWithMines[position_for_check.y]
            x_out_of_fielf = position_for_check.x >= len(line) or position_for_check.x < 0
            if x_out_of_fielf:
                continue
            checking_cell = line[position_for_check.x]
            if checking_cell != None and checking_cell.get_content_type() == MineCell:
                count += 1
        return count
