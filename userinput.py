from typing import List
from card import Card
from cardset import CardSet

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

def input_to_card(input: str) -> object:
    ''''Transforms user input string into a card object'''
    card = Card(input.strip())
    return(card)

def input_to_card_set(input: str):
    '''Transforms user input string into a cardset object'''
    if input == 'finished':
        return('finished')
    card_strings = input.strip().split(', ')
    card_lst = [Card(cs) for cs in card_strings]
    card_set = CardSet(card_lst)
    return(card_set)

def check_str(user_input: str, acceptable_values: List[str]):
    user_input = user_input.strip().lower()
    if user_input not in acceptable_values:
        while True:
            user_input = input('{} is not valid input. Enter one of {}:\n'.format(user_input, acceptable_values))
            user_input = user_input.strip().lower()
            if user_input in acceptable_values:
                return(user_input)
    else:
        return(user_input)

def check_int(user_input: str):
    while not user_input.strip().isdigit():
        user_input = input('Unable to process {}. Please enter a number:\n'.format(user_input))
    return(int(user_input))

def verify_is_not_list(input: str):
    '''Checks if user input is list. (If it is a list, that means the user 
    is trying to submit more than one card.) If list, keep asking the user 
    for input until they are only submitting one card.'''
    input_is_list = len(input.split(', ')) > 1
    while input_is_list:
        input = input('Error: You tried to submit more than one card. Try again:\n')
        input_is_list = len(input.split(', ')) > 1
    return(input)

def verify_is_card(input: str):
    acceptable_card_lens = [2, 3]
    if len(input) in acceptable_card_lens:
        suit = input[0].upper()
        acceptable_suits = ['S', 'D', 'H', 'C']
        if suit in acceptable_suits:
            rank = input[1:].upper()
            acceptable_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            if rank in acceptable_ranks:
                return(input)
    else:  
        raise Exception('Input is not a card. Try again.')

def discard_card_from_user_input() -> object: 
    ''''Returns card object from user input.'''
    while True:
        try:
            card2discard = input('Enter the card you want to discard: ')
            card2discard = verify_is_not_list(card2discard)
            card2discard = verify_is_card(card2discard)
            card_obj = input_to_card(card2discard)
            return(card_obj)
        except:
            print('{} is invalid input. Try again.'.format(card2discard))
            pass

def cards2submit_from_user_input() -> object:
    '''Returns cardset object from user input.'''
    cards2submit = input("Enter the cards you want to submit separated by commas. "
                        "If you do not want to play any more cards, enter 'finished':\n")
    cardset_obj = input_to_card_set(cards2submit)
    return(cardset_obj)

def target_cards_from_user_input() -> object:
    '''Returns cardset object from user input.'''
    target_cards = input('Enter the cards on the table where you want to'
                        'submit your cards:\n')
    cardset_obj = input_to_card_set(target_cards)
    return(cardset_obj)

def verify_player_has_cards(player: object, cards: object):
    '''Verify that the player has the cards that they submit. If they do not,
    keep asking them until they submit valid input. 
    
    Param cards: Cards that the player wants to submit. Can be instance of 
        card or cardset.'''
    # TODO: add 'stop'/'finished' functionality
    while not player.has_cards(cards):
        print('Error: {} does not have {}. Try again.'.format(player.name, cards))
        cards = cards2submit_from_user_input() 
        if player.has_cards(cards):
            return(cards)
    else:
        return(cards)

def verify_table_contains_target_cards(table: object, target_cards: object):
    '''Verify that the table has the cards where the player wants to add their cards. 
    If the table does not have the cards, keep asking the user for valid input until
    given.
    
    Param target_cards: Cardset on the table where the player wants to add their cards. 
        Cardset object.'''
    while not table.contains(target_cards):
        print('Error: The table does not have {}. Try again.'.format(target_cards))
        target_cards = target_cards_from_user_input()
        if table.contains(target_cards):
            return(target_cards)
    else:
        return(target_cards)

class UserInput:
    ''''Helper class for getting and verifying input from the user.'''
    def get_score_limit(self, score_limit = 250) -> int: 
        does_user_change_score = input('The default score limit is {}. Do you want to change this?\nEnter yes/no: '.format(score_limit))
        verified_input = check_str(does_user_change_score, ['yes', 'no'])
        if verified_input == 'yes':
            new_score = input('Enter the value you want to change the score limit to: ')
            verified_score = check_int(new_score)
            return(verified_score)
        else:
            return(score_limit)

    def get_player_names(self) -> List[str]: 
        player_names = input('Enter all player names separated by a commma. (e.g., p1, p2, ... etc.): ')
        player_names_lst = player_names.split(', ')
        return(player_names_lst)

    def discard_or_deck_or_all(self) -> str:
        long_message = ('Do you want to draw from the deck, take the top card of the discard pile, or take all cards from the discard pile?\nEnter deck/top/all: ')
        deck_or_discard_or_all = input(long_message)
        deck_or_discard_or_all = check_str(deck_or_discard_or_all, ['deck', 'top', 'all'])
        return(deck_or_discard_or_all)

    def add_to_table(self, table: object) -> str:
        '''Returns yes/no'''
        print(table)
        add_to_table = input('Do you want to add any cards to the table?\nEnter yes/no: ')
        verified_input = check_str(add_to_table, ['yes', 'no'])
        return(verified_input)    

    def add_to_target_cards(self) -> str:
        '''Returns yes/no'''
        add_to_target_cards = input('Do you want to add these cards to any existing groups'
                                    'on the table?\nEnter yes/no: ')
        verified_input = check_str(add_to_target_cards, ['yes', 'no'])
        return(verified_input)

    def get_discard_card(self, player: object) -> object:
        '''Verifies and returns the card the player wants to discard.'''
        card = discard_card_from_user_input()
        verified_card = verify_player_has_cards(player, card)
        return(verified_card)

    def get_player_cards(self, player: object) -> object:
        player.print_cards()
        cards2submit = cards2submit_from_user_input()
        if cards2submit == 'finished':
            return('finished')
        verified_cards = verify_player_has_cards(player, cards2submit)
        return(verified_cards)

    def get_target_cards(self, table: object) -> object:
        print(table)
        target_cards = target_cards_from_user_input()
        verified_cards = verify_table_contains_target_cards(table, target_cards)
        if verified_cards == 'stop':
            return('stop')
        return(verified_cards)

    def assign_wildcard_attrs(self, card: object) -> object:
        '''Use when a player is adding a wildcard to the table. Function should 
        be called for each wildcard that is played.
        
        If user wants to modify the card, returns modified card object.
        Else, returns the original card object'''

        yes_no_input = input('Do you want to assign an alternative suit and/or rank '
                            'to {}? Enter yes/no:\n'.format(card))
        yes_no = check_str(yes_no_input, ['yes', 'no'])
        if yes_no == 'yes':
            suit_input = input('Enter the suit you want to assign to the wildcard:\n')
            possible_suits = ['C', 'H', 'D', 'S']
            suit = check_str(suit_input.strip().upper(), possible_suits)
            card.hidden_suit = suit

            rank_input = input('Enter the rank you want to assign to the wildcard:\n')
            possible_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
            rank = check_str(rank_input.strip().upper(), possible_ranks)
            card.hidden_rank = rank

            int_value = _rank_to_int_dict[rank]
            card.hidden_int_value = int_value
            
if __name__ == '__main__':
    cardset = cards2submit_from_user_input()
    print(cardset)
    print(dir(cardset))