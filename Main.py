#Imports
import random

import pygame, sys
from pygame.locals import *

from Board import Board
from PlayerPlayArea import PlayerPlayArea
from Enums import Characters
from Player import Player

# Initializing
pygame.init()

NUMBER_OF_TILES = 26
screenInfo = pygame.display.Info()
SCREEN_WIDTH = screenInfo.current_w
SCREEN_HEIGHT = screenInfo.current_h
DISPLAY_SURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

players = [
    Player(Characters.SCARLET, Color("darkred"), (8, 24)),
    Player(Characters.MUSTARD, Color("yellow3"),(1 , 17)),
    Player(Characters.WHITE, Color("white"),(10, 0)),
    Player(Characters.GREEN, Color("forestgreen"), (15, 0)),
    Player(Characters.PEACOCK, Color("mediumblue"), (24, 6)),
    Player(Characters.PLUM, Color("purple4"), (24, 19))
]

board_font = pygame.font.SysFont('Comic Sans MS', 30)
player_font = pygame.font.SysFont('Comic Sans MS', 30)

board = Board(SCREEN_WIDTH, SCREEN_HEIGHT, NUMBER_OF_TILES, players, board_font)
player_area = PlayerPlayArea(player_font, 0, SCREEN_WIDTH / 2)
current_player = 0
board.draw_board_state(DISPLAY_SURF)

while True:
    move_number = random.randint(1, 6) + random.randint(1, 6)
    board.get_move_candidates(players[current_player].current_loc, 4)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            valid_move = board.move_player_if_valid(players[current_player], pos)
            if valid_move:
                if current_player == len(players) - 1:
                    current_player = 0
                else:
                    current_player += 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAY_SURF.fill(Color("white"))
    board.draw_board_state(DISPLAY_SURF)
    player_area.draw_player_play_area(players[current_player], DISPLAY_SURF)
    pygame.display.update()
