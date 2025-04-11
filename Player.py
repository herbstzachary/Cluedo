class Player:

    def __init__(self, character, color, start_loc, hand):
        self.character = character
        self.color = color
        self.current_loc = start_loc
        self.hand = hand
        self.knowledge = hand

    def set_location(self, new_loc):
        self.current_loc = new_loc

    def add_knowledge(self, clue):
        self.knowledge.append(clue)