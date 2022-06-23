from Source.Core.Vector2i import Vector2i
from Source.Gameplay.Models.Cell import Cell
from Source.Gameplay.Models.OpenedCell import OpenedCell
from Source.Gameplay.Models.ClosedCell import ClosedCell, IClosedCellDelegate
from Source.Gameplay.Models.MineCell import MineCell
from Source.Gameplay.Models.SafeCell import SafeCell
from typing import List
from typing import TypeVar
from random import randint


class IGameFieldDelegate(IClosedCellDelegate):
    def on_lose(self, mine_at : Vector2i):
        pass

    def on_restart(self):
        pass

    def on_win(self):
        pass


TCell = TypeVar("TCell", Cell, OpenedCell, ClosedCell)


class GameField(IClosedCellDelegate): #TODO implement delegate
    def __init__(self, size : Vector2i, count_of_mines : int, delegate : IGameFieldDelegate):
        self._field = self._generate(size, count_of_mines)
        self._size = size
        self._delegate = delegate
        self._lose = False
        self._win = False
        self._count_of_mines = count_of_mines

    def restart(self):
        self._field = self._generate(self._size, self._count_of_mines)
        self._lose = False
        self._delegate.on_restart()

    def get_mines_count(self):
        return self._count_of_mines

    def is_lose(self) -> bool:
        return self._lose

    def is_win(self) -> bool:
        return self._win

    def register_delegate(self, delegate : IGameFieldDelegate):
        self._delegate = delegate #TODO improve

    def get_size(self) -> Vector2i:
        return  self._size

    def get_cell(self, position : Vector2i) -> TCell:
        if position.x < 0 or position.y < 0 or position.x >= self._size.x or position.y >= self._size.y:
            raise Exception("Cell position out of field")
        cell : Cell = self._field[position.y][position.x]
        return cell

    def on_cell_opened(self, at: Vector2i, content: OpenedCell):
        if self._lose:
            raise Exception("Already lose, but you're trying to open some cell")
        self._field[at.y][at.x] = content
        self._delegate.on_cell_opened(at, content)
        if type(content) == MineCell:
            self._lose = True
            self._delegate.on_lose(at)
        self._check_win()

    def on_cell_flag_changed(self, at: Vector2i, value: bool):
        self._delegate.on_cell_flag_changed(at, value)
        self._check_win()

    def _generate(self, size : Vector2i, count_of_mines : int) -> List[List[Cell]]:
        one_safe_opened = False
        one_opened_safe_cell = None
        one_safe_opened_at = Vector2i(0, 0)
        field : List[List[ClosedCell]] = []
        mine_positions = []
        mine_positions_left = count_of_mines
        while mine_positions_left > 0:
            generated_position = Vector2i(randint(0, size.x - 1), randint(0, size.y - 1))
            if generated_position in mine_positions:
                continue
            mine_positions.append(generated_position)
            mine_positions_left -= 1
        for iy in range(size.y):
            field.append([])
            for ix in range(size.x):
                field[iy].append(None)
        for position in mine_positions:
            mine = MineCell()
            cell = ClosedCell(mine, position, self)
            field[position.y][position.x] = cell
        for ix in range(size.x):
            for iy in range(size.y):
                if field[iy][ix] == None:
                    position = Vector2i(ix, iy)
                    safe_cell = SafeCell(position, field)
                    cell = ClosedCell(safe_cell, position, self)
                    field[iy][ix] = cell
                    if not one_safe_opened and safe_cell.get_mines_around() == 0:
                        one_opened_safe_cell = safe_cell
                        one_safe_opened_at = Vector2i(ix, iy)
                        one_safe_opened = True
        if one_safe_opened:
            field[one_safe_opened_at.y][one_safe_opened_at.x] = one_opened_safe_cell
        return field

    def _check_win(self):
        flagged_mines = 0
        for ix in range(self._size.x):
            for iy in range(self._size.y):
                cell = self._field[iy][ix]
                if type(cell) == ClosedCell:
                    closed_cell : ClosedCell = cell
                    if closed_cell.is_flagged():
                        if closed_cell.get_content_type() != MineCell:
                            return
                        flagged_mines += 1
        if flagged_mines == self._count_of_mines:
            self._win = True
            self._delegate.on_win()
