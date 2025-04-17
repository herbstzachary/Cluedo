import sys

import pygame.sysfont
from pygame import QUIT, Rect

from Colors import WHITE, BLACK


class MainMenu:

    def __init__(self, screen_width, screen_height):
        title_font = pygame.sysfont.SysFont("Times New Roman", 100)
        select_font = pygame.sysfont.SysFont("Times New Roman", 50)
        button_font = pygame.sysfont.SysFont("Times New Roman", 30)

        self.title_text = title_font.render("Cluedo", True, BLACK)
        self.title_text_rect = self.title_text.get_rect()
        self.title_text_rect.center = (screen_width / 2, screen_height / 4)

        self.select_text = select_font.render("Please select the number of players:", True, BLACK)
        self.select_text_rect = self.select_text.get_rect()
        self.select_text_rect.center = (screen_width / 2, screen_height / 2)

        self.buttons = []
        x_margin = screen_width / 100
        left_x = x_margin
        middle_y = (screen_height * 3) / 4
        button_width = (screen_width - (x_margin * 2)) / 5
        button_height = screen_height / 4

        for i in range(2, 7):
            outline_rect = Rect(
                left_x,
                screen_height - button_height - x_margin,
                button_width,
                button_height)

            button_text = button_font.render(str(i), True, BLACK)
            rect = button_text.get_rect()
            rect.center = outline_rect.center
            self.buttons.append((button_text, rect, outline_rect))
            left_x = outline_rect.right

    def run_main_menu(self, surface):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button[2].collidepoint(pos):
                            return self.buttons.index(button) + 2

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            surface.fill(WHITE)
            surface.blit(self.title_text, self.title_text_rect)
            surface.blit(self.select_text, self.select_text_rect)
            for button in self.buttons:
                surface.blit(button[0], button[1])
                pygame.draw.rect(surface, BLACK, button[2], width=1)
            pygame.display.update()
