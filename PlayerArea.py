import pygame
from pygame import Rect

import Enums
from Card import Card
from Colors import RED, YELLOW, BLUE, BLACK, WHITE
from Enums import TurnPhases


class PlayerArea:
    def __init__(self, area: Rect, card_font):
        self.area = area
        self.card_font = card_font

        self.x_margin = area.width / 100
        self.y_margin = area.height / 100
        self.rooms = list(Enums.Rooms)
        self.weapons = list(Enums.Weapons)
        self.suspects = list(Enums.Characters)

        self.current_suggestion = {
            Enums.Rooms: None,
            Enums.Weapons: None,
            Enums.Characters: None
        }

        top_y = area.top
        left_x = area.left
        self.card_width = int((area.width - (self.x_margin * 2)) / 7)
        self.card_height = int(area.height / 3)

        room_cards_area = Rect(left_x, top_y, (self.card_width * 3) + (self.x_margin * 2), self.card_height * 3)
        self.room_cards = self.__create_cards(room_cards_area, Enums.Rooms)

        left_x += room_cards_area.width + self.x_margin
        weapon_cards_area = Rect(left_x, top_y, (self.card_width * 2) + self.x_margin, self.card_height * 3)
        self.weapon_cards = self.__create_cards(weapon_cards_area, Enums.Weapons)

        left_x += weapon_cards_area.width + self.x_margin
        character_cards_area = Rect(left_x, top_y, (self.card_width * 2) + self.x_margin, self.card_height * 3)
        self.character_cards = self.__create_cards(character_cards_area, Enums.Characters)

    def __create_cards(self, area, category):
        cards = []
        top = area.top
        left = area.left
        counter = 0

        for card in category:
            rect = Rect(left, top, self.card_width, self.card_height)
            cards.append(Card(rect, card))
            if counter < (len(category) / 3) - 1:
                left += self.card_width
                counter += 1
            else:
                top += self.card_height
                left = area.left
                counter = 0

        return cards

    def __draw_clues(self, cards, player, surface):
        for card in cards:
            left_x = card.rect.left
            top_y = card.rect.top
            card_rect = Rect(left_x, top_y, self.card_width, self.card_height)
            pygame.draw.rect(surface, WHITE, card_rect)

            if card.type in player.knowledge:
                pygame.draw.rect(surface, RED, card_rect)

            if card.type in player.hand:
                pygame.draw.rect(surface, YELLOW, card_rect)

            if card.type in self.current_suggestion.values():
                pygame.draw.rect(surface, BLUE, card_rect)

            pygame.draw.rect(surface, BLACK, card_rect, width=2)
            text = self.card_font.render(card.type, True, BLACK)
            text_rect = text.get_rect()
            text_rect.center = (left_x + (self.card_width / 2), top_y + (self.card_height / 2))
            text_rect.width = self.card_width
            surface.blit(text, text_rect)

    def __draw_player_clue_info(self, player, surface):
        self.__draw_clues(self.room_cards, player, surface)
        self.__draw_clues(self.weapon_cards, player, surface)
        self.__draw_clues(self.character_cards, player, surface)

    def draw_player_play_area(self, player, turn_phase, move_amount, surface):
        self.__draw_player_clue_info(player, surface)

    def select_card_for_guess(self, mouse, phase):
        if phase == TurnPhases.ACCUSE:
            for card in self.room_cards:
                if card.rect.collidepoint(mouse):
                    self.current_suggestion[Enums.Rooms] = card.type
                    return

        for card in self.weapon_cards:
            if card.rect.collidepoint(mouse):
                self.current_suggestion[Enums.Weapons] = card.type
                return

        for card in self.character_cards:
            if card.rect.collidepoint(mouse):
                self.current_suggestion[Enums.Characters] = card.type
                return

    def clear_suggestion(self):
        for key in self.current_suggestion.keys():
            self.current_suggestion[key] = None