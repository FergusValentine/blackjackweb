from pydantic import BaseModel, Field
from .blackjack_data import Suits, Ranks

import random

class Card(BaseModel):
    suit: int = 0
    rank: int = 0

class Player(BaseModel):
    hand: list[Card] = Field(default_factory=list)
    count: int

class BlackjackGame(BaseModel):
    deck: list[Card] = Field(default_factory=list)
    player: Player
    dealer: Player
    over: bool = False

def unrevealed_card() -> Card:
    return Card(suit=0, rank=0)

def create_shuffled_deck() -> list[Card]:
    deck = [Card(suit = s, rank = r) for s in Suits for r in Ranks]
    random.shuffle(deck)
    return deck

def draw_card(deck: list[Card]) -> Card:
    return deck.pop()

def count_hand(player: Player) -> None:
    hand_value = 0
    ace_count = 0

    for card in player.hand:
        if card.rank == 1:
            hand_value += 11
            ace_count += 1
        elif card.rank >= 10:
            hand_value += 10
        else:
            hand_value += card.rank

    while hand_value > 21 and ace_count > 0:
        hand_value -= 10
        ace_count -= 1

    player.count = hand_value
    #return hand_value

def is_bust(player: Player) -> bool:
    count_hand(player)
    return player.count >= 21

def hit_action(game: BlackjackGame, player: Player) -> bool:
    if player.count != 21:
        player.hand.append(draw_card(game.deck))
        count_hand(player)

    return is_bust(player)

def new_game() -> BlackjackGame:
    deck: list[Card] = create_shuffled_deck()
    game: BlackjackGame = BlackjackGame(deck=deck, player=Player(hand=[], count=0), dealer=Player(hand=[], count=0))

    for i in range(0,2):
        hit_action(game, game.player)
        hit_action(game, game.dealer)
    return game

def dealer_round(game: BlackjackGame) -> None:
    dealer_hand: list[Card] = game.dealer.hand
    player_hand: list[Card] = game.player.hand

    player_count = game.player.count
    player: Player = game.player
    dealer: Player = game.dealer

    if is_bust(player):
        print(f"player busted at {game.player.count}")
        return

    while dealer.count < 17:
        hit_action(game, dealer)

    if is_bust(dealer):
        print(f"dealer busted at {dealer.count} win")
        return
    elif player_count > dealer.count:
        print(f"player: {player.count}, dealer: {dealer.count}, dealer lost")
        return
    elif player.count == dealer.count:
        print(f"player: {player.count}, dealer: {dealer.count}, draw")
        return
    else:
        print(f"player: {player.count}, dealer: {dealer.count}, player lost")
        return

def process_game(game: BlackjackGame, action: str):
    if game.over:
        return game

    match action:
        case 'hit':
            player_bust: bool = hit_action(game, game.player)
            game.over = player_bust
        case 'stand':
            dealer_round(game)
            game.over = True

    return game

def load_game(json_game: dict) -> BlackjackGame:
    return BlackjackGame(**json_game)

def save_game(game: BlackjackGame):
    return game.model_dump()
