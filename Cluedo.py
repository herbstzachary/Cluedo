#Imports
import random

import pygame, sys
from pygame.locals import *

from Helpers import Enums
from Helpers.Colors import *
from Board.GameBoard import GameBoard
from Helpers.GameplayHelpers import create_deck, create_hands, check_suggestion, get_next_player, get_active_players
from MiscScreens.GameStateInformationArea import GameStateInformationArea
from MiscScreens.MainMenu import MainMenu
from Player.PlayerArea import PlayerArea
from Helpers.Enums import Characters, Rooms, Weapons, TurnPhases, TileTypes
from Player.Player import Player

# Initializing
pygame.init()

NUMBER_OF_TILES_IN_ROW = 26
DISPLAY_SURF = pygame.display.set_mode()
SCREEN_WIDTH, SCREEN_HEIGHT = DISPLAY_SURF.get_size()
x_margin = SCREEN_WIDTH / 100
y_margin = SCREEN_HEIGHT / 100
horizontal_text_padding = SCREEN_WIDTH / 200
vertical_text_padding = SCREEN_HEIGHT / 200

main_menu = MainMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
number_of_players = main_menu.run_main_menu(DISPLAY_SURF)

solution = [
    list(Characters)[random.randint(0, len(Characters) - 1)],
    list(Rooms)[random.randint(0, len(Rooms) - 1)],
    list(Weapons)[random.randint(0, len(Weapons) - 1)]
]

deck = create_deck(solution)
random.shuffle(deck)

player_hands = create_hands(deck, number_of_players)

board_font = pygame.font.Font("./resources/FuturaRenner-Regular.otf", int((40 * SCREEN_HEIGHT) / 1600))
player_font = pygame.font.SysFont('Comic Sans MS', int((40 * SCREEN_HEIGHT) / 1600))
card_font = pygame.font.SysFont('Comic Sans MS', int((20 * SCREEN_HEIGHT) / 1600))

# Upper portion of game screen
info_area = GameStateInformationArea(
    Rect(
        x_margin,
        y_margin,
        SCREEN_WIDTH - (2 * x_margin),
        player_font.get_linesize() + (vertical_text_padding * 2)
    ),
    player_font,
    horizontal_text_padding,
    vertical_text_padding
)

# Left hand side of screen, below information area
player_area = PlayerArea(
    Rect(
        x_margin,
        info_area.area.bottom + y_margin,
        (SCREEN_WIDTH / 2) - (x_margin * 2),
        SCREEN_HEIGHT - info_area.area.bottom - (2 * y_margin)
    ),
    card_font
)

# Right hand side of screen, below information area
board = GameBoard(
    Rect(
        player_area.area.right + (2 * x_margin),
        info_area.area.bottom + y_margin,
        player_area.area.width,
        player_area.area.height
    ),
    NUMBER_OF_TILES_IN_ROW,
    board_font
)

players = [
    Player(Characters.SCARLET, CHARACTER_SCARLET, board.board[24][8]),
    Player(Characters.MUSTARD, CHARACTER_MUSTARD, board.board[17][1]),
    Player(Characters.WHITE, CHARACTER_WHITE,board.board[0][10]),
    Player(Characters.GREEN, CHARACTER_GREEN, board.board[0][15]),
    Player(Characters.PEACOCK, CHARACTER_PEACOCK, board.board[6][24]),
    Player(Characters.PLUM, CHARACTER_PLUM, board.board[19][24])
]
random.shuffle(players)
while len(players) > number_of_players:
    players.pop()

hand_index = 0
for player in players:
    player.set_hand(player_hands[hand_index])
    hand_index += 1

board.players = players

current_player = players[0]
board.draw_board_state(DISPLAY_SURF)
current_player_phase = TurnPhases.MOVE
move_number = random.randint(1, 6) + random.randint(1, 6)
board.get_move_candidates(current_player.current_tile, move_number)
game_over = False

wood = pygame.image.load("./resources/wood.jpeg")
wood = pygame.transform.scale(wood, (SCREEN_WIDTH, SCREEN_HEIGHT))

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if current_player_phase == TurnPhases.MOVE:
                valid_move = board.move_player_if_valid(current_player, pos)
                if valid_move:
                    info_area.eliminated_player = None
                    if current_player.current_tile.tile_type == TileTypes.ROOM:
                        current_player_phase = TurnPhases.SUGGEST
                        player_area.current_suggestion[
                            Enums.Rooms] = board.get_room_for_tile(current_player.current_tile)
                    else:
                        current_player_phase = TurnPhases.ACCUSE
            elif current_player_phase == TurnPhases.SUGGEST:
                player_area.select_card_for_guess(pos, current_player_phase)
                if info_area.submit_guess(pos, player_area.current_suggestion):
                    suggestion = player_area.current_suggestion

                    if current_player not in player_area.room_cards.get(suggestion.get(Rooms)).guessed:
                        player_area.room_cards.get(suggestion.get(Rooms)).guessed.append(current_player)

                    if current_player not in player_area.weapon_cards.get(suggestion.get(Weapons)).guessed:
                        player_area.weapon_cards.get(suggestion.get(Weapons)).guessed.append(current_player)

                    if current_player not in player_area.character_cards.get(suggestion.get(Characters)).guessed:
                        player_area.character_cards.get(suggestion.get(Characters)).guessed.append(current_player)

                    new_knowledge = check_suggestion(players, current_player, suggestion)

                    if new_knowledge is not None:
                        current_player.add_knowledge(new_knowledge)

                    current_player_phase = TurnPhases.ACCUSE
                    player_area.clear_suggestion()
            elif current_player_phase == TurnPhases.ACCUSE:
                advance = False
                player_area.select_card_for_guess(pos, current_player_phase)
                if info_area.submit_accuse(pos, player_area.current_suggestion):
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
                        info_area.eliminated_player = current_player
                        if len(get_active_players(players)) == 1:
                            game_over = True


                if info_area.skip_accuse(pos):
                    advance = True

                if advance:
                    info_area.player_that_revealed_info = None
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

    DISPLAY_SURF.fill(WHITE)
    DISPLAY_SURF.blit(wood, wood.get_rect())
    board.draw_board_state(DISPLAY_SURF)
    player_area.draw_player_play_area(current_player, current_player_phase, move_number, DISPLAY_SURF)
    info_area.draw_info_area(current_player, current_player_phase, move_number, player_area.current_suggestion, DISPLAY_SURF)
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

    DISPLAY_SURF.fill(WHITE)

    default_winner = get_active_players(players)
    if len(default_winner) == 1:
        winner_text = pygame.sysfont.SysFont('Comic Sans MS', 50).render(default_winner[0].character.value + " is the winner due to everyone else being eliminated!", True, BLACK)
    else:
        winner_text = pygame.sysfont.SysFont('Comic Sans MS', 50).render(current_player.character.value + " is the winner due to guessing the correct solution!", True, BLACK)

    winner_text_rect = winner_text.get_rect()
    winner_text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    DISPLAY_SURF.blit(winner_text, winner_text_rect)
    pygame.display.update()

