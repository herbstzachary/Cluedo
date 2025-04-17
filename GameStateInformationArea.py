import pygame
from pygame import Color

from Enums import TurnPhases


class GameStateInformationArea:

    def __init__(self, area, font):
        self.area = area
        self.font = font

        self.suggest_text = font.render("Submit Suggestion", True, Color("black"))
        self.suggest_submit_button = self.suggest_text.get_rect()
        self.suggest_submit_button.centerx = area.centerx
        self.suggest_submit_button.top = area.top

        self.accuse_text = font.render("Accuse", True, Color("black"))
        self.accuse_submit_button = self.accuse_text.get_rect()
        self.accuse_submit_button.left = area.left
        self.accuse_submit_button.top = area.top

        self.skip_accuse_text = font.render("Skip Accuse Phase", True, Color("black"))
        self.skip_accuse_button = self.skip_accuse_text.get_rect()
        self.skip_accuse_button.right = area.right
        self.skip_accuse_button.top = area.top

        self.player_that_revealed_info = None
        self.eliminated_player = None

    def draw_info_area(self, player, phase, move_amount, guess, surface):
        if phase == TurnPhases.MOVE:
            move_text_center_x = self.area.centerx
            if self.eliminated_player is not None:
                eliminated_text = self.font.render(self.eliminated_player.character.value + " was eliminated.", True, Color("black"))
                eliminated_text_rect = eliminated_text.get_rect()
                eliminated_text_rect.left = self.area.left
                eliminated_text_rect.top = self.area.top
                surface.blit(eliminated_text, eliminated_text_rect)
                move_text_center_x = (eliminated_text_rect.right + self.area.right) / 2
            text = self.font.render(player.character.value + " can move up to " + str(move_amount) + " spaces", True, Color("black"))
            text_rect = text.get_rect()
            text_rect.center = (move_text_center_x, self.area.centery)
            surface.blit(text, text_rect)
        elif phase == TurnPhases.SUGGEST:
            text_rect = self.suggest_submit_button
            if None in guess.values():
                pygame.draw.rect(surface, Color("grey"), text_rect)
            else:
                pygame.draw.rect(surface, Color("green"), text_rect)
            pygame.draw.rect(surface, Color("black"), text_rect, width=1)
            surface.blit(self.suggest_text, text_rect)
        else:
            if None in guess.values():
                pygame.draw.rect(surface, Color("grey"), self.accuse_submit_button)
            else:
                pygame.draw.rect(surface, Color("green"), self.accuse_submit_button)
            pygame.draw.rect(surface, Color("black"), self.accuse_submit_button, width=1)
            surface.blit(self.accuse_text, self.accuse_submit_button)

            if self.player_that_revealed_info is not None:
                revealed_text = self.font.render(
                    self.player_that_revealed_info.character.value + " revealed " + player.knowledge[-1].value,
                    True,
                    Color("black")
                )
                revealed_text_rect = revealed_text.get_rect()
                revealed_text_rect.centerx = (self.skip_accuse_button.left + self.accuse_submit_button.right) / 2
                revealed_text_rect.top = self.area.top
                surface.blit(revealed_text, revealed_text_rect)

            pygame.draw.rect(surface, Color("green"), self.skip_accuse_button)
            pygame.draw.rect(surface, Color("black"), self.skip_accuse_button, width=1)
            surface.blit(self.skip_accuse_text, self.skip_accuse_button)

    def submit_guess(self, mouse, suggestion):
        return self.suggest_submit_button.collidepoint(mouse) and None not in suggestion.values()

    def submit_accuse(self, mouse, accusation):
        return self.accuse_submit_button.collidepoint(mouse) and None not in accusation.values()

    def skip_accuse(self, mouse):
        if self.skip_accuse_button.collidepoint(mouse):
            return True