from enum import Enum, StrEnum


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

class Characters(StrEnum):
    SCARLET = "Miss Scarlet",
    MUSTARD = "Colonel Mustard",
    WHITE = "Mrs. White",
    GREEN = "Mr. Green",
    PEACOCK = "Mrs. Peacock",
    PLUM = "Professor Plum"