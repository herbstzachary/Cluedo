from enum import Enum

class TileTypes(Enum):
    HALLWAY = 0,
    ROOM = 1,
    ROOM_ENTRANCE = 2,
    EMPTY = 3

class EntranceDirections(Enum):
    NORTH = 0,
    EAST = 1,
    SOUTH = 2,
    WEST = 3

class Characters(Enum):
    SCARLET = 0,
    MUSTARD = 1,
    WHITE = 2,
    GREEN = 3,
    PEACOCK = 4,
    PLUM = 5