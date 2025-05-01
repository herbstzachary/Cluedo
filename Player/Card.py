class Card:
    def __init__(self, rect):
        self.rect = rect
        self.guessed = []
        self.possibly_revealed = []