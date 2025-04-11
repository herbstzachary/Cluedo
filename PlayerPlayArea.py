import pygame
from pygame import Color, Rect

import Enums


class PlayerPlayArea:
    def __init__(self, top_font, card_font, x_start, width):
        self.top_font = top_font
        self.card_font = card_font
        self.x_start = x_start
        self.width = width
        self.height = pygame.display.Info().current_h

        self.x_margin = width / 100
        self.y_margin = self.height / 100
        self.current_player_text_bottom = 0
        self.rooms = list(Enums.Rooms)
        self.weapons = list(Enums.Weapons)
        self.suspects = list(Enums.Characters)

    def __draw_current_turn_text(self, player, phase, surface):
        text = self.top_font.render(player.character.value + "'s " + phase + " Phase", True, Color("black"))
        text_rect = text.get_rect()
        text_rect.center = (self.x_start + (self.width / 2), text_rect.height)
        surface.blit(text, text_rect)

        self.current_player_text_bottom = text_rect.bottom

    # def __draw_clue_category_title(self, center_x, top_y, title, surface):
    #     text = self.top_font.render(title, True, Color("black"))
    #     text_rect = text.get_rect()
    #     text_rect.center = (center_x, center_y)
    #     surface.blit(text, text_rect)

    def __draw_clues(self, clues, left_x, top_y, card_width, card_height, player, surface):
        initial_left_x = left_x
        counter = 0
        for clue in clues:
            if clue in player.knowledge:
                pygame.draw.rect(surface, Color("red"), Rect(left_x, top_y, card_width, card_height))
            pygame.draw.rect(surface, Color("black"), Rect(left_x, top_y, card_width, card_height), width=2)
            text = self.card_font.render(clue, True, Color("black"))
            text_rect = text.get_rect()
            text_rect.center = (left_x + (card_width / 2), top_y + (card_height / 2))
            text_rect.width = card_width
            surface.blit(text, text_rect)
            if counter < (len(clues) / 3) - 1:
                left_x += card_width
                counter += 1
            else:
                top_y += card_height
                left_x = initial_left_x
                counter = 0

    def __draw_player_clue_info(self, player, surface):
        top_y = self.current_player_text_bottom + self.y_margin
        left_x = self.x_start + self.x_margin
        card_width = int((self.width - (self.x_margin * 5)) / 7)
        card_height = int((self.height - self.y_margin - top_y) / 3)

        self.__draw_clues(self.rooms, left_x, top_y, card_width, card_height, player, surface)

        left_x += (card_width * 3) + self.x_margin
        self.__draw_clues(self.weapons, left_x, top_y, card_width, card_height, player, surface)

        left_x += (card_width * 2) + self.x_margin
        self.__draw_clues(self.suspects, left_x, top_y, card_width, card_height, player, surface)

    def draw_player_play_area(self, player, turn_phase, surface):
        self.__draw_current_turn_text(player, turn_phase, surface)
        self.__draw_player_clue_info(player, surface)

    def select_cards_for_guess(self, mouse):
        return 0