class Card(object):

    value_rank = {
        '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7, '8' : 8,
        '9' : 9, 'T' : 10, 'J' : 11, 'Q' : 12, 'K' : 13, 'A' : 14
    }

    def __init__(self, *args, seed=None):
        
        self.seed = seed
        if not self.seed is None:
            random.seed(self.seed)

        # some error parsing and checking
        if len(args) == 1:
            card = args[0]
            if type(card) != str or len(card) != 2:
                raise TypeError(f"Expected a string with 2 characters, got {card}")
            value = card[0]
            suit = card[1]
        
        if len(args) == 2:
            value, suit = args
            if type(value) not in [str, int] or len(str(value)) != 1:
                raise TypeError(f"In first argument, expected a single character or integer, got {value}")
            if type(suit) not in [str, int] or len(str(suit)) != 1:
                raise TypeError(f"In first argument, expected a single character or integer, got {suit}")

        self.value = str(value).upper()
        self.suit = str(suit).upper()

        if self.value not in self.all_values():
            raise ValueError(f"Got value {self.value}, expected {self.all_values()}")
        
        if self.suit not in self.all_suits():
            raise ValueError(f"Got suit {self.suit}, expected {self.all_suits()}")

    @staticmethod
    def all_values():
        return ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']

    @staticmethod
    def all_suits():
        return ['C', 'H', 'D', 'S']

    def __repr__(self):
        return f"{self.value}{self.suit}"
    

    """ When we compare cards, we only care about the value, not the suit of the card  """

    def __eq__(self, other):
        if not isinstance(other, Card):
            raise TypeError("Comparing only implemented between 'Card' types")
        return self.value == other.value
    
    def __gt__(self, other):
        if not isinstance(other, Card):
            raise TypeError("Comparing only implemented between 'Card' types")
        return self.value_rank[self.value] > self.value_rank[other.value]
    
    # only have to implement the above, and the rest follow
    def __ne__(self, other):
        return not self.__eq__(other)

    def ge(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __lt__(self, other):
        if not isinstance(other, Card):
            raise TypeError("Comparing only implemented between 'Card' types")
        return other.__gt__(self)
    
    def le(self, other):
        return self.__lt__(other) or self.__eq__(other)

if __name__ == "__main__":

    C1 = Card("TH")
    C2 = Card("TD")
    C3 = Card("4S")
    C4 = Card("AS")

    print(C1 < C3)

    L = [C1, C2, C3, C4]
    print(L)
    print(list(sorted(L)))
    print()