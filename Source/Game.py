import pygame
from pygame import *
from pygame_gui import *
from pygame_gui.elements import *

WINDOW_SIZE : Vector2 = Vector2(300, 400)
NAME = "Miner"
CLEAR_COLOR : Color = Color(255, 255, 255, 255)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(NAME)
        window_surface : Surface = pygame.display.set_mode(WINDOW_SIZE)
        ui_manager : UIManager = UIManager((WINDOW_SIZE.x, WINDOW_SIZE.y))
        test_button = UIButton(Rect(0, 0, 100, 100), "Hello", ui_manager)

        running : bool = True

        while running:
            time_delta = 1 #TODO upd
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                ui_manager.process_events(event)

            ui_manager.update(time_delta)

            window_surface.fill(CLEAR_COLOR)
            ui_manager.draw_ui(window_surface)

            pygame.display.update()
