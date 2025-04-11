class Player:

    def __init__(self, character, color, start_tile, hand):
        self.character = character
        self.color = color
        self.current_tile = start_tile
        self.hand = hand
        self.knowledge = hand

    def add_knowledge(self, clue):
        self.knowledge.append(clue)