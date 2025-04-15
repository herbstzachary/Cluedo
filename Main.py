#Imports
import random

import pygame, sys
from pygame.locals import *

import Enums
from Board import Board
from GameplayHelpers import create_deck, create_hands, check_suggestion
from PlayerPlayArea import PlayerPlayArea
from Enums import Characters, Rooms, Weapons, TurnPhases, TileTypes
from Player import Player

# Initializing
pygame.init()

NUMBER_OF_TILES = 26
screenInfo = pygame.display.Info()
SCREEN_WIDTH = screenInfo.current_w
SCREEN_HEIGHT = screenInfo.current_h
DISPLAY_SURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

solution = [
    list(Characters)[random.randint(0, len(Characters) - 1)],
    list(Rooms)[random.randint(0, len(Rooms) - 1)],
    list(Weapons)[random.randint(0, len(Weapons) - 1)]
]

deck = create_deck(solution)
random.shuffle(deck)

player_hands = create_hands(deck, 6)

board_font = pygame.font.SysFont('Comic Sans MS', int((40 * SCREEN_HEIGHT) / 1600))
player_font = pygame.font.SysFont('Comic Sans MS', int((40 * SCREEN_HEIGHT) / 1600))
card_font = pygame.font.SysFont('Comic Sans MS', int((20 * SCREEN_HEIGHT) / 1600))

board = Board(SCREEN_WIDTH, SCREEN_HEIGHT, NUMBER_OF_TILES, board_font)
players = [
    Player(Characters.SCARLET, Color("darkred"), board.board[24][8], player_hands[0]),
    Player(Characters.MUSTARD, Color("yellow3"),board.board[17][1], player_hands[1]),
    Player(Characters.WHITE, Color("white"),board.board[0][10], player_hands[2]),
    Player(Characters.GREEN, Color("forestgreen"), board.board[0][15], player_hands[3]),
    Player(Characters.PEACOCK, Color("mediumblue"), board.board[6][24], player_hands[4]),
    Player(Characters.PLUM, Color("purple4"), board.board[19][24], player_hands[5])
]
board.players = players

player_area = PlayerPlayArea(player_font, card_font, 0, SCREEN_WIDTH / 2)
current_player = players[0]
board.draw_board_state(DISPLAY_SURF)
current_player_phase = TurnPhases.MOVE
move_number = random.randint(1, 6) + random.randint(1, 6)
board.get_move_candidates(current_player.current_tile, move_number)

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if current_player_phase == TurnPhases.MOVE:
                valid_move = board.move_player_if_valid(current_player, pos)
                if valid_move:
                    if current_player.current_tile.tile_type == TileTypes.ROOM:
                        current_player_phase = TurnPhases.SUGGEST
                        player_area.current_suggestion[Enums.Rooms] = board.get_room_for_tile(current_player.current_tile)
                    else:
                        current_player_phase = TurnPhases.ACCUSE
            elif current_player_phase == TurnPhases.SUGGEST:
                player_area.select_cards_for_guess(pos)
                if player_area.submit_guess(pos):
                    suggestion = player_area.current_suggestion
                    new_knowledge = check_suggestion(players, current_player, suggestion)

                    if new_knowledge is not None:
                        player_area.player_that_revealed_info = new_knowledge[0]
                        current_player.add_knowledge(new_knowledge[1])

                    current_player_phase = TurnPhases.ACCUSE
                    player_area.clear_suggestion()
            elif current_player_phase == TurnPhases.ACCUSE:
                if player_area.skip_accuse(pos):
                    player_area.player_that_revealed_info = -1
                    index = players.index(current_player)
                    if index == len(players) - 1:
                        current_player = players[0]
                    else:
                        current_player = players[index + 1]
                    current_player_phase = TurnPhases.MOVE
                    move_number = random.randint(1, 6) + random.randint(1, 6)
                    board.get_move_candidates(current_player.current_tile, move_number)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAY_SURF.fill(Color("white"))
    board.draw_board_state(DISPLAY_SURF)
    player_area.draw_player_play_area(current_player, current_player_phase, DISPLAY_SURF)
    pygame.display.update()
