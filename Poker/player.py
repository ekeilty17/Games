from card import Card
from hand import Hand

class Player(object):

    def __init__(self, name, money):
        self.name = name
        self.money = money
    

    def __repr__(self)
        return f"{self.name}: {self.money}"
    

    def deal(self, card):
        pass


if __name__ == "__main__":

    hand = ["AC", "TC"]
    common = ["KC", "QC", "JC", "7D", "2S"]

    hand = [Card(card) for card in hand]
    common = [Card(card) for card in common]

    P = Player(hand, common)
    P.get_best_hand()