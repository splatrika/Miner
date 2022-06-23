import pygame.event

class GameLoopObject:
    def on_input(self, event : pygame.event.Event):
        pass

    def on_update(self, time_delta : float):
        pass

    def on_draw(self, surface : pygame.Surface):
        pass
