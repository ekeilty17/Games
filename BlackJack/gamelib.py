import random
import os

class Deck:

    def __init__(self):
        self.cards = [
                        'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC',
                        'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH',
                        'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS',
                        'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD'
                    ]

    def getCards(self):
        return self.cards

    def setCards(self, new_cards):
        self.cards = new_cards

    def Shuffle(self):
        random.shuffle(self.cards)

    def DealCard(self):
        if len(self.cards) == 0:
            return None
        dealt_card = self.cards[0]
        self.cards = self.cards[1:]
        return dealt_card

    def NewDeck(self):
        self.cards = [
                        'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC',
                        'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH',
                        'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS',
                        'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD'
                    ]

card_to_value = {
            'A': 11,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            'T': 10,
            'J': 10,
            'Q': 10,
            'K': 10
        }

# might have to add some stuff in the case of a soft 17
def getTotal(dealer_hand):
    accum = 0
    numAces = 0
    for card in dealer_hand:
        accum += card_to_value[card[0]]
        if card[0] == 'A':
            numAces += 1
    while accum > 21 and numAces != 0:
        accum -= 10
        numAces -= 1
    return accum

class Player:

    def __init__(self, name, hand, chips):
        self.name = name
        self.cards = [hand]
        self.chips = chips
        self.curr_bet = 0

        # cards are different than a hand 
        #   because you can split, a player can have multiple hands, which comprises his cards

    def newCards(self, cards):
        self.cards = [cards]

    def addCard(self, hand_num, card):
        self.cards[hand_num] += [card]

    def makeBet(self, bet):
        self.curr_bet = bet
        self.chips -= bet
    
    def split(self, hand_num):
        self.cards = self.cards[0:hand_num] + [[self.cards[hand_num][0]], [self.cards[hand_num][1]]] + self.cards[hand_num+1:]
        self.chips -= self.curr_bet

    def getTotal(self, hand):
        accum = 0
        numAces = 0
        for card in hand:
            accum += card_to_value[card[0]]
            if card[0] == 'A':
                numAces += 1
        while accum > 21 and numAces != 0:
            accum -= 10
            numAces -= 1
        return accum

    def DisplayCards(self, curr_hand):
        
        # to get rid of .0 if it doesn't need to be there
        total_bet = self.curr_bet * len(self.cards)
        if int(total_bet) == total_bet:
            total_bet = int(total_bet)
        
        total_chips = self.chips
        if int(total_chips) == total_chips:
            total_chips = int(total_chips)

        out = self.name + ": (" + str(total_chips) + ")\t\t\tBet: " + str(total_bet) + "\n"
        for j in range(len(self.cards)):
            if j == curr_hand:
                out += '\t    --> '
            else:
                out += '\t\t'
            for c in self.cards[j]:
                out += c + ' '
            out += "\t\t(" + str(self.getTotal(self.cards[j])) + ")"
        
            if self.getTotal(self.cards[j]) > 21:
                out += " BUSTED!"
            out += "\n"
        print out
        print


def DisplayTable(dealer_hand, players, curr_player, curr_hand, showDealer):

    os.system('clear')

    # Display dealer's hand
    if showDealer:
        out = "Dealer: \t"
        for card in dealer_hand:
            out += card + " "
        out += "\t\t(" + str(getTotal(dealer_hand)) + ")"

        if getTotal(dealer_hand) > 21:
            out += " BUSTED!"
        print out
        print
    else:
        print "Dealer: \t" + dealer_hand[0] + " ??"
        print

    # Displayer player's hands
    for i in range(len(players)):
        if i == curr_player:
            players[i].DisplayCards(curr_hand)
        else:
            players[i].DisplayCards(None)

stacked_deck = [
                    '2C', '4C', 
                    'AC', 'AH', 
                    '2C', '3C', '4C', '5C',
                    'AS', 'AD',
                    '6C', '7C', '8C', '9C', '4H', '5H', '6H', '7H', '8H', '9H', 
                    'TC', 'JC', '2H', '3H', 'QC', 'KC',
                    'TH', 'JH', 'QH', 'KH',
                    '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS',
                    '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD'
                ]
