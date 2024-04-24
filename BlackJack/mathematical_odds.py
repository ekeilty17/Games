from Players import Dealer
from hand import DealerHand
from card import Card
from action import Action
from Shoes import FairShoe

import numpy as np
from prettytable import PrettyTable

def cell_color(value):
    if value == 0:
        return '\033[30m'
    if value < 0.1:
        return '\033[91m'
    if value < 0.2:
        return '\033[33m'
    if value < 0.4:
        return '\033[92m'
    return '\033[96m'

def display_odds_table(odds_table, row_labels, title=None):
    pretty_table = PrettyTable()
    if title is not None:
        pretty_table.title = title
    pretty_table.field_names = [""] + [str(tf) for tf in range(17, 22)] + ["bust"]

    for label, row in reversed(list(zip(row_labels, odds_table))):
        pretty_table.add_row([str(label)] + [cell_color(cell) + str(round(cell, 4)) + '\033[0m' for cell in row])
    
    # odds_table.add_row(["-" * 6] * len(odds_table.field_names))
    # means = np.round(np.mean(S, axis=0), decimals=3)
    # odds_table.add_row([""] + list(means))
    # print(sum(means))

    return pretty_table

def dealer_probabilities(hit_on_soft_17=False):
    H = np.zeros((19, 6))       # hard hands, (4 to 21 + bust) by (17 to 21 + bust)
    S = np.zeros((10, 6))       # soft hands, (2 to 10) by (17 to 21 + bust)

    H.fill(0)
    S.fill(0)

    # base-cases
    for ti in range(17, 23):
        H[ti-4, ti-17] = 1
    for ti in range(17, 22):
        S[ti-12, ti-17] = 1

    #                     A, 2, 3, 4, 5, 6, 7, 8, 9, T
    card_freq = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 4])

    # Recurance

    # First we solve for hard hands which have a total > 11, since these cannot become soft hands
    for ti in reversed(range(11, 17)):
        for tf in range(17, 23):
            # We count Aces as having value 1 here, since having value 11 will cause a bust
            for c in range(1, 11):
                t = min(ti+c, 22)
                H[ti-4, tf-17] += H[t-4, tf-17] * card_freq[c-1]
            H[ti-4, tf-17] /= sum(card_freq)

    # Now, we can solve for all the soft hands since either it remains a soft hand, or it will become a hard hand > 11
    for ti in reversed(range(12, 17)):
        for tf in range(17, 23):
            # We count Aces as having value 1 here, since having value 11 will cause a bust
            for c in range(1, 11):
                t = ti + c
                if t > 21:      # since it's a soft hand, if we go over 21, we treat the A as value 1 instead of 10, now the hard becomes hard
                    t -= 10
                    S[ti-12, tf-17] += H[t-4, tf-17] * card_freq[c-1]
                else:
                    S[ti-12, tf-17] += S[t-12, tf-17] * card_freq[c-1]
            S[ti-12, tf-17] /= sum(card_freq)

    # Finally, we can finish the rest of the hard hands
    for ti in reversed(range(4, 11)):
        for tf in range(17, 23):
            # We do 2-T as we normally would
            for c in range(2, 11):
                t = ti+c        # since ti <= 10, we can never bust
                H[ti-4, tf-17] += H[t-4, tf-17] * card_freq[c-1]
            # Aces are an exception since they give the soft-hand case
            t = ti+11
            H[ti-4, tf-17] += S[t-12, tf-17] * card_freq[c-1]

            H[ti-4, tf-17] /= sum(card_freq)

    hard_row_labels = [str(ti) for ti in range(4, 22)] + ["bust"]
    print(display_odds_table(H, hard_row_labels, title="Hard Hands (Calculate)"))
    print()
    print()
    soft_row_labels = ["12 (A,A)"] + [f"{ti+10} (A,{ti-1})" for ti in range(3, 11)] + ["21 (A,T)"]
    print(display_odds_table(S, soft_row_labels, title="Soft Hands (Calculated)"))

def dealer_simulator(hit_on_soft_17=False, number_of_simulations=100):
    table_rules = {
        "hit_on_soft_17": hit_on_soft_17,
    }
    dealer = Dealer(**table_rules)

    H = np.zeros((19, 6))
    S = np.zeros((10, 6))
    for ti in range(17, 23):
        H[ti-4, ti-17] = 1
    for ti in range(17, 22):
        S[ti-12, ti-17] = 1
    
    shoe = FairShoe(number_of_decks=8)
    
    # hard hands
    first_card = Card("2C")
    for pip in ["2", "3", "4", "5", "6", "7", "8", "9", "T","A"]:
        second_card = Card(f"{pip}S")

        for i in range(number_of_simulations):
            dealer_hand = DealerHand(first_card, second_card)
            ti = min(dealer_hand.get_comparison_total(), 22)

            shoe.shuffle()
            while True:
                action = dealer.action(dealer_hand, allowed_actions=[Action.HIT, Action.STAND])
                if action == Action.STAND:
                    break
                dealer_hand.add_card( shoe.deal() )
            
            tf = min(dealer_hand.get_comparison_total(), 22)
            H[ti-4, tf-17] += 1
    
    first_card = Card("TC")
    for pip in ["4", "5", "6"]:
        second_card = Card(f"{pip}S")

        for i in range(number_of_simulations):
            dealer_hand = DealerHand(first_card, second_card)
            ti = min(dealer_hand.get_comparison_total(), 22)

            shoe.shuffle()
            while True:
                action = dealer.action(dealer_hand, allowed_actions=[Action.HIT, Action.STAND])
                if action == Action.STAND:
                    break
                dealer_hand.add_card( shoe.deal() )
            
            tf = min(dealer_hand.get_comparison_total(), 22)
            H[ti-4, tf-17] += 1
    
    # soft hands
    first_card = Card("AC")
    for pip in ["2", "3", "4", "5", "6", "7", "8", "9", "T", "A"]:
        second_card = Card(f"{pip}S")

        for i in range(number_of_simulations):
            dealer_hand = DealerHand(first_card, second_card)
            ti = min(dealer_hand.get_comparison_total(), 22)

            shoe.shuffle()
            while True:
                action = dealer.action(dealer_hand, allowed_actions=[Action.HIT, Action.STAND])
                if action == Action.STAND:
                    break
                dealer_hand.add_card( shoe.deal() )
            
            dealer_hand.reveal_hole_card()
            tf = min(dealer_hand.get_comparison_total(), 22)
            S[ti-12, tf-17] += 1
    
    # normalize tables
    for row in H:
        row /= sum(row)
    for row in S:
        row /= sum(row)

    hard_row_labels = [str(ti) for ti in range(4, 22)] + ["bust"]
    print(display_odds_table(H, hard_row_labels, title="Hard Hands (Simulated)"))
    print()
    print()
    soft_row_labels = ["12 (A,A)"] + [f"{ti+10} (A,{ti-1})" for ti in range(3, 11)] + ["21 (A,T)"]
    print(display_odds_table(S, soft_row_labels, title="Soft Hands (Simulated)"))

if __name__ == "__main__":
    dealer_simulator(number_of_simulations=10000)
    print()
    print("-"*70)
    print()
    dealer_probabilities()