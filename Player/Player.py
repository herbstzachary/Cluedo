class Player:
    def __init__(self, character, color, start_tile):
        #Can only assign hands after we know how many players there are
        self.hand = None
        self.knowledge = {}

        self.character = character
        self.color = color
        self.current_tile = start_tile

        self.active = True

    def set_hand(self, hand):
        self.hand = hand

    def add_knowledge(self, clue):
        self.knowledge.update(clue)