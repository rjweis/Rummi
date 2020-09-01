from typing import List

def check_str(user_input: str, acceptable_values: List[str]):
    if user_input not in acceptable_values:
        while True:
            user_input = input('{} is not valid input. Enter one of {}:\n'.format(user_input, acceptable_values))
            if user_input in acceptable_values:
                return(user_input)
    else:
        return(user_input)

class Card:
    _rank_to_int_dict = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'J': 11,
        'Q': 12,
        'K': 13, 
        'A': 14
    }

    _int_to_rank_dict = {
        2: '2',
        3: '3',
        4: '4',
        5: '5',
        6: '6',
        7: '7',
        8: '8', 
        9: '9',
        10: '10',
        11: 'J',
        12: 'Q',
        13: 'K',
        14: 'A'
    }

    _points_dict = {
        '2': 30,
        '3': 5,
        '4': 5,
        '5': 5,
        '6': 5,
        '7': 5,
        '8': 5,
        '9': 5,
        '10': 10,
        'J': 10,
        'Q': 10,
        'K': 10, 
        'A': 20
    }

    def __init__(self, suit_rank: str):
        '''
        suit_rank: 0th character represents the suit, the remaining characters
            represent the rank.

        .hidden_ attributes are those that are used for sorting and evaluating 
        sets of submitted cards. The user will never see these, though; they will 
        only see .suit, .rank. and .id. 
        
        Attributes:
            .int_value: the rank converted to an integer. E.g., J = 11, Q = 12, etc.
                Used for sorting. 
            .is_wildcard_replacing: describes the function of a wildcard. If True,
                .hidden_rank and .hidden_int_value will be assgined the 'replacement'
                value.
            .hidden_rank: used for sorting.
            .hidden_int_value: used for sorting'''
        self.suit = suit_rank[0].upper()
        self.rank = suit_rank[1:].upper()
        self.id = self.suit + self.rank
        self.int_value = self._rank_to_int_dict[self.rank]
        self.points = self._points_dict[self.rank]
        
        self.is_wildcard = True if self.rank == '2' else False
        self.is_wildcard_replacing = False if self.is_wildcard else None 
        self.hidden_rank = self.rank 
        self.hidden_int_value = self.int_value 
        self.hidden_suit = self.suit 

    def __eq__(self, comparison_card: object):
        '''When comparing wildcards:
            Returns True if the rank and suit for each wildcard are equal
        
        When comparing all other cards:
            Returns True if the hidden_rank and hidden_suit from each card
            are equal'''
        if isinstance(comparison_card, Card):
            if self.is_wildcard and comparison_card.is_wildcard:
                same_rank = (self.rank == comparison_card.rank)
                same_suit = (self.suit == comparison_card.suit)
                return(same_rank and same_suit)
            else:
                same_rank = (self.hidden_rank == comparison_card.hidden_rank)
                same_suit = (self.hidden_suit == comparison_card.hidden_suit)
                return(same_rank and same_suit)
        else:
            return(False)
    
    def __repr__(self):
        return(self.id)
        
    def __len__(self):
        return(1)

    def same_suit(self, comparison_card: object) -> bool:
        '''Determines if the card (self) has the same suit as the
        comparison card.
        
        Returns: Bool'''
        if self.hidden_suit and comparison_card.hidden_suit:
            are_suits_same = (self.hidden_suit == comparison_card.hidden_suit)
            return(are_suits_same)

    def same_rank(self, comparison_card: object) -> bool:
        '''Determines if the card (self) has the same rank as the
         comparison card.
        
        Returns: Bool'''
        if self.hidden_suit and comparison_card.hidden_suit:
            are_ranks_same = (self.hidden_rank == comparison_card.hidden_rank)
            return(are_ranks_same)
    
    def adjacent(self, comparison_card: object) -> bool:
        '''Determines if the card rank (self) is adjacent to 
        the rank of the comparison card.
        
        Returns: Bool'''
        # rank '2' and rank 'A' must be considered adjacent
        if self.hidden_rank == '2' and comparison_card.hidden_rank == 'A':
            return(True)

        elif self.hidden_rank == 'A' and comparison_card.hidden_rank == '2':
            return(True)

        elif self.hidden_int_value + 1 == comparison_card.hidden_int_value:
            return(True)

        elif self.hidden_int_value - 1 == comparison_card.hidden_int_value:
            return(True)

        else:
            return(False)

    def between(self, comparison_card1: object, comparison_card2: object) -> bool:
        ''''Determines if the card rank (self) falls immediately between
        two cards (comparison_card1 and comparison_card2). That is, self 
        is adjacent to both comparison_card1 and comparison_card2.
        
        Returns: bool'''
        is_between = (self.adjacent(comparison_card1) and self.adjacent(comparison_card2))
        return(is_between)

    def isin(self, card_set: object):
        '''Returns true if card is contained in the card_set.'''
        cards = card_set.cards
        isincards = any(self == card for card in cards)
        return(isincards)

    def distance(self, comparison_card: object) -> int:
        '''Returns the absolute distance between the self card and the 
        comparison card from their respective int_values. 
        
        Note: does NOT use the hidden_values.'''
        distance = abs(self.int_value - comparison_card.int_value)
        return(distance)

    def assign_wildcard_attrs(self):
        '''Use when a player is adding a wildcard to the table. Function should 
        be called for each wildcard that is played.
        
        If user wants to modify the card, modifies the card object.'''

        yes_no_input = input('Do you want to assign an alternative suit and/or rank '
                            'to {}? Enter yes/no:\n'.format(self))
        yes_no = check_str(yes_no_input, ['yes', 'no'])
        if yes_no == 'yes':
            suit_input = input('Enter the suit you want to assign to the wildcard:\n')
            possible_suits = ['C', 'H', 'D', 'S']
            suit = check_str(suit_input.strip().upper(), possible_suits)
            self.hidden_suit = suit

            rank_input = input('Enter the rank you want to assign to the wildcard:\n')
            possible_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            rank = check_str(rank_input.strip().upper(), possible_ranks)
            self.hidden_rank = rank

            int_value = self._rank_to_int_dict[rank]
            self.hidden_int_value = int_value

    def reset_wildcard_attrs(self):
        self.hidden_suit = self.suit
        self.hidden_rank = self.rank
        self.hidden_int_value = self.int_value