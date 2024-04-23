from card import Card

class Hand(object):

    def __init__(self, bet, *cards):
        self.cards = list(cards)
        self.bet = bet
        self.is_resolved = False
        self.is_doubled = False
        self.insurance = False
        self.even_money = False
    
    # TODO: If player has soft 11, we probably shouldn't display as (11/21)
    def __repr__(self):
        if len(self.cards) == 0:
            return f"${self.bet}:"
        str_cards = [str(card) for card in self.cards]
        if self.is_doubled:
            str_cards[-1] = f"[{str_cards[-1]}]"
        total = self.get_total()
        str_totals = [str(total), str(total+10)] if self.is_soft_hand() else [str(total)]
        str_bet = f"${self.bet} + ${self.bet}" if self.is_doubled else f"${self.bet}"
        str_insurance = f"\n\t${self.bet//2}:\tInsurance" if self.insurance else ""
        str_even_money = f"\n\tTook Even Money" if self.even_money else ""
        return f"{str_bet}:\t{' '.join(str_cards)}\t({'/'.join(str_totals)}){str_insurance}{str_even_money}"
    
    def __len__(self):
        return len(self.cards)

    def contains_ace(self):
        for card in self.cards:
            if card.pip == 'A':
                return True
        return False

    # TODO: should a soft 11 be counted as a soft hand?
    def is_soft_hand(self):
        # the A's in this sum are set to 1 by default
        # therefore, if an ace exists, it's only a soft hand if the total is less than 11
        # otherwise letting one of the aces be 11 would make the hand > 21
        return self.contains_ace() and self.get_total() <= 11

    def get_total(self):
        return sum(self.cards)
    
    def get_comparison_total(self):
        total = self.get_total()
        return total + 10 if self.is_soft_hand() else total

    def add_card(self, card):
        if self.is_busted():
            raise ValueError(f"This hand is busted ({' '.join([str(c) for c in self.cards])} = {self.get_total()}). It should not recieve another card.")
        self.cards.append(card)

    def resolve(self):
        self.is_resolved = True

    def double_down(self):
        self.is_doubled = True

    def take_insurance(self):
        self.insurance = True
    
    def take_even_money(self):
        self.even_money = True

    def is_busted(self):
        return self.get_total() > 21
    
    def is_hard_21(self):
        return self.get_total() == 21

    def is_soft_21(self):
        return self.contains_ace() and self.get_total() == 11
    
    def is_21(self):
        return self.is_hard_21() or self.is_soft_21()
    
    def is_blackjack(self):
        return len(self.cards) == 2 and self.is_21()

    """ Comparisons """
    def __eq__(self, other):
        if not isinstance(other, Hand):
            raise TypeError("Comparing only implemented between 'Hand' types")
        return self.get_comparison_total() == other.get_comparison_total()
    
    def __gt__(self, other):
        if not isinstance(other, Hand):
            raise TypeError("Comparing only implemented between 'Hand' types")
        return self.get_comparison_total() > other.get_comparison_total()
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def ge(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __lt__(self, other):
        return (not self.__gt__(other)) and (not self.__eq__(other))
    
    def __le__(self, other):
        return not self.__gt__(other)

class DealerHand(Hand):

    def __init__(self, *cards):
        super(DealerHand, self).__init__(0, *cards)
        self._hide_hole_card = True

    # TODO: If dealer has soft 18, we probably shouldn't display at (8/18)
    def __repr__(self):
        str_cards = [str(card) for card in self.cards]
        total = self.get_total()
        str_totals = [str(total), str(total+10)] if self.is_soft_hand() else [str(total)]
        if len(self.cards) <= 2 and self._hide_hole_card:
            if len(self.cards) == 2:
                str_cards[1] = "??"
            return ' '.join(str_cards)
        else:
            return f"{' '.join(str_cards)}\t({'/'.join(str_totals)})"

    def reveal_hole_card(self):
        self._hide_hole_card = False


if __name__ == "__main__":
    H1 = Hand(10)
    print(H1)

    H2 = Hand(10, Card("AH"), Card("AS"))
    print(H2)
    H2.add_card(Card("TD"))
    print(H2)
    H2.add_card(Card("9C"))
    print(H2)

    H3 = Hand(10, Card("AH"), Card("KS"))
    print(H3)

    DH = DealerHand(Card("4H"), Card("9D"))
    print(DH)
    DH.dealer_show()
    print(DH)