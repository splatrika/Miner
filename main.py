import pygame

from Source.Core.Vector2i import Vector2i
from Source.Core.GameLoop import GameLoopObject, GameLoop
from Source.Gameplay.Models.GameField import GameField
from Source.Gameplay.ViewControllers.GameFieldViewController import GameFieldViewController

NAME = "Miner"
WINDOW_SIZE = Vector2i(350, 500)
GAME_FIELD_SIZE = Vector2i(10, 10)
COUNT_OF_MINES = 10

def main():
    pygame.init()
    pygame.display.set_caption(NAME)
    window_surface: pygame.Surface = pygame.display.set_mode(WINDOW_SIZE)

    game_field = GameField(GAME_FIELD_SIZE, COUNT_OF_MINES, None)
    view_controller = GameFieldViewController(game_field)

    game_loop = GameLoop(window_surface, view_controller)
    game_loop.run()



if __name__ == '__main__':
    main()
