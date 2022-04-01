from card import Card
import random

class Deck(object):

    def __init__(self):
        
        self.cards = []
        for suit in ['H', 'C', 'D', 'S']:
            
            # This logic will put the cards in the standard "new deck order"
            ordered_values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
            if suit in ['D', 'S']:
                ordered_values = reversed(ordered_values)
            
            for value in ordered_values:
                self.cards.append( Card(value, suit) )
    
    def __repr__(self):
        str_cards = [str(card) for card in self.cards]
        return ' '.join(str_cards)
        """
        return ' '.join(str_cards[0:13]) + '\n' + \
               ' '.join(str_cards[13:26]) + '\n' + \
               ' '.join(str_cards[26:39]) + '\n' + \
               ' '.join(str_cards[39:52])
        """

    def shuffle(self):
        random.shuffle(self.cards)
    
    # basically equivalent to popping from a queue or stack
    def deal(self):
        card = self.cards[0]
        self.cards = self.cards[1:]
        return cards


if __name__ == "__main__":

    D = Deck()
    print(D)
    print()
    D.shuffle()
    print(D)