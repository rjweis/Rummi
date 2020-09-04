from card import Card

class CardDeck:
    '''Players get their cards from the card deck.'''
    def get_cards(self):
        '''Card deck will be defined as list of card objects. Each
        card object is represented by a string, where the 0th char
        represents the suit and the remaining chars represent the
        rank.
        '''
        suits = ['S', 'C', 'D', 'H']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        cards = []
        for suit in suits:
            for rank in ranks:
                card = Card(suit+rank)
                cards.append(card)
        return(cards)

    def __init__(self):
        self.cards = self.get_cards()