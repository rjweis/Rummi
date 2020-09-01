import random 
import copy
from cardset import CardSet
from typing import List
from userinput import check_str
from userinput import _rank_to_int_dict
from userinput import UserInput
from table import Table

class Player:
    def _draw_from_deck(self, card_deck: object):
        selected_card = random.choice(card_deck.cards)
        card_deck.cards.remove(selected_card)
        return(selected_card)

    def get_starting_cards(self, card_deck: object, number_of_starting_cards: int):
        unsorted_cards = [self._draw_from_deck(card_deck) for _ in range(number_of_starting_cards)]
        starting_cards = CardSet(unsorted_cards)
        starting_cards.sort_cards()
        return(starting_cards)

    def print_cards(self):
        print("You have the following cards:\n{}\n".format(self.cards.get_card_ids()))

    def __init__(self, name: str, card_deck: object, number_of_starting_cards = 7):
        '''self.cards = CardSet = list of card objects'''
        self.name = name
        self.cards = self.get_starting_cards(card_deck, number_of_starting_cards)
        self.points = 0
        self.submitted_cards = [] # used for keeping track of points at the end of each round
    
    def draw_from_deck(self, card_deck: object):
        selected_card = random.choice(card_deck.cards)
        card_deck.cards.remove(selected_card)
        self.cards.append(selected_card)
        self.cards.sort_cards()
        print('{} was drawn from the deck.\n'.format(selected_card.id))
        self.print_cards() 

    def has_cards(self, cards: object):
        '''Returns true if player has the passed cards. Argument cards 
        can be either an instance of Card or CardSet.'''
        return(self.cards.contains(cards))
    
    def discard(self, card: object, discard_pile: object):
        self.cards.remove(card)
        discard_pile.cards.append(card)
        self.print_cards()
        discard_pile.print_info()

    def draw_one_card_from_discard_pile(self, discard_pile: object):
        top_card_from_discard_pile = discard_pile.cards.pop()
        print('Adding {} to {}...\n'.format(top_card_from_discard_pile, self.name))
        self.cards.append(top_card_from_discard_pile)
        self.cards.sort_cards()
        discard_pile.print_info()
        self.print_cards()

    def draw_all_cards_from_discard_pile(self, discard_pile: object):
        discard_to_card_set = CardSet([card for card in discard_pile.cards])
        self.cards.extend(discard_to_card_set)
        self.cards.sort_cards()
        discard_pile.cards = []
        discard_pile.print_info()
        self.print_cards()

    def get_net_points(self):
        '''Method will be called at the end of each round'''
        points_gained = sum([card_set.get_points() for card_set in self.submitted_cards])
        points_lost = self.cards.get_points()
        net_points = points_gained - points_lost
        self.points += net_points

    def make_move_cards_stand_alone(self, submitted_card_set: object, table: object):
        '''Cards submitted with this method must stand alone, meaning that they cannot be added to 
        existing groups on the table.'''
        # TODO: assign WC attrs if WC
        player_has_cards = self.cards.contains(submitted_card_set)
        if player_has_cards:
            submitted_card_set.assign_wc_attrs_to_cardset()
            cards_can_stand_alone = submitted_card_set.can_stand_alone()
            if cards_can_stand_alone:
                self.cards.remove(submitted_card_set)
                print('Adding {} to the table...'.format(submitted_card_set))
                table.add_cards(submitted_card_set)
                print(table)
                self.submitted_cards.append(submitted_card_set)
            else:
                print('Error: {} is not a valid move.'.format(submitted_card_set))
                submitted_card_set.reset_wc_attrs_in_cardset()
        else:
            print("Error: {} is not in {}'s hand.".format(submitted_card_set, self.name))

    def make_move_add2target_cards(self, submitted_card_set: object, target_card_set: object, table: object):
        player_has_cards = self.cards.contains(submitted_card_set)
        target_cards_on_table = table.contains(target_card_set)
        if player_has_cards and target_cards_on_table:
            submitted_card_set.assign_wc_attrs_to_cardset()
            evaluation_set = copy.deepcopy(submitted_card_set)
            evaluation_set.extend(target_card_set) # for evaluating if the move is valid
            cards_can_be_added = evaluation_set.can_stand_alone()
            if cards_can_be_added:
                self.cards.remove(submitted_card_set)
                print('Adding {} to {}...'.format(submitted_card_set, target_card_set))
                table.add_cards_to_target_cards(submitted_card_set, target_card_set)
                print(table)
                self.submitted_cards.append(submitted_card_set)
            else:
                print('Error: {} is not a valid move.'.format(submitted_card_set))
                submitted_card_set.reset_wc_attrs_in_cardset()
        else:
            print('Error: Cards from the player or the table are missing.')

    def swap_cards(self, card2table: str, card2hand: str, table: object):
        # TODO
        pass

    
if __name__ == '__main__':
    from carddeck import CardDeck
    deck = CardDeck()
    table = Table()
    p1 = Player('p1', deck)
    p1.print_cards()
    for _ in range(5):
        p1.draw_from_deck(deck)
    
    ui = UserInput()
    cards2submit = ui.get_player_cards(p1)
    p1.make_move_cards_stand_alone(cards2submit, table)

