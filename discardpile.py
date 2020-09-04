import random 

class DiscardPile:
    ''''Players end each turn by discarding a card from their hand.'''

    def __len__(self):
        return(len(self.cards))

    def __repr__(self):
        '''Players can only see the top card of the pile at a given time.'''
        return(self.cards[-1].id)

    def print_top_card(self):
        print("Top card of the discard pile: {}\n".format(self))

    def print_number_of_cards(self):
        print('Number of cards in discard pile: {}'.format(len(self)))

    def print_info(self):
        '''Call print_top_card and print_number_of_cards.'''
        self.print_number_of_cards()
        if self.cards:
            self.print_top_card()

    def __init__(self, card_deck: object):
        '''When the game starts, a card is randomly drawn from the card_deck
        and placed into the discard pile. Like the card_deck object, the discard
        pile is a list of card objects.
        
        Args:
            card_deck: A random card object is drawn from the card_deck
        Attrs:
            cards: List of card objects.
        '''
        selected_card = random.choice(card_deck.cards)
        card_deck.cards.remove(selected_card)
        self.cards = [selected_card]