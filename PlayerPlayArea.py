import pygame
from pygame import Color, Rect


class PlayerPlayArea:
    def __init__(self, top_font, card_font, x_start, width):
        self.top_font = top_font
        self.card_font = card_font
        self.x_start = x_start
        self.width = width

    def draw_player_play_area(self, player, surface):
        self.__draw_current_turn_text(player, surface)
        self.__draw_players_cards(player, surface)

    def __draw_current_turn_text(self, player, surface):
        text = self.top_font.render("Current player's turn: " + player.character.value, True, Color("black"))
        text_rect = text.get_rect()
        text_rect.center = (self.x_start + (self.width / 2), text_rect.height)
        surface.blit(text, text_rect)

    def __draw_players_cards(self, player, surface):
        card_width = int((self.width - 20) / len(player.hand))
        card_height = int(pygame.display.Info().current_h / 6)
        top_y = pygame.display.Info().current_h * (3/4)
        left_x = self.x_start + 10
        for card in player.hand:
            pygame.draw.rect(surface, Color("black"), Rect(left_x, top_y, card_width, card_height), width=2)
            text = self.card_font.render(card.value, True, Color("black"))
            text_rect = text.get_rect()
            text_rect.center = (left_x + (card_width / 2), top_y + (card_height / 2))
            text_rect.width = card_width
            surface.blit(text, text_rect)
            left_x = left_x + card_width + int(10 / len(player.hand))