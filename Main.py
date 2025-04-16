#Imports
import random

import pygame, sys
from pygame.locals import *

import Enums
from Board import Board
from GameplayHelpers import create_deck, create_hands, check_suggestion, get_next_player, get_active_players
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
game_over = False

while not game_over:
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
                advance = False
                player_area.select_cards_for_accusation(pos)
                if player_area.submit_accuse(pos):
                    advance = True
                    accusation = player_area.current_suggestion
                    is_correct = True
                    for clue in accusation.values():
                        if clue not in solution:
                            is_correct = False
                            break

                    if is_correct:
                        game_over = True
                    else:
                        index = players.index(current_player)
                        players[index].active = False
                        current_player.current_tile.occupied = False
                        if len(get_active_players(players)) == 1:
                            game_over = True


                if player_area.skip_accuse(pos):
                    advance = True

                if advance:
                    player_area.player_that_revealed_info = -1
                    player_area.clear_suggestion()
                    current_player = get_next_player(players, current_player)
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

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAY_SURF.fill(Color("white"))

    default_winner = get_active_players(players)
    if len(default_winner) == 1:
        winner_text = pygame.sysfont.SysFont('Comic Sans MS', 60).render("Player " + str(players.index(default_winner[0])) + " is the winner due to everyone else being eliminated!", True, Color("Black"))
    else:
        winner_text = pygame.sysfont.SysFont('Comic Sans MS', 60).render("Player " + str(players.index(current_player)) + " is the winner due to guessing the correct solution!", True, Color("Black"))

    winner_text_rect = winner_text.get_rect()
    winner_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    DISPLAY_SURF.blit(winner_text, winner_text_rect)
    pygame.display.update()

