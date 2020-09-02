from typing import List
from cardset import CardSet

class Table:
    '''List of CardSet objects'''
    def __init__(self, card_sets: List[object] = None):
        if card_sets:
            self.cards = card_sets
        else:
            self.cards = []

    def __str__(self):
        if self.cards:
            txt_lst = [str(card) for card in self.cards]
            txt = '\n'.join(txt_lst)
            msg = '\nThe following cards are on the table:\n------\n'
            return(msg + txt + '\n')
        else:
            return('The table is empty')

    def __eq__(self, other_table: object):
        return(self.cards == other_table.cards)

    def add_cards(self, card_set: object):
        '''Add cards to table as an individual set'''
        if isinstance(card_set, CardSet):
            self.cards.append(card_set)
            # TODO: concatenate adjacent card sets 
            # (e.g., [h3, h4, h5] and [h6, h7, h8] should be one set)

    def contains(self, card_set: object): 
        return(any([parent_set == card_set for parent_set in self.cards]))

    def add_cards_to_target_cards(self, added_set: object, target_set: object):
        for idx, parent_set in enumerate(self.cards):
            if parent_set == target_set: 
                parent_set.extend(added_set)
                parent_set.sort_cards()
                self.cards[idx] = parent_set
                # TODO: Organize the table
