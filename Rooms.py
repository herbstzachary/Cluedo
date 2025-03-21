from Enums import EntranceDirections

class Kitchen:
    name = "Kitchen"

    def __init__(self):
        self.locations = []
        for x in range(1, 7):
            for y in range (1, 7):
                if (x, y) != (1, 6):
                    self.locations.append((x,y))

        self.center = (4, 3)
        self.entrances = [(5, 6, EntranceDirections.SOUTH)]

class DiningRoom:
    name = "Dining Room"

    def __init__(self):
        self.locations = []
        for x in range(1, 9):
            for y in range (9, 16):
                if (x, y) != (6, 9) and (x, y) != (7, 9) and (x, y) != (8, 9):
                    self.locations.append((x,y))

        self.center = (5, 12)
        self.entrances = [(8, 12, EntranceDirections.EAST), (7, 15, EntranceDirections.SOUTH)]

class Lounge:
    name =  "Lounge"

    def __init__(self):
        self.locations = []
        for x in range(1, 8):
            for y in range(19, 25):
                if (x, y) != (7, 24):
                    self.locations.append((x, y))

        self.center = (4, 22)
        self.entrances = [(7, 19, EntranceDirections.NORTH)]

class Ballroom:
    name = "Ballroom"

    def __init__(self):
        self.locations = []
        for x in range(9, 17):
            for y in range(1, 8):
                if (x, y) != (9, 1) and (x, y) != (10, 1) and (x, y) != (15, 1) and (x, y) != (16, 1):
                    self.locations.append((x, y))

        self.center = (13, 4)
        self.entrances = [
            (9, 5, EntranceDirections.WEST),
            (10, 7, EntranceDirections.SOUTH),
            (15, 7, EntranceDirections.SOUTH),
            (16, 5, EntranceDirections.EAST)
        ]

class Center:
    name = ""

    def __init__(self):
        self.locations = []
        for x in range(11, 16):
            for y in range(10, 17):
                self.locations.append((x, y))

        self.center = (13, 13)
        self.entrances = []

class Hall:
    name = "Hall"

    def __init__(self):
        self.locations = []
        for x in range(10, 16):
            for y in range(18, 24):
                self.locations.append((x, y))

        self.center = (13, 21)
        self.entrances = [(12, 18, EntranceDirections.NORTH), (13, 18, EntranceDirections.NORTH)]

class Conservatory:
    name = "Conservatory"

    def __init__(self):
        self.locations = []
        for x in range(19, 25):
            for y in range(1, 6):
                if (x, y) != (19, 5) and (x,y) != (24, 5):
                    self.locations.append((x, y))

        self.center = (22, 3)
        self.entrances = [(19, 4, EntranceDirections.SOUTH)]

class BilliardRoom:
    name = "Billiard Room"

    def __init__(self):
        self.locations = []
        for x in range(19, 25):
            for y in range(8, 13):
                self.locations.append((x, y))

        self.center = (22, 10)
        self.entrances = [(19, 9, EntranceDirections.WEST), (23, 12, EntranceDirections.SOUTH)]

class Library:
    name = "Library"

    def __init__(self):
        self.locations = []
        for x in range(18, 25):
            for y in range(14, 19):
                if (x, y) not in [(18, 14), (24, 14), (18, 18), (24, 18)]:
                    self.locations.append((x, y))

        self.center = (22, 16)
        self.entrances = [(21, 14, EntranceDirections.NORTH), (18, 16, EntranceDirections.WEST)]

class Study:
    name = "Study"

    def __init__(self):
        self.locations = []
        for x in range(18, 25):
            for y in range(21, 25):
                if (x, y) != (18, 24):
                    self.locations.append((x, y))

        self.center = (22, 23)
        self.entrances = [(18, 21, EntranceDirections.NORTH)]