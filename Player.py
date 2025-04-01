class Player:

    def __init__(self, character, color, start_loc, hand):
        self.character = character
        self.color = color
        self.current_loc = start_loc
        self.hand = hand

    def set_location(self, new_loc):
        self.current_loc = new_loc