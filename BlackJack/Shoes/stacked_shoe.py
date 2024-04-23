from .shoe import Shoe
import random

class StackedShoe(Shoe):

    """
    This is mostly used for testing. 
    It lets you put cards in a particular order at the beginning of the shoe
    Remember to remove cutting the deck in the code
    """

    name = "Stacked Shoe"

    super_split_2_player = ["??", "3?", "A?", "6?", "3?", "A?", "6?", "3?", "8?", "7?", "3?", "3?", "3?", "2?", "T?", "K?", "A?", "7?", "5?", "A?", "J?", "A?", "A?", "T?", "A?", "9?"]
    dealer_blackjack_2_player = ["??", "A?", "3?", "T?", "K?", "Q?", "A?"]
    insurance_and_even_money_2_player = ["??", "A", "6", "A", "9", "K", "Q"]

    def __init__(self, stacked_cards, *args, **kwargs):
        super(StackedShoe, self).__init__(*args, **kwargs)
        self.stacked_cards = stacked_cards

    @staticmethod
    def _find_card_and_remove(cards, pip, suit):
        for i, card in enumerate(cards):
            if (card.pip == pip or pip == '?') and (card.suit == suit or suit == '?'):
                return cards.pop(i)
        return cards.pop(0)

    def shuffle_cards(self):
        random.shuffle(self.cards)

        # construct the stack by finding these cards in the deck
        beginning_of_the_shoe = []
        end_of_shoe = list(self.cards)
        for s in self.stacked_cards:
            pip, suit = (s[0], s[1]) if len(s) == 2 else (s[0], "?")
            card = self._find_card_and_remove(end_of_shoe, pip, suit)
            if card is not None:
                beginning_of_the_shoe.append(card)

        # shuffle everything not stacked and put the deck back to gether
        random.shuffle(end_of_shoe)
        self.cards = beginning_of_the_shoe + end_of_shoe