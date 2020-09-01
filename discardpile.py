import random 

class DiscardPile:
    def __len__(self):
        return(len(self.cards))

    def top_card(self):
        return(self.cards[-1].id)

    def print_top_card(self):
        print("Top card of the discard pile: {}\n".format(self.top_card()))

    def print_number_of_cards(self):
        print('Number of cards in discard pile: {}'.format(len(self)))

    def print_info(self):
        self.print_number_of_cards()
        if self.cards:
            self.print_top_card()

    def __init__(self, card_deck: object):
        selected_card = random.choice(card_deck.cards)
        card_deck.cards.remove(selected_card)
        self.cards = [selected_card]

if __name__ == '__main__':
    from carddeck import CardDeck
    deck = CardDeck()
    discard = DiscardPile(deck)
    discard.print_info()