from typing import NamedTuple

Vector2i = NamedTuple("Vector2i", [('x', int), ('y', int)])

INT_EIGHT_DIRECTIONS = [Vector2i(0, 1), Vector2i(0, -1), Vector2i(1, 0), Vector2i(-1, 0),
                        Vector2i(1, 1), Vector2i(-1, 1), Vector2i(1, -1), Vector2i(-1, -1)]