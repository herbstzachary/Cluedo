import pygame.draw
from pygame import Color, Rect

from Enums import TileTypes, EntranceDirections

class Tile:
    def __init__(self, size, x, y, coord_offset):
        self.x = x
        self.y = y
        self.size = size
        self.top_left_corner = ((x * size) + coord_offset[0], (y * size) + coord_offset[1])
        self.tile_type = TileTypes.HALLWAY
        self.entrance_direction = None
        self.move_candidate = False
        self.occupied = False

    def draw(self, surface):
        x_coord = self.top_left_corner[0]
        y_coord = self.top_left_corner[1]

        if self.move_candidate:
            pygame.draw.rect(surface, Color("orange2"), Rect(x_coord, y_coord, self.size, self.size))
            pygame.draw.rect(surface, Color(210, 180, 140), Rect(x_coord, y_coord, self.size, self.size), width=1)
        elif self.tile_type == TileTypes.HALLWAY:
            pygame.draw.rect(surface, Color(100, 100, 100), Rect(x_coord, y_coord, self.size, self.size))
            pygame.draw.rect(surface, Color(210, 180, 140), Rect(x_coord, y_coord, self.size, self.size), width=1)
        elif self.tile_type == TileTypes.ROOM_ENTRANCE:
            pygame.draw.rect(surface, Color(0, 255, 0), Rect(x_coord, y_coord, self.size, self.size))
        elif self.tile_type == TileTypes.ROOM:
            pygame.draw.rect(surface, Color(0, 0, 255), Rect(x_coord, y_coord, self.size, self.size))
        else:
            pygame.draw.rect(surface, Color("white"), Rect(x_coord, y_coord, self.size, self.size))

