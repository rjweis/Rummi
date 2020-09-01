from card import Card

class CardDeck:
    def get_cards(self):
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

    def number_of_cards(self):
        return(len(self.cards))