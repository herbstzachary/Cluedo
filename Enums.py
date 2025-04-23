from enum import Enum, StrEnum

class TileTypes(Enum):
    HALLWAY = 0,
    ROOM = 1,
    ROOM_ENTRANCE = 2,
    PASSAGE_ONE = 3,
    PASSAGE_TWO = 4,
    EMPTY = 5

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

class Rooms(StrEnum):
    KITCHEN = "Kitchen",
    DINING_ROOM = "Dining Room",
    LOUNGE = "Lounge",
    BALLROOM = "Ballroom",
    HALL = "Hall",
    CONSERVATORY = "Conservatory",
    BILLIARD_ROOM = "Billiard Room",
    LIBRARY = "Library",
    STUDY = "Study"

class Weapons(StrEnum):
    CANDLESTICK = "Candlestick",
    DAGGER = "Dagger",
    LEAD_PIPE = "Lead Pipe",
    REVOLVER = "Revolver",
    ROPE = "Rope",
    WRENCH = "Wrench"

class TurnPhases(StrEnum):
    MOVE = "Move",
    SUGGEST = "Suggest",
    ACCUSE = "Accuse"