import pathsetup
from card import Card
from cardset import CardSet
from table import Table
from discardpile import DiscardPile
from carddeck import CardDeck
from player import Player

deck = CardDeck()
discard = DiscardPile(deck)
p1 = Player('p1', deck)
p1.print_cards()

def input_to_card_set(input):
    card_strings = input.strip().split(', ')
    card_lst = [Card(cs) for cs in card_strings]
    card_set = CardSet(card_lst)
    return(card_set)

def test_add2target_cards():
    target_cards = input('Input target_cards separated by commas:\n')
    target_cards = input_to_card_set(target_cards)
    table = Table([target_cards])

    cards2submit = input('Input cards2submit separated by commas:\n')
    cards2submit = input_to_card_set(cards2submit)
    p1.make_move_add2target_cards(cards2submit, target_cards, table)
    p1.print_cards()
    print(table)

def test_cards_stand_alone():
    table = Table()
    cards2submit = input('Input cards2submit separated by commas:\n')
    cards2submit = input_to_card_set(cards2submit)
    p1.make_move_cards_stand_alone(cards2submit, table)
    p1.print_cards()
    print(table)

def test_draw():
    for _ in range(2):
        p1.draw_from_deck(deck)
        user_input = input('Input card2discard:\n').strip()
        card2discard = Card(user_input)
        p1.discard(card2discard, discard)

    p1.draw_all_cards_from_discard_pile(discard)

    for _ in range(2):
        user_input = input('Input card2discard:\n').strip()
        card2discard = Card(user_input)
        p1.discard(card2discard, discard)
        
    p1.draw_all_cards_from_discard_pile(discard)
        

test_draw()


