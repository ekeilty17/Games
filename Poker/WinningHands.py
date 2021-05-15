card_val = {
        '2' : 2,
        '3' : 3,
        '4' : 4,
        '5' : 5,
        '6' : 6,
        '7' : 7,
        '8' : 8,
        '9' : 9,
        'T' : 10,
        'J' : 11,
        'Q' : 12,
        'K' : 13,
        'A' : 14
    }

def getHighestCard(hand):
    highest_val = 0
    for C in hand:
        if card_val[C[0]] > highest_val:
            highest_val = card_val[C[0]]
    return highest_val

def OnePair(hand):
    hand_vals = []
    for C in hand:
        hand_vals += [card_val[C[0]]]
    for i in range(0,len(hand_vals)-1):
        for j in range(i+1,len(hand_vals)):
            if hand_vals[i] == hand_vals[j]:
                return [True, hand_vals[i]]
    return [False, -1]

def TwoPair(hand):
    hand_vals = []
    for C in hand:
        hand_vals += [card_val[C[0]]]
    pairs = []
    for i in range(0,len(hand_vals)-1):
        for j in range(i+1,len(hand_vals)):
            if hand_vals[i] == hand_vals[j]:
                pairs += [hand_vals[i]]
    if len(pairs) == 2:
        return [True, max(pairs[0], pairs[1])]
    return [False, -1]

def ThreeOfaKind(hand):
    hand_vals = []
    for C in hand:
        hand_vals += [card_val[C[0]]]
    for i in range(0,len(hand_vals)-1):
        for j in range(i+1,len(hand_vals)):
            for k in range(j+1,len(hand_vals)):
                if hand_vals[i] == hand_vals[j] == hand_vals[k]:
                    return [True, hand_vals[i]]
    return [False, -1]

def Straight(hand):
    hand_vals = []
    for C in hand:
        hand_vals += [card_val[C[0]]]
    hand_vals = list(sorted(hand_vals))
    if hand_vals[0]+4 == hand_vals[1]+3 == hand_vals[2]+2 == hand_vals[3]+1 == hand_vals[4]:
        return [True, hand_vals[4]]
    #accounting for the fact aces can be high or low
    if 14 in hand_vals:
        hand_vals = [1] + hand_vals[0:-1]
    if hand_vals[0]+4 == hand_vals[1]+3 == hand_vals[2]+2 == hand_vals[3]+1 == hand_vals[4]:
        return [True, 14]
    return [False, -1]

def Flush(hand):
    hand_suits = []
    for C in hand:
        hand_suits += [C[1]]
    if hand_suits[0] == hand_suits[1] == hand_suits[2] == hand_suits[3] == hand_suits[4]:
        return [True, getHighestCard(hand)]
    return [False, -1]

def FullHouse(hand):
    if not FourOfaKind(hand):
        hand_vals = []
        for C in hand:
            hand_vals += [card_val[C[0]]]
        L = list(set(hand_vals))
        if len(L) == 2:
            cnt = 0
            for C in hand_vals:
                if C == L[0]:
                    cnt += 1
            if cnt == 3:
                return [True, L[0]]
            else:
                return [True, L[1]]
    return [False, -1]

def FourOfaKind(hand):
    hand_vals = []
    for C in hand:
        hand_vals += [card_val[C[0]]]
    for i in range(0,len(hand_vals)-1):
        for j in range(i+1,len(hand_vals)):
            for k in range(j+1,len(hand_vals)):
                for l in range(k+1,len(hand_vals)):
                    if hand_vals[i] == hand_vals[j] == hand_vals[k] == hand_vals[l]:
                        return [True, hand_vals[i]]
    return [False, -1]

def StraightFlush(hand):
    if Straight(hand)[0] and Flush(hand)[0]:
        return [True, Straight(hand)[1]]
    return [False, -1]

def RoyalFlush(hand):
    hand_vals = []
    for C in hand:
        hand_vals += [card_val[C[0]]]
    if Flush(hand) and hand_vals == [10, 11, 12, 13, 14]:
        return [True, 14]
    return [False, -1]


def HandScore(hand):
    if RoyalFlush(hand)[0]:
        return 9
    elif StraightFlush(hand)[0]:
        return 8
    elif FourOfaKind(hand)[0]:
        return 7
    elif FullHouse(hand)[0]:
        return 6
    elif Flush(hand)[0]:
        return 5
    elif Straight(hand)[0]:
        return 4
    elif ThreeOfaKind(hand)[0]:
        return 3
    elif TwoPair(hand)[0]:
        return 2
    elif OnePair(hand)[0]:
        return 1
    return 0

def compare(hand1, hand2):
    S1 = HandScore(hand1)
    S2 = HandScore(hand2)
    if S1 > S2:
        return 1
    elif S2 > S1:
        return 2
    else:
        high1 = 0
        high2 = 0
        if S1 == 8:     #Royal Flush
            high1 = StraightFlush(hand1)[1]
            high2 = StraightFlush(hand2)[1]
        elif S1 == 7:   #Four of a Kind
            high1 = FourOfaKind(hand1)[1]
            high2 = FourOfaKind(hand2)[1]
            if high1 == high2:
                new1 = [C for C in hand1 if card_val[C[0]] != high1]
                new2 = [C for C in hand2 if card_val[C[0]] != high2]
                high1 = getHighestCard(new1)
                high2 = getHighestCard(new2)
        elif S1 == 6:   #Full House
            high1 = FullHouse(hand1)[1]
            high2 = FullHouse(hand2)[1]
        elif S1 == 5:   #Flush
            high1 = Flush(hand1)[1]
            high2 = Flush(hand2)[1]
        elif S1 == 4:   #Straight
            high1 = Straight(hand1)[1]
            high2 = Straight(hand2)[1]
        elif S1 == 3:   #Three of a Kind
            high1 = ThreeOfaKind(hand1)[1]
            high2 = ThreeOfaKind(hand2)[1]
        elif S1 == 2:   #Two Pair
            high1 = TwoPair(hand1)[1]
            high2 = TwoPair(hand2)[1]
            if high1 == high2:
                new1 = [C for C in hand1 if card_val[C[0]] != high1]
                new2 = [C for C in hand2 if card_val[C[0]] != high2]
                high1 = getHighestCard(new1)
                high2 = getHighestCard(new2)
        elif S1 == 1:   #One Pair
            high1 = OnePair(hand1)[1]
            high2 = OnePair(hand2)[1]
            if high1 == high2:
                new1 = [C for C in hand1 if card_val[C[0]] != high1]
                new2 = [C for C in hand2 if card_val[C[0]] != high2]
                high1 = getHighestCard(new1)
                high2 = getHighestCard(new2)
        else:
            high1 = getHighestCard(hand1)
            high2 = getHighestCard(hand2)
        if high1 > high2:
            return 1
        elif high2 > high1:
            return 2
    return 0

#test
#P1 = ["5H", "5C", "6S", "7S", "KD"]
#P2 = ["2C", "3S", "8S", "8D", "TD"]

#P1 = ["5D", "8C", "9S", "JS", "AC"]
#P2 = ["2C", "5C", "7D", "8S", "QH"]

#P1 = ["2D", "9C", "AS", "AH", "AC"]
#P2 = ["3D", "6D", "7D", "TD", "QD"]

#P1 = ["4D", "6S", "9H", "QH", "QC"]
#P2 = ["3D", "6D", "7H", "QD", "QS"]

#P1 = ["2H", "2D", "4C", "4D", "4S"]
#P2 = ["3C", "3D", "3S", "9S", "9D"]


#print P1,HandScore(P1),'\t',P2,HandScore(P2),'\t',compare(P1,P2)

#print Straight(['AS', '2D', '3D', '4D', '5H'])
#print Straight(['AS', 'KD', 'QD', 'JD', 'TH'])
