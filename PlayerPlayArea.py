from pygame import Color


class PlayerPlayArea:
    def __init__(self, font, x_start, width):
        self.font = font
        self.x_start = x_start
        self.width = width

    def draw_player_play_area(self, player, surface):
        self.__draw_current_turn_text(player, surface)

    def __draw_current_turn_text(self, player, surface):
        text = self.font.render("Current player's turn: " + player.character.value, True, Color("black"))
        text_rect = text.get_rect()
        text_rect.center = (self.x_start + (self.width / 2), text_rect.height)
        surface.blit(text, text_rect)