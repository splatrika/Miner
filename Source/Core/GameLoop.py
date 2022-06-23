import pygame
from Source.Core.GameLoopObject import GameLoopObject

CLEAR_COLOR = pygame.Color(5, 5, 5, 255)

class GameLoop:
    def __init__(self, surface : pygame.Surface, root : GameLoopObject):
        self._surface = surface
        self._root = root


    def run(self):
        running = True
        last_frame_ticks = 0
        while running:
            try:
                ticks = pygame.time.get_ticks()
                time_delta = (ticks - last_frame_ticks) / 1000.0
                last_frame_ticks = ticks
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    self._root.on_input(event)

                self._root.on_update(time_delta)
                self._surface.fill(CLEAR_COLOR)
                self._root.on_draw(self._surface)

                pygame.display.update()
            except Exception as error:
                print(f"ERROR: {error}")
