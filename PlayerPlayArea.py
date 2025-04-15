import pygame
from pygame import Color, Rect

import Enums
from Card import Card
from Enums import TileTypes, TurnPhases


class PlayerPlayArea:
    def __init__(self, top_font, card_font, x_start, width):
        self.top_font = top_font
        self.card_font = card_font
        self.x_start = x_start
        self.width = width
        self.height = pygame.display.Info().current_h

        self.x_margin = width / 100
        self.y_margin = self.height / 100
        self.rooms = list(Enums.Rooms)
        self.weapons = list(Enums.Weapons)
        self.suspects = list(Enums.Characters)

        top_y = self.y_margin + top_font.size("Phase")[1]
        left_x = self.x_start + self.x_margin
        self.card_width = int((self.width - (self.x_margin * 5)) / 7)
        self.card_height = int((self.height - self.y_margin - top_y) / 3)

        room_cards_area = Rect(left_x, top_y, (self.card_width * 3) + (self.x_margin * 2), self.card_height * 3)
        self.room_cards = self.__create_cards(room_cards_area, Enums.Rooms)

        left_x += room_cards_area.width + self.x_margin
        weapon_cards_area = Rect(left_x, top_y, (self.card_width * 2) + self.x_margin, self.card_height * 3)
        self.weapon_cards = self.__create_cards(weapon_cards_area, Enums.Weapons)

        left_x += weapon_cards_area.width + self.x_margin
        character_cards_area = Rect(left_x, top_y, (self.card_width * 2) + self.x_margin, self.card_height * 3)
        self.character_cards = self.__create_cards(character_cards_area, Enums.Characters)

        self.current_suggestion = {
            Enums.Rooms: None,
            Enums.Weapons: None,
            Enums.Characters: None
        }

        self.suggest_text = self.top_font.render("Submit Suggestion", True, Color("black"))
        self.suggest_submit_button = self.suggest_text.get_rect()
        self.suggest_submit_button.center = (self.x_start + (self.width / 2), self.suggest_submit_button.height / 2)

        self.accuse_text = self.top_font.render("Accuse", True, Color("black"))
        self.accuse_submit_button = self.accuse_text.get_rect()
        self.accuse_submit_button.center = (self.x_start + (self.width / 4), self.accuse_submit_button.height / 2)

        self.skip_accuse_text = self.top_font.render("Skip Accuse Phase", True, Color("black"))
        self.skip_accuse_button = self.skip_accuse_text.get_rect()
        self.skip_accuse_button.center = (
            self.accuse_submit_button.left + self.accuse_submit_button.width + (self.width / 2),
            self.skip_accuse_button.height / 2
        )

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

    def __draw_current_turn_text(self, player, phase, surface):
        if phase == TurnPhases.MOVE:
            text = self.top_font.render(player.character.value + "'s " + phase + " Phase", True, Color("black"))
            text_rect = text.get_rect()
            text_rect.center = (self.x_start + (self.width / 2), (text_rect.height / 2))
            surface.blit(text, text_rect)
        elif phase == TurnPhases.SUGGEST:
            text_rect = self.suggest_submit_button
            if None in self.current_suggestion.values():
                pygame.draw.rect(surface, Color("grey"), text_rect)
            else:
                pygame.draw.rect(surface, Color("green"), text_rect)
            pygame.draw.rect(surface, Color("black"), text_rect, width=1)
            surface.blit(self.suggest_text, text_rect)
        else:
            # if None in self.current_suggestion.values():
            #     pygame.draw.rect(surface, Color("grey"), self.accuse_text_rect)
            # else:
            #     pygame.draw.rect(surface, Color("green"), self.accuse_text_rect)
            # pygame.draw.rect(surface, Color("black"), self.accuse_text_rect, width=1)
            # surface.blit(self.accuse_text, self.accuse_text_rect)

            pygame.draw.rect(surface, Color("green"), self.skip_accuse_button)
            pygame.draw.rect(surface, Color("black"), self.skip_accuse_button, width=1)
            surface.blit(self.skip_accuse_text, self.skip_accuse_button)



    # def __draw_clue_category_title(self, center_x, top_y, title, surface):
    #     text = self.top_font.render(title, True, Color("black"))
    #     text_rect = text.get_rect()
    #     text_rect.center = (center_x, center_y)
    #     surface.blit(text, text_rect)

    def __draw_clues(self, cards, player, surface):
        for card in cards:
            left_x = card.rect.left
            top_y = card.rect.top
            if card.type in player.knowledge:
                pygame.draw.rect(surface, Color("red"), Rect(left_x, top_y, self.card_width, self.card_height))
            if card.type in self.current_suggestion.values():
                pygame.draw.rect(surface, Color("blue"), Rect(left_x, top_y, self.card_width, self.card_height))
            pygame.draw.rect(surface, Color("black"), Rect(left_x, top_y, self.card_width, self.card_height), width=2)
            text = self.card_font.render(card.type, True, Color("black"))
            text_rect = text.get_rect()
            text_rect.center = (left_x + (self.card_width / 2), top_y + (self.card_height / 2))
            text_rect.width = self.card_width
            surface.blit(text, text_rect)


    def __draw_player_clue_info(self, player, surface):
        self.__draw_clues(self.room_cards, player, surface)
        self.__draw_clues(self.weapon_cards, player, surface)
        self.__draw_clues(self.character_cards, player, surface)

    def draw_player_play_area(self, player, turn_phase, surface):
        self.__draw_current_turn_text(player, turn_phase, surface)
        self.__draw_player_clue_info(player, surface)

    def select_cards_for_guess(self, mouse):
        for card in self.weapon_cards:
            if card.rect.collidepoint(mouse):
                self.current_suggestion[Enums.Weapons] = card.type
                return

        for card in self.character_cards:
            if card.rect.collidepoint(mouse):
                self.current_suggestion[Enums.Characters] = card.type
                return

    def submit_guess(self, mouse):
        if self.suggest_submit_button.collidepoint(mouse) and None not in self.current_suggestion.values():
            return True

    def skip_accuse(self, mouse):
        if self.skip_accuse_button.collidepoint(mouse):
            return True

    def clear_suggestion(self):
        for key in self.current_suggestion.keys():
            self.current_suggestion[key] = None