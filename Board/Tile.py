import pygame.draw
from pygame import Rect

from Colors import BLACK, BOARD_HALLWAY_TILE_COLOR, BOARD_ROOM_TILE_COLOR, BOARD_MOVE_CANDIDATE_TILE_COLOR, PURPLE, AQUA
from Enums import TileTypes

class Tile:
    def __init__(self, size, x, y, coord_offset):
        self.x = x
        self.y = y
        self.rect = Rect(
            (x * size) + coord_offset[0],
            (y * size) + coord_offset[1],
            size,
            size
        )
        self.tile_type = TileTypes.HALLWAY
        self.entrance_direction = None
        self.move_candidate = False
        self.occupied = False

    def draw(self, surface):
        if self.move_candidate:
            pygame.draw.rect(surface, BOARD_MOVE_CANDIDATE_TILE_COLOR, self.rect)
            pygame.draw.rect(surface, BLACK, self.rect, width=1)
        elif self.tile_type == TileTypes.HALLWAY:
            pygame.draw.rect(surface, BOARD_HALLWAY_TILE_COLOR, self.rect)
            pygame.draw.rect(surface, BLACK, self.rect, width=1)
        elif self.tile_type == TileTypes.ROOM_ENTRANCE or self.tile_type == TileTypes.ROOM:
            pygame.draw.rect(surface, BOARD_ROOM_TILE_COLOR, self.rect)
        elif self.tile_type == TileTypes.PASSAGE_ONE:
            pygame.draw.rect(surface, PURPLE, self.rect)
        elif self.tile_type == TileTypes.PASSAGE_TWO:
            pygame.draw.rect(surface, AQUA, self.rect)