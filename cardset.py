from typing import List
from card import Card
# TODO: how to handle [H2, D2, C5, C6]?
# TODO: How to sort cards when there is a wildcard present? Multiple wildcards?
# TODO: Solution will be much easier if player is required to input the 'hidden' attrs
# of a replacement card

class CardSet:
    '''A card set is a list of card objects. The class is used for
    recording data about sets of cards submitted by players'''

    def wc_is_present(self):
        bools = [card.is_wildcard for card in self.cards]
        wc_is_present = any(bools)
        return(wc_is_present)

    def n_wc(self):
        '''Returns number of wildcards in the current cardset. Call only if wc_is_present.'''
        bools = [card.is_wildcard for card in self.cards]
        n_wc = sum(bools)
        return(n_wc)
    
    def cards_are_consecutive(self) -> bool:
        '''Returns True if each card.hidden_int_value is adjacent to one another.'''
        bools = (self.cards[idx].adjacent(self.cards[idx+1]) for idx, card in enumerate(self.cards) 
                        if card != self.cards[-1]) # if statement for avoiding index out of range error
        cards_are_consecutive = all(bools) 
        return(cards_are_consecutive)

    def cards_are_same_rank(self) -> bool:
        '''Returns True if each card.hidden_rank is the same.'''
        n_ranks = len(set([card.hidden_rank for card in self.cards]))
        only_one_rank = (n_ranks == 1)
        return(only_one_rank)

    def cards_are_same_suit(self) -> bool:
        '''Returns True if each card.hidden_suit is the same.'''
        n_suits = len(set([card.hidden_suit for card in self.cards]))
        only_one_suit = (n_suits == 1)
        return(only_one_suit)

    def get_card_ids(self):
        card_ids = [card.id for card in self.cards]
        return(card_ids)

    def get_points(self):
        if self.cards:
            points = sum([card.points for card in self.cards])
            return(points)
        else:
            return(0)

    def __init__(self, cards: List[object]):
        '''cards: list of card objects'''
        if not isinstance(cards, list):
            cards = [cards] # ensures that single card instances 
                            # can be considered as card set instances
        if cards:
            self.cards = cards
            self.card_ids = self.get_card_ids()
            self.wc_is_in_cards = self.wc_is_present()
            self.number_of_wc = self.n_wc() if self.wc_is_in_cards else None
            self.consecutive = self.cards_are_consecutive()
            self.same_rank = self.cards_are_same_rank()
            self.same_suit = self.cards_are_same_suit()

    def __eq__(self, other_set):
        if isinstance(other_set, CardSet):
            return(self.cards == other_set.cards)
            # reminder: cards are considered equal if their hidden attrs are equal

    def __len__(self):
        return(len(self.cards))

    def __repr__(self):
        return(self.cards)

    def __str__(self):
        txt_lst = [str(card) for card in self.cards]
        txt = ', '.join(txt_lst)
        return(txt)

    def sort_cards(self):
        self.cards.sort(key = lambda card: (card.hidden_int_value, card.hidden_suit))
        self.card_ids = self.get_card_ids()

    def append(self, item):
        if isinstance(item, Card):
            self.cards.append(item)
            self.sort_cards()
        elif isinstance(item, CardSet):
            self.cards.append(item.cards)
            self.sort_cards()

    def extend(self, item):
        if isinstance(item, CardSet):
            self.cards.extend(item.cards)
            self.sort_cards()

    def isin(self, parent_set: object):
        '''Returns True if each card in self.cards is in parent_set.cards'''
        all_in_parent_set = all(card in parent_set.cards for card in self.cards)
        return(all_in_parent_set)

    def remove(self, item):
        if isinstance(item, Card):
            self.cards = [card for card in self.cards if card != item]
            self.sort_cards()
        elif isinstance(item, CardSet):
            self.cards = [card for card in self.cards if not card.isin(item)]
            self.sort_cards()

    def contains(self, child_set: object):
        '''Returns True if self.cards contains each card in child_set.cards'''
        if not isinstance(child_set, CardSet):
            child_set = CardSet(child_set)
        contains_child_set = (all(card in self.cards for card in child_set.cards))
        return(contains_child_set)
    
    def can_stand_alone(self):
        '''Verify that the card set can stand by itself (i.e., does not depend
        on card sets existing on the table). The card set instance can stand by
        itself if the following conditions are met:
            1) there are at least three cards;
            2) all cards have the same_hidden rank OR the cards have the same suit 
                and are consecutive'''
        min_number_of_cards = 3
        if len(self) < min_number_of_cards:
            return(False)
        elif self.cards_are_same_rank():
            return(True)
        elif self.cards_are_same_suit():
            return(self.cards_are_consecutive())
        else:
            return(False)

    def assign_wc_attrs_to_cardset(self):
        '''Loop through a cardset and assign wildcard attrs to all
        wildcards'''
        for card in self.cards:
            if card.is_wildcard:
                card.assign_wildcard_attrs()

    def reset_wc_attrs_in_cardset(self):
        '''Loop through a cardset and reset all wildcard attrs'''
        for card in self.cards:
            if card.is_wildcard:
                card.reset_wildcard_attrs()
        