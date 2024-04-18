from gamelib import * 
from time import sleep
import os

def isGoodInput(val, possible):
    if val == None:
        return False
    if val.upper() in possible:
        return True
    return False

def isGoodBet(bet, min_bet, bet_intervals, max_bet):
    if bet == None:
        return False
    try:
        bet = float(bet)
    except:
        print "Input must be a number"
        return False
    
    if bet < min_bet:
        print "Must bet at least " + str(min_bet)
        return False
    if bet > max_bet:
        print "You don't have enough chips to make that bet"
        return False
    if bet % bet_intervals:
        print "You don't have the chips to make that bet"
        return False
    return True

def isSplitable(card1, card2):
    if card1[0] == card2[0]:
        return True
    if card1[0] in ['T', 'J', 'Q', 'K'] and card2[0] in ['T', 'J', 'Q', 'K']:
        return True
    return False


def BlackJack(num_players):
    
    # initialize variables
    deck = Deck()
    dealer_hand = [None, None]
    players = []
    for i in range(num_players):
        players += [Player("Player " + str(i+1), [], 100)]

    while True:
        
        # Shuffle deck
        deck.NewDeck()
        deck.Shuffle()
        
        # For testing purposes
        #deck.setCards(stacked_deck)

        # Deal cards to dealer and players
        dealer_hand = [deck.DealCard(), deck.DealCard()]
        for i in range(num_players):
            players[i].newCards([deck.DealCard(), deck.DealCard()])

        # Getting player bets
        min_bet = 5
        os.system('clear')
        for i in range(num_players):
            
            b = None    # b = bet
            print
            while not isGoodBet(b, min_bet, min_bet/float(2), players[i].chips):
                b = raw_input(players[i].name + "'s Bet: ")
            players[i].makeBet(float(b))
            

        # Options for each player (not a real BlackJack term)
        for i in range(num_players):
            
            p = players[i]      # current player
            d = None            # d = decision
            
            # Because of splitting, each player can have more than 1 hand
            # I can't just use a simple for loop because when a player splits
            # I need to restart each hand, and for loops don't let you just restart
            j = 0
            while j < len(p.cards):
                
                hand = p.cards[j]   # current hand of current player
                
                # Player can keep adding cards until total at 21
                while p.getTotal(hand) < 21:
                    
                    DisplayTable(dealer_hand, players, i, j, False)

                    # Constructing possible decisions given the player's hand
                    decisions = ['H', 'ST', 'D']
                    decision_string = p.name + ": (H) Hit, (St) Stand, (D) Double, "
                
                    # Can split iff first two cards are the same value
                    if isSplitable(hand[0], hand[1]):
                        decisions += ['SP']
                        decision_string += "(Sp) Split, "
                    decisions += ['SR']
                    decision_string += "(Sr) Surrender\n"
                
                    # Getting player's decision
                    d = None
                    while not isGoodInput(d, decisions):
                        if d != None:
                            print "Not a valid option, try again" 
                        print
                        d = raw_input(decision_string)
                
                    # Executing game rules based on decision made
                    if d.upper() == 'H':
                        p.addCard(j, deck.DealCard())
                    
                    elif d.upper() == 'ST':
                        # move onto next player
                        break
                    elif d.upper() == 'D':
                        # Double bet
                        self.chips -= self.curr_bet
                        self.curr_bet *= 2

                        # get only one more card
                        p.addCard(j, deck.DealCard())

                        # move onto next player
                        break
                    elif d.upper() == 'SP':
                        # Splitting hand
                        p.split(j)
                        # Doubling the bet is done by the .split() method

                        # add a card to each hand
                        p.addCard(j, deck.DealCard())
                        p.addCard(j+1, deck.DealCard())
                        # resetting dealer index
                        j -= 1
                        # move to next player
                        break
                    elif d.upper() == 'SR':
                        # Return half of chips
                        p.chips += 0.5*p.curr_bet
                        p.curr_bet = 0
                        # move to next player
                        break
                j += 1

        # Determining results
        DisplayTable(dealer_hand, players, None, None, True)
        while getTotal(dealer_hand) <= 17:
            
            # Dealer doesn't hit on a hard 17
            isHard = True
            for card in dealer_hand:
                if card[0] == 'A':
                    isHard = False
                    break
            if getTotal(dealer_hand) == 17 and isHard:
                break

            dealer_hand += [deck.DealCard()]
            sleep(1)
            DisplayTable(dealer_hand, players, None, None, True)
        
        # Need to compare each players hand to the dealer
        # and redistributing chips
        for i in range(num_players):
            
            p = players[i]

            for hand in p.cards:
                
                if getTotal(dealer_hand) > 21:
                    
                    if p.getTotal(hand) == 21:
                        p.chips += 2.5*p.curr_bet
                    elif p.getTotal(hand) < 21:
                        p.chips += 2*p.curr_bet

                elif getTotal(dealer_hand) == 21:
                    
                    if p.getTotal(hand) == 21:
                        p.chips += 1.5*p.curr_bet
                
                else:
                    
                    if p.getTotal(hand) > getTotal(dealer_hand):
                    
                        if p.getTotal(hand) == 21:
                            p.chips += 2.5*p.curr_bet
                        else:
                            p.chips += 2*p.curr_bet

                    elif p.getTotal(hand) == getTotal(dealer_hand):
                        p.chips += p.curr_bet
            
            p.curr_bet = 0

        DisplayTable(dealer_hand, players, None, None, True)
        x = raw_input("Hit ENTER to go to next hand")

BlackJack(2)
