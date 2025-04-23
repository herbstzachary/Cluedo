import pygame
from pygame import Rect

from Helpers.Colors import BLACK, GREY, GREEN
from Helpers.Enums import TurnPhases

class GameStateInformationArea:

    def __init__(self, area, font, horizontal_text_padding, vertical_text_padding):
        self.area = area
        self.font = font
        self.horizontal_text_padding = horizontal_text_padding
        self.vertical_text_padding = vertical_text_padding

        # Useful to have so we can reference them when checking click locations later
        self.suggest_submit_button = None
        self.accuse_submit_button = None
        self.skip_accuse_button = None

        self.eliminated_player = None

    def draw_info_area(self, player, phase, move_amount, guess, surface):
        if phase == TurnPhases.MOVE:
            text_to_render = player.character.value + " can move up to " + str(move_amount) + " spaces."

            if self.eliminated_player is not None:
                text_to_render = self.eliminated_player.character.value + " was eliminated. " + text_to_render

            move_text = self.font.render(text_to_render, True, BLACK)
            move_text_rect = move_text.get_rect()
            move_text_rect.center = self.area.center
            outline = Rect(
                move_text_rect.left - self.horizontal_text_padding,
                move_text_rect.top - self.vertical_text_padding,
                move_text_rect.width + (2 * self.horizontal_text_padding),
                move_text_rect.height + (2 * self.vertical_text_padding)
            )

            pygame.draw.rect(surface, GREY, outline)
            pygame.draw.rect(surface, BLACK, outline, width=1)
            surface.blit(move_text, move_text_rect)
        elif phase == TurnPhases.SUGGEST:
            suggest_text = self.font.render("Submit suggestion for " + player.character.value, True, BLACK)
            self.suggest_submit_button = suggest_text.get_rect()
            self.suggest_submit_button.center = self.area.center

            button_rect = Rect(
                self.suggest_submit_button.left - self.horizontal_text_padding,
                self.suggest_submit_button.top - self.vertical_text_padding,
                self.suggest_submit_button.width + (2 * self.horizontal_text_padding),
                self.suggest_submit_button.height + (2 * self.vertical_text_padding)
            )
            border_radius = int(button_rect.width / 2)

            if None in guess.values():
                pygame.draw.rect(surface, GREY, button_rect, border_radius=border_radius)
            else:
                pygame.draw.rect(surface, GREEN, button_rect, border_radius=border_radius)
            pygame.draw.rect(surface, BLACK, button_rect, width=1, border_radius=border_radius)

            surface.blit(suggest_text, self.suggest_submit_button)
        else:
            submit_accuse_text = self.font.render("Submit accusation for " + player.character.value, True, BLACK)
            self.accuse_submit_button = submit_accuse_text.get_rect()
            self.accuse_submit_button.right = self.area.centerx - self.horizontal_text_padding
            self.accuse_submit_button.top = self.area.top

            submit_button_rect = Rect(
                self.accuse_submit_button.left - self.horizontal_text_padding,
                self.accuse_submit_button.top - self.vertical_text_padding,
                self.accuse_submit_button.width + (2 * self.horizontal_text_padding),
                self.accuse_submit_button.height + (2 * self.vertical_text_padding)
            )
            submit_border_radius = int(submit_button_rect.width / 2)

            skip_accuse_text = self.font.render("Skip Accuse Phase for " + player.character.value, True, BLACK)
            self.skip_accuse_button = skip_accuse_text.get_rect()
            self.skip_accuse_button.left = submit_button_rect.right + (2 * self.horizontal_text_padding)
            self.skip_accuse_button.top = self.area.top

            skip_button_rect = Rect(
                self.skip_accuse_button.left - self.horizontal_text_padding,
                self.skip_accuse_button.top - self.vertical_text_padding,
                self.skip_accuse_button.width + (2 * self.horizontal_text_padding),
                self.skip_accuse_button.height + (2 * self.vertical_text_padding)
            )
            skip_border_radius = int(submit_button_rect.width / 2)

            if None in guess.values():
                pygame.draw.rect(surface, GREY, submit_button_rect, border_radius=submit_border_radius)
            else:
                pygame.draw.rect(surface, GREEN, submit_button_rect, border_radius=submit_border_radius)
            pygame.draw.rect(surface, BLACK, submit_button_rect, width=1, border_radius=submit_border_radius)
            surface.blit(submit_accuse_text, self.accuse_submit_button)

            pygame.draw.rect(surface, GREEN, skip_button_rect, border_radius=skip_border_radius)
            pygame.draw.rect(surface, BLACK, skip_button_rect, width=1, border_radius=skip_border_radius)
            surface.blit(skip_accuse_text, self.skip_accuse_button)

    def submit_guess(self, mouse, suggestion):
        return self.suggest_submit_button.collidepoint(mouse) and None not in suggestion.values()

    def submit_accuse(self, mouse, accusation):
        return self.accuse_submit_button.collidepoint(mouse) and None not in accusation.values()

    def skip_accuse(self, mouse):
        if self.skip_accuse_button.collidepoint(mouse):
            return True