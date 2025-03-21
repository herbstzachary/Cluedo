class Player:

    def __init__(self, character, color, start_loc):
        self.character = character
        self.color = color
        self.current_loc = start_loc

    def set_location(self, new_loc):
        self.current_loc = new_loc