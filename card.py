from typing import List

def check_str(user_input: str, acceptable_values: List[str]) -> str:
    '''Helper function for ensuring that user_input is a str listed 
    in acceptable_values. If not, use loop to keep requesting user_input 
    until it is a str listed in acceptable_values.
    
    Args:
        user_input: Str passed in from the built-in input() function.
        acceptable_values: The values that user_input may take.

    Returns:
        user_input: Str that is in accetable_values.
    '''
    if user_input not in acceptable_values:
        while True:
            user_input = input('{} is not valid input. Enter one of {}:\n'.format(user_input, acceptable_values))
            if user_input in acceptable_values:
                return(user_input)
    else:
        return(user_input)

class Card:
    '''Object that is used to form the CardSet, Deck, and DiscardPile classes.'''

    # dictionaries for mapping ranks and ints, where ints represent the numeric
    # value assigned to a rank. E.g., a rank of '3' corresponds to an int of 3, 
    # a rank of 'Q' corresponeds to an int of 12, etc.
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

    # dictionary for mapping points to each rank
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
        Args:
            suit_rank: 0th character represents the suit, the remaining characters
            represent the rank.
        
        Attrs:
            suit: Suit of the card. Should be one of 
                'H', 'C', 'A', 'D'
                for hearts, clubs, ace, and diamonds, respectively.
            rank: Rank of the card.
            id: The __repr__ of the card, which is suit + rank.
            int_value: the rank converted to an integer. E.g., J = 11, Q = 12, etc.
                Used for sorting. 
            points: Int representing how many points the card is worth.
            is_wildcard: Bool where True indicates that the card is a wildcard. 
                A card is a wildcard if its rank is '2'. 
            hidden_rank: used for sorting when wildcard is present.
            hidden_int_value: used for sorting when wildcard is present.
            hidden_suit: used for sorting when wildcard is present.

        Hidden attributes (hidden_rank, hidden_int_value, hidden_suit) are used for 
        sorting and evaluating sets of submitted cards when there is a wildcard present. 
        The user will never see these hidden atrs; they will only see the id 
        (which is simply suit + rank).

        Note on wildcards:
            Wildcards can be played next to any card. When they are submitted, they take on
            the rank and suit that correspond to making the move valid. For example, if
            ['H3', 'D2', 'H5'] are played, then the corresponding hidden attrs for 'D2'
            are 'H' and '4', respectively. If another player has the actual card H4, they may 
            steal this card from the table by swapping the actual card with the wildcard.
        '''
        self.suit = suit_rank[0].upper()
        self.rank = suit_rank[1:].upper()
        self.id = self.suit + self.rank
        self.int_value = self._rank_to_int_dict[self.rank]
        self.points = self._points_dict[self.rank]
        
        self.is_wildcard = True if self.rank == '2' else False
        self.hidden_rank = self.rank 
        self.hidden_int_value = self.int_value 
        self.hidden_suit = self.suit 

    def __eq__(self, comparison_card: object) -> bool:
        '''Wildcards are considered equal when both ranks and suits are equal.
        All other cards are considered euqal when both their hidden ranks and suits
        are equal.
        
        Args:
            comparison_card: The object that the self object is being compared to. 
        '''
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

        Args:
            comparison_card: The object the self object is being compared to.
        '''
        are_suits_same = (self.hidden_suit == comparison_card.hidden_suit)
        return(are_suits_same)

    def same_rank(self, comparison_card: object) -> bool:
        '''Determines if the card (self) has the same rank as the
         comparison card.
        
        Args:
            comparison_card: The object the self object is being compared to.
        '''
        are_ranks_same = (self.hidden_rank == comparison_card.hidden_rank)
        return(are_ranks_same)
    
    def adjacent(self, comparison_card: object) -> bool:
        '''Determines if the card rank (self) is adjacent to the 
        rank of the comparison card. Cards are considered adjacent when
        1) the absolute value of the difference between the hidden_int_value 
        is equal to 1; OR 2) the self object and the comparison_card have ranks
        '2' and 'A'.
        
        Args:
            comparison_card: The object the self object is being compared to.
        '''
        # rank '2' and rank 'A' must be considered adjacent
        if self.hidden_rank == '2' and comparison_card.hidden_rank == 'A':
            return(True)
        elif self.hidden_rank == 'A' and comparison_card.hidden_rank == '2':
            return(True)

        elif abs(self.hidden_int_value - comparison_card.hidden_int_value) == 1:
            return(True)

        else:
            return(False)

    def isin(self, card_set: object) -> bool:
        '''Returns True if card is contained in the card_set.
        
        Args:
            card_set: Object that contains a list of card objects.
        '''
        cards = card_set.cards
        isincards = any(self == card for card in cards)
        return(isincards)

    def assign_wildcard_attrs(self):
        '''Method is called for each wilcard that is submitted to the table. 
        If the user chooses to modify the card, then they may input the suit
        and rank to assign to the wildcard's hidden attrs.
        '''
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
        '''Called when a player assigns hidden attrs to a wildcard
        that lead to an invalid move. For example, H2 takes on its 
        original suit ('H') and rank ('2').
        '''
        self.hidden_suit = self.suit
        self.hidden_rank = self.rank
        self.hidden_int_value = self.int_value