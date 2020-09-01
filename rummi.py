from card import Card
from carddeck import CardDeck
from cardset import CardSet
from discardpile import DiscardPile
from player import Player
from table import Table
from typing import List, Tuple
import userinput
from userinput import UserInput
import logo
# TODO: add the player method .swap_card() to the game
# TODO: make move invalid if player empties their hand -- they must have at least one card remaining

ui = UserInput()
class Rummi:
    def __init__(self, player_names):
        print("Let's start the game!\n")    
        self.deck = CardDeck()
        self.discard_pile = DiscardPile(self.deck)
        self.table = Table()
        self.players = [Player(name, self.deck) for name in player_names]
        self.turn_counter = 0

    def print_score_board(self):
        print('Here is the scoreboard:\n')
        for player in self.players:
            print('{}: {} points'.format(player.name, player.points))

    def draw(self, player: object):
        self.discard_pile.print_info() 
        deck_or_discard_or_all = ui.discard_or_deck_or_all()
        if deck_or_discard_or_all == 'deck':
            print('Drawing card from deck...')
            player.draw_from_deck(self.deck)
        elif deck_or_discard_or_all == 'top':
            print('Drawing from discard pile...')
            player.draw_one_card_from_discard_pile(self.discard_pile)
        elif deck_or_discard_or_all == 'all':
            print('Drawing all cards from discard pile...')
            player.draw_all_cards_from_discard_pile(self.discard_pile)

    def add_cards_player_has_0_points(self, player, table):
        while True:
            if not player.points:
                cards2submit = ui.get_player_cards(player)
                if cards2submit in ['finished', 'stop']:
                    break
                player.make_move_cards_stand_alone(cards2submit, table)
            else:
                cards2submit = ui.get_player_cards(player)
                if cards2submit in ['finished', 'stop']:
                    break
                add_to_target_cards = ui.add_to_target_cards()
                if add_to_target_cards == 'yes':
                    # TODO: Add stop/break option 
                    target_cards = ui.get_target_cards(table)
                    player.make_move_add2target_cards(submitted_cards = cards2submit, target_cards = target_cards, table = self.table)
                else:
                    player.make_move_cards_stand_alone(submitted_cards = cards2submit, table = self.table)

    def add_cards(self, player: object, table: object): 
        while True:
            cards2submit = ui.get_player_cards(player)
            if cards2submit in ['finished', 'stop']:
                break
            add_to_target_cards = ui.add_to_target_cards()
            if add_to_target_cards == 'yes':
                target_cards = ui.get_target_cards(table)
                if target_cards in ['finished', 'stop']:
                    break
                player.make_move_add2target_cards(submitted_card_set = cards2submit, target_card_set = target_cards, table = self.table)
            else:
                player.make_move_cards_stand_alone(submitted_card_set = cards2submit, table = self.table)

    def first_turn(self, player: object): 
        '''On the first turn, players may not add cards to the table'''
        self.draw(player)
        card2discard = ui.get_discard_card(player)
        player.discard(card2discard, self.discard_pile)

    def turn_if_player_has_0_points(self, player: object, table: object):
        '''After the player's first turn, they may add cards to the table. When the player has zero points,
        cards must be submitted on their own; i.e., not to any existing groups of cards on the table.
        Only after the player has earned points is when the player can add to existing groups of cards (which
        is when the turn() method will be called).'''
        print(table)
        self.draw(player)
        add_to_table = ui.add_to_table(table)
        if add_to_table == 'yes':
            self.add_cards_player_has_0_points(player, table)
        print(table)
        player.print_cards()
        card2discard = ui.get_discard_card(player)
        player.discard(card2discard, self.discard_pile)

    def turn(self, player: object, table: object):
        print(table)
        self.draw(player)
        add_to_table = ui.add_to_table(table)
        if add_to_table == 'yes':
            self.add_cards(player, table)
        player.print_cards()
        card2discard = ui.get_discard_card(player)
        player.discard(card2discard, self.discard_pile)

    def reset(self, number_of_starting_cards = 7):
        self.deck = CardDeck()
        self.discard_pile = DiscardPile(self.deck)
        self.table = Table()
        self.turn_counter = 0 
        for player in self.players:
            player.cards = player.get_starting_cards(self.deck, number_of_starting_cards)
            player.submitted_cards = []

def round(game: object):
    '''Round ends when a player has successfully played all their cards.
    
    Param game: Rummi object'''
    winning_condition = False
    while not winning_condition:

        for player in game.players:
            print("\n---------------\nIt's your turn, {}!\n---------------\n".format(player.name))
            player.print_cards()
            if game.turn_counter < 2:
                game.first_turn(player)
            else:
                if not player.submitted_cards:
                    game.turn_if_player_has_0_points(player, game.table)
                else:
                    game.turn(player, game.table)

            winning_condition = (len(player.cards) == 0)
            if winning_condition:
                player.points += 50
                for player in game.players:
                    player.get_net_points()
                print('{} wins the round!'.format(player.name))
                game.print_score_board()
                game.reset()
                break

            game.turn_counter += 1
    
def main():
    print(logo.img)
    player_names = ui.get_player_names()
    SCORE_LIMIT = ui.get_score_limit()
    game = Rummi(player_names)
    max_score = 0

    while max_score < SCORE_LIMIT:
        round(game)
        max_score = max([player.points for player in game.players])
        if max_score < SCORE_LIMIT:
            print('------\nStarting new round...\n------\n')
        
    for player in game.players:
        if player.points == max_score:
            print('{} wins the game! Here is the final score board: '.format(player.name))
            game.print_score_board()

if __name__ == '__main__':
    main()