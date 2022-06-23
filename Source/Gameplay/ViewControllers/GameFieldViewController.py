import math

import pygame
import pygame_gui
import pygame_gui.elements as ui_elements

from Source.Core.Vector2i import Vector2i
from Source.Core.GameLoopObject import GameLoopObject
from Source.Gameplay.Models.GameField import IGameFieldDelegate, GameField
from Source.Gameplay.Models.ClosedCell import ClosedCell
from Source.Gameplay.Models.MineCell import MineCell
from Source.Gameplay.Models.OpenedCell import OpenedCell
from Source.Gameplay.Models.SafeCell import SafeCell
from typing import List
from enum import Enum


WINDOW_SIZE = Vector2i(350, 500) #TODO move to constrants


class PlayerMode(Enum):
    OPENING_CELLS = 0
    FLAGGING = 1


class GameFieldViewController(GameLoopObject, IGameFieldDelegate):
    def __init__(self, field : GameField):
        self._field = field
        self._field.register_delegate(self)
        self._mode : PlayerMode = PlayerMode.OPENING_CELLS
        self._buttons : List[List[pygame_gui.elements.UIButton]] = []
        self._message_label : pygame_gui.elements.UILabel
        self._change_mode_button : pygame_gui.elements.UIButton
        self._ui_manager = pygame_gui.UIManager(WINDOW_SIZE)
        self._create_ui()

        self._time = 0
        self._bad_circle_radius = 0
        self._bad_position = Vector2i(0, 0)


    def _create_ui(self):
        change_mode_button_rect = pygame.Rect(40, 433, 270, 36)
        self._change_mode_button = ui_elements.UIButton(change_mode_button_rect, "Current mode: opening",
                                                        self._ui_manager)
        mines_label_rect = pygame.Rect(0, 16, 350, 22)
        self._message_label = ui_elements.UILabel(mines_label_rect, f"Mines: {self._field.get_mines_count()}", self._ui_manager)

        cell_button_size = WINDOW_SIZE.x / self._field.get_size().x
        buttons_offset = Vector2i(0, 50)

        for iy in range(self._field.get_size().y):
            self._buttons.append([])
            for ix in range(self._field.get_size().x):
                button_rect = pygame.Rect(cell_button_size * ix + buttons_offset.x,
                                          cell_button_size * iy + buttons_offset.y,
                                          cell_button_size,
                                          cell_button_size)
                button = ui_elements.UIButton(button_rect, "", self._ui_manager)
                self._buttons[iy].append(button)
                self._update_cell(Vector2i(ix, iy))


    def on_update(self, time_delta : float):
        self._ui_manager.update(time_delta)
        self._time += time_delta
        self._bad_circle_radius = math.fabs(math.sin(self._time * 3) * 50) + 20


    def on_draw(self, surface : pygame.Surface):
        self._ui_manager.draw_ui(surface)
        color = pygame.Color(255, 0, 0, 255)
        if self._field.is_lose() or self._field.is_win():
            tint = pygame.Surface(Vector2i(WINDOW_SIZE.x, WINDOW_SIZE.x))
            tint.fill(pygame.Color(0, 0, 0))
            tint.set_alpha(100)
            surface.blit(tint, Vector2i(0, 50))
        if self._field.is_lose():
            pygame.draw.circle(surface, color, self._bad_position, self._bad_circle_radius, 10)


    def on_input(self, event : pygame.event.Event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self._change_mode_button:
                if not self._field.is_lose():
                    self._mode = PlayerMode.OPENING_CELLS if self._mode == PlayerMode.FLAGGING else PlayerMode.FLAGGING
                    self._update_mode_button()
                else:
                    self._field.restart()
            else:
                for iy in range(self._field.get_size().y):
                    for ix in range(self._field.get_size().x):
                        if event.ui_element == self._buttons[iy][ix]:
                            cell = self._field.get_cell(Vector2i(ix, iy))
                            print(f"CLICKED ON CELL: {type(cell)}")
                            if type(cell) == ClosedCell and not self._field.is_lose() and not self._field.is_win():
                                closed_cell: ClosedCell = cell
                                if self._mode == PlayerMode.OPENING_CELLS:
                                    print(f"Open cell: {(ix, iy)}")
                                    closed_cell.open()
                                if self._mode == PlayerMode.FLAGGING:
                                    print(f"Flag cell: {(ix, iy)}")
                                    closed_cell.set_flag(not closed_cell.is_flagged())


        self._ui_manager.process_events(event)


    def on_cell_flag_changed(self, at: Vector2i, value: bool):
        self._update_cell(at)


    def on_cell_opened(self, at: Vector2i, content: OpenedCell):
        self._update_cell(at)


    def on_lose(self, mine_at : Vector2i):
        self._change_mode_button.set_text("Restart")
        self._message_label.set_text("LOSE!")
        button_size = int(WINDOW_SIZE.x / self._field.get_size().x)
        self._bad_position = Vector2i(button_size * mine_at.x + button_size / 2 + 2,
                                      button_size * mine_at.y + 50 + button_size / 2 + 2)

    def on_win(self):
        self._message_label.set_text("WIN!")

    def on_restart(self):
        for iy in range(self._field.get_size().y):
            for ix in range(self._field.get_size().x):
                self._buttons[iy][ix].enable()
                self._update_cell(Vector2i(ix, iy))
        self._update_mode_button()
        self._message_label.set_text(f"Mines: {self._field.get_mines_count()}")

    def _update_mode_button(self):
        mode_caption = "opening" if self._mode == PlayerMode.OPENING_CELLS else "flagging"
        self._change_mode_button.set_text(f"Current mode: {mode_caption}")

    def _update_cell(self, at : Vector2i):
        print(f"UPDATE CELL {at}")
        button = self._buttons[at.y][at.x]
        cell = self._field.get_cell(at)
        if type(cell) == ClosedCell:
            closed_cell : ClosedCell = cell
            caption = "x" if closed_cell.is_flagged() else ""
            button.set_text(caption)
            button.colours["active_bg"] = pygame.Color(54, 88, 128)
        elif type(cell) == MineCell:
            button.set_text("*")
            button.colours["active_bg"] = pygame.Color(190, 15, 15)
        elif type(cell) == SafeCell:
            safe_cell : SafeCell = cell
            button.set_text(str(safe_cell.get_mines_around()))
            button.colours["active_bg"] = pygame.Color(190, 190, 190)
