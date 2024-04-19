class Card(object):

    all_pips = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
    pip_rank = {
        'A' : 1, '2' : 2, '3' : 3, '4' : 4, '5' : 5, '6' : 6, '7' : 7,
        '8' : 8, '9' : 9, 'T' : 10, 'J' : 10, 'Q' : 10, 'K' : 10
    }

    all_suits = ['H', 'C', 'D', 'S']
    suit_symbols = {
        'H': '♡', 'C': '♣', 'D': '♢', 'S': '♠'
    }

    def __init__(self, *args, ace_high=False):

        if ace_high:
            pip_rank['A'] = 11

        # some error parsing and checking
        if len(args) == 1:
            card = args[0]
            if type(card) not in [str, list, tuple] or len(card) != 2:
                raise TypeError(f"Expected a string with 2 characters or a list/tuple of length 2, instead got {card}")
            pip = card[0]
            suit = card[1]
        
        elif len(args) == 2:
            pip, suit = args
            if type(pip) not in [str, int] or len(str(pip)) != 1:
                raise TypeError(f"In first argument, expected a single character or integer, instead got {pip}")
            if type(suit) not in [str, int] or len(str(suit)) != 1:
                raise TypeError(f"In second argument, expected a single character or integer, instead got {suit}")
        
        else:
            raise TypeError(f"Recieved more arguments than 2 arguments, {args}")

        self.pip = str(pip).upper()
        self.suit = str(suit).upper()

        if self.pip not in self.all_pips:
            raise ValueError(f"Got pip {self.pip}, expected one of {self.all_pips}")
        
        if self.suit not in self.all_suits:
            raise ValueError(f"Got suit {self.suit}, expected one of {self.all_suits}")

        self.value = self.pip_rank[self.pip]

    def __repr__(self):
        return f"{self.pip}{self.suit_symbols[self.suit]}"
    

    """ In most games, when comparing cards we only care about the value, not the suit of the card  
        Also, if you want to distinguish between suits, (say sort the cards uniquely) you can use the string representation
    """
    def __eq__(self, other):
        if isinstance(other, CutCard):
            return False
        if not isinstance(other, Card):
            raise TypeError("Comparing only implemented between 'Card' types")
        return self.pip_rank[self.pip] == self.pip_rank[other.pip]
    
    def __gt__(self, other):
        if isinstance(other, CutCard):
            # I'll treat the cut card as having value 0
            return True
        if not isinstance(other, Card):
            raise TypeError("Comparing only implemented between 'Card' types")
        return self.pip_rank[self.pip] > self.pip_rank[other.pip]
    
    # only have to implement the above, and the rest can be derived
    def __ne__(self, other):
        return not self.__eq__(other)

    def ge(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __lt__(self, other):
        return (not self.__gt__(other)) and (not self.__eq__(other))
    
    def __le__(self, other):
        return not self.__gt__(other)


    """ So we can add card values """
    def __add__(self, other):
        if isinstance(other, CutCard):
            return self.pip_rank[self.pip]
        return other.__add__(self.pip_rank[self.pip]) 
    
    def __radd__(self, other):
        if isinstance(other, CutCard):
            return self.pip_rank[self.pip]
        return other.__add__(self.pip_rank[self.pip]) 


class CutCard(object):

    def __init__(self):
        self.pip = None
        self.suit = None

    def __repr__(self):
        return "||"

    def __eq__(self, other):
        if isinstance(other, CutCard):
            return True
        if not isinstance(other, Card):
            raise TypeError("Comparing only implemented between 'CutCard' and 'Card' types")
        return other.__eq__(self)
    
    def __gt__(self, other):
        if isinstance(other, CutCard):
            return False
        if not isinstance(other, Card):
            raise TypeError("Comparing only implemented between 'CutCard' and 'Card' types")
        return other.__lt__(self)

    def __ne__(self, other):
        return not self.__eq__(other)

    def ge(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __lt__(self, other):
        return (not self.__gt__(other)) and (not self.__eq__(other))
    
    def __le__(self, other):
        return not self.__gt__(other)

if __name__ == "__main__":

    C1 = Card("TH")
    C2 = Card("TD")
    C3 = Card("4S")
    C4 = Card("AS")
    C5 = Card("A", "D")
    CC = CutCard()

    print(CC)
    print(str(C1), '<=', str(C3), C3 <= C1)

    L = [C1, C2, C3, C4, C5]
    print(sum(L))
    print(L)
    print(list(sorted(L)))
    print()