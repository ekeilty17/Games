from WinningHands import *
import os
import random

def print_hand(hand, deck):
    out = ""
    for card in hand:
        out += str(deck[card]) + "  "
    return out

#N is the number of players
def Five_Card_Stud(N=2):
    #You really can't play with more ppl bc there aren't enough cards
    if N > 4:
        return False

    deck = [    'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC',
                'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH',
                'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS',
                'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD'
            ]
    shuffle = random.sample(range(0,52),52)

    #each players hand is given by an index
    player_hands = []
    for p in range(N):
        player_hands += [shuffle[:5]]
        shuffle = shuffle[5:]

    T = 3
    for t in range(T):
        os.system('cls' if os.name == 'nt' else 'clear')
        for p in range(N):
            temp = raw_input("Press enter to see Player " + str(p+1) + " input.")
            #printing player hand
            print
            print print_hand(player_hands[p], deck)
            print

            #making sure input is valid
            correct_input = False
            discard = ""
            while not correct_input:
                discard = raw_input("Which cards do you want to replace? (ex: 1, 2, 4)\n")

                #Make it so that "1, 2, 3" and "1,2,3" and "1 2 3" are both valid inputs
                discard = discard.split(',')
                discard2 = ""
                for c in discard:
                    discard2 += c + ' '
                discard = discard2.split()

                #Making sure indeces are in rangee
                correct_input = True
                for c in discard:
                    if not (0 < int(c) < 6):
                        print "Inputs must be between 1 and 5"
                        correct_input = False
                        break

            #replacing specificed cards
            for c in discard:
                player_hands[p][int(c)-1] = shuffle[0]
                shuffle = shuffle[1:]

            print
            print print_hand(player_hands[p], deck)
            print

            print
            temp = raw_input("Press enter to clear the terminal.")
            os.system('cls' if os.name == 'nt' else 'clear')
    
    winning = 0
    for p in range(1,N):
        better = compare(        

Five_Card_Stud()
