import pygame
from pygame import Rect

from Helpers import Enums
from Helpers.Colors import RED, BLUE, BLACK, CARD_BACKGROUND_COLOR, HAND_CARD_BACKGROUND_COLOR, \
    BOARD_CARD_BACKGROUND_COLOR
from Helpers.Enums import TurnPhases
from Player.Card import Card


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
        cards = {}
        top = area.top
        left = area.left
        counter = 0

        for card in category:
            rect = Rect(left, top, self.card_width, self.card_height)
            cards[card] = Card(rect)
            if counter < (len(category) / 3) - 1:
                left += self.card_width
                counter += 1
            else:
                top += self.card_height
                left = area.left
                counter = 0

        return cards

    def __draw_clues(self, cards, player, surface):
        for card_type in cards:
            card = cards.get(card_type)
            left_x = card.rect.left
            top_y = card.rect.top

            text = self.card_font.render(card_type, True, BLACK)
            additional_text = None

            if card_type in self.current_suggestion.values():
                pygame.draw.rect(surface, BLUE, card.rect)
            elif card_type in player.hand:
                pygame.draw.rect(surface, HAND_CARD_BACKGROUND_COLOR, card.rect)
            elif card_type in player.board_cards:
                pygame.draw.rect(surface, BOARD_CARD_BACKGROUND_COLOR, card.rect)
            elif card_type in player.knowledge.keys():
                pygame.draw.rect(surface, RED, card.rect)
                additional_text = self.card_font.render("(" + player.knowledge[card_type].character.value + ")", True, BLACK)
            else:
                pygame.draw.rect(surface, CARD_BACKGROUND_COLOR, card.rect)

            guess_radius = (card.rect.width / 9)
            guess_center_x = card.rect.left + guess_radius + 5
            guess_center_y = card.rect.top + guess_radius + 5
            count = 0
            for guess in card.guessed:
                pygame.draw.circle(surface, guess.color, (guess_center_x, guess_center_y), guess_radius)
                guess_center_x += guess_radius * 3
                if count >= 2:
                    guess_center_x = card.rect.left + guess_radius + 5
                    guess_center_y += guess_radius * 2
                    count = 0
                else:
                    count += 1

            pygame.draw.rect(surface, BLACK, card.rect, width=2)
            text_rect = text.get_rect()
            text_rect.center = (left_x + (self.card_width / 2), top_y + (self.card_height / 2))
            surface.blit(text, text_rect)

            if additional_text is not None:
                additional_text_rect = additional_text.get_rect()
                additional_text_rect.center = (text_rect.centerx, text_rect.bottom + (additional_text_rect.height / 2))
                surface.blit(additional_text, additional_text_rect)

    def __draw_player_clue_info(self, player, surface):
        self.__draw_clues(self.room_cards, player, surface)
        self.__draw_clues(self.weapon_cards, player, surface)
        self.__draw_clues(self.character_cards, player, surface)

    def draw_player_play_area(self, player, turn_phase, move_amount, surface):
        self.__draw_player_clue_info(player, surface)

    def select_card_for_guess(self, mouse, phase):
        if phase == TurnPhases.ACCUSE:
            for entry in self.room_cards.items():
                card_type = entry[0]
                card = entry[1]
                if card.rect.collidepoint(mouse):
                    self.current_suggestion[Enums.Rooms] = card_type
                    return

        for entry in self.weapon_cards.items():
            card_type = entry[0]
            card = entry[1]
            if card.rect.collidepoint(mouse):
                self.current_suggestion[Enums.Weapons] = card_type
                return

        for entry in self.character_cards.items():
            card_type = entry[0]
            card = entry[1]
            if card.rect.collidepoint(mouse):
                self.current_suggestion[Enums.Characters] = card_type
                return

    def clear_suggestion(self):
        for key in self.current_suggestion.keys():
            self.current_suggestion[key] = None