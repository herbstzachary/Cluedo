#Imports
import random

import pygame, sys
from pygame.locals import *

from Board import Board
from PlayerPlayArea import PlayerPlayArea
from Enums import Characters, Rooms, Weapons, TurnPhases
from Player import Player

def __create_deck(solution):
    deck = []
    for character in list(Characters):
        if character not in solution:
            deck.append(character)

    for room in list(Rooms):
        if room not in solution:
            deck.append(room)

    for weapon in list(Weapons):
        if weapon not in solution:
            deck.append(weapon)

    return deck

def __create_hands(card_deck, number_of_players):
    hands = []
    each_player_gets = int(len(card_deck) / number_of_players)
    current_card = 0
    for _ in range(number_of_players):
        hand = []
        for i in range(current_card, current_card + each_player_gets):
            hand.append(card_deck[i])
        current_card = current_card + each_player_gets
        hands.append(hand)

    for i in range(current_card, len(card_deck)):
        for hand in hands:
            hand.append(card_deck[i])

    return hands

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

deck = __create_deck(solution)
random.shuffle(deck)

player_hands = __create_hands(deck, 6)

board_font = pygame.font.SysFont('Comic Sans MS', 30)
player_font = pygame.font.SysFont('Comic Sans MS', 30)
card_font = pygame.font.SysFont('Comic Sans MS', 15)

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
current_player = 0
board.draw_board_state(DISPLAY_SURF)
current_player_phase = TurnPhases.MOVE
move_number = random.randint(1, 6) + random.randint(1, 6)
board.get_move_candidates(players[current_player].current_tile, move_number)

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if current_player_phase == TurnPhases.MOVE:
                valid_move = board.move_player_if_valid(players[current_player], pos)
                if valid_move:
                    current_player_phase = TurnPhases.SUGGEST
            elif current_player_phase == TurnPhases.SUGGEST:
                player_area.select_cards_for_guess(pos)
                current_player_phase = TurnPhases.ACCUSE
            elif current_player_phase == TurnPhases.ACCUSE:
                if current_player == len(players) - 1:
                    current_player = 0
                else:
                    current_player += 1
                current_player_phase = TurnPhases.MOVE
                move_number = random.randint(1, 6) + random.randint(1, 6)
                board.get_move_candidates(players[current_player].current_tile, move_number)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAY_SURF.fill(Color("white"))
    board.draw_board_state(DISPLAY_SURF)
    player_area.draw_player_play_area(players[current_player], current_player_phase, DISPLAY_SURF)
    pygame.display.update()
