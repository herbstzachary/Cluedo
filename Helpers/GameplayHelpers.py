import random

from Helpers.Enums import Characters, Rooms, Weapons


def create_deck(solution):
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


def create_hands(card_deck, number_of_players):
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


def check_suggestion(players, current_player, suggestion):
    index = players.index(current_player) + 1
    if index >= len(players):
        index = 0

    for _ in range(0, len(players)):
        clues_present = []
        for card in suggestion.values():
            if card in players[index].hand:
                clues_present.append(card)
        if len(clues_present) == 0:
            if index >= len(players) - 1:
                index = 0
            else:
                index += 1
        else:
            random.shuffle(clues_present)
            return {clues_present[0]: players[index]}

    return None

def get_next_player(players, current_player):
    index = players.index(current_player) + 1
    for _ in range(len(players)):
        if index >= len(players):
            index = 0

        if players[index].active:
            return players[index]
        else:
            index += 1

def get_active_players(players):
    active_players = []
    for player in players:
        if player.active:
            active_players.append(player)

    return active_players