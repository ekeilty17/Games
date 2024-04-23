import os
import math

from card import CutCard
from Players import Dealer
from hand import Hand, DealerHand
from action import Action

class BlackJackTable(object):

    """
    This is essentially the game engine
    """

    def __init__(self, shoe, number_of_spots=8, verbose=False, **table_rules):
        
        self.table_rules = table_rules

        # This is what I would consider a high-quality BlackJack game that is realistic to find
        default_table_rules = {
            # bets and cards
            "min_bet": 10,
            "max_bet": 1000,
            "number_of_decks": 6,

            # dealing procedures
            "blackjack_multiplier": 1.5,    # never play a table where this is 1.2 (6:5)
            "hit_on_soft_17": False,        # dealer standing on soft 17 is better for the player
            "dealer_peaks_for_blackjack": True,    # If set to False, this is called ENHC rules
            "insurance_and_even_money": True,
            "early_surrender": False,       # Almost no casino would allow this, it's too good for the player
            
            # player action
            "late_surrender": True,         # Many places actually don't allow this
            "double_after_split": True,
            "split_max": 4,                 # this means, we can have a max of 4 hands after splitting
            # exceptions for Aces
            "surrender_against_ace": True,
            "split_max_aces": 2,
            "hit_after_split_aces": False,
            "double_after_split_aces": False,
            
        }
        for rule, default_value in default_table_rules.items():
            self.table_rules[rule] = self.table_rules.get(rule, default_value)

        self._shoe = shoe
        self._shoe.set_number_of_decks(self.table_rules['number_of_decks'])

        self.number_of_spots = number_of_spots
        self._spots = [{
            "player": None,
            "hands": [],    # to get the number of splits, we can just take the length of `hands`
        } for _ in range(self.number_of_spots)]

        self._dealer = Dealer(**self.table_rules)
        self._dealer_hand = None

        self._verbose = verbose
        self._last_hand = False

    def __repr__(self):
        os.system('cls||clear')
        out = ""
        out += f"Dealer: {'' if self._dealer_hand is None else self._dealer_hand}\n"
        out += "-" * 20 + '\n'
        for i, spot in enumerate(self._spots):
            out += f"Spot {i+1}: "
            if spot['player'] is None:
                out += '\n'
                continue
            out += str(spot['player'])
            for hand in spot['hands']:
                out += "\n\t" + str(hand)
            out += '\n'
        out += "-" * 20 + '\n'
        return out


    """ Adding/Removing Players """

    def add_player(self, player, spot_index=None):
        # find the next available spot
        if spot_index is None:
            for i in range(len(self._spots)):
                if self._spots[i]['player'] is None:
                    self._spots[i]['player'] = player
                    return
            raise ValueError("There are no spots available")
        if self._spots[spot_index] is None:
            raise IndexError("Spot already occupied.")
        self._spots[spot_index]['player'] = player

    def remove_player(self, spot_index):
        player = self._spot[spot_index]
        self._spots[spot_index] = {
            "player": None,
            "hands": [],
        }
        return player


    """ Dealing and Managing Cards """

    def get_dealer_upcard(self):
        if self._dealer_hand is None:
            return None
        return self._dealer_hand.cards[0]
    
    def get_dealer_hole_card(self):
        if self._dealer_hand is None:
            return None
        if len(self._dealer_hand) < 2:
            return None
        return self._dealer_hand.cards[1]

    def get_next_card(self):
        card = self._shoe.deal()
        if card == CutCard():
            if self._verbose:
                print("\nDealer pulled cut card, this is the last hand")
                input("Press ENTER to continue ")
            self._last_hand = True
            card = self._shoe.deal()
        return card

    def show_card(self, card):
        for spot in self._spots:
            if spot['player'] is None:
                continue

            spot['player'].see_dealt_card(card)


    """ Game Procedure Logic """

    def _prepare_new_shoe(self):
        self._shoe.shuffle()
        if self._shoe.name != "Stacked Shoe":   # Stacked Shoe is just used for testing, but it doesn't work if we cut
            self._shoe.cut()
        self._shoe.place_cut_card()
        self._shoe.burn_card()            # not sure why, but they always burn the first card

    def _clear_table(self):
        for spot in self._spots:
            if spot['player'] is None:
                continue
            spot['hands'] = []
        
        self._dealer_hand = None

        if self._verbose:
            print(self)
            input("Press ENTER to continue ")

    def _initialize_bets_and_hands(self):
        if self._verbose:
            print("\nPlayer Bets")

        # Initialize players' hands and bets
        for spot in self._spots:
            player = spot['player']
            if player is None:
                continue
            
            bet = player.bet()
            if bet < self.table_rules['min_bet']:
                if self._verbose:
                    print(f"\t{player.name}'s bet of ${bet} is less than the minimum, they are sitting out this round")
                player.recieve_chips(bet)
                continue
            # we are going to ignore this case so it's easier to see the differential
            # if bet > player.chips:
            #     print("You don't have enough chips to make that bet, you are sitting out this round")
            #     player.recieve_chips(bet)
            #     continue
            if bet > self.table_rules['max_bet']:
                if self._verbose:
                    print(f"\t{player.name} bet over the maximum, the bet of {bet} is being reduced to {self.table_rules['max_bet']}")
                player.recieve_chips(bet - self.table_rules['max_bet'])
                bet = self.table_rules['max_bet']
                continue
            
            if self._verbose:
                print(f"\t{player.name} bets ${bet}")
            player.bet_chips(bet)
            spot['hands'] = [Hand(bet)]
        
        # Initialize dealer's hand
        self._dealer_hand = DealerHand()

        if self._verbose:
            input("\nPress ENTER to continue ")

    def _initial_deal(self):
        if self._verbose:
            print("\nDealing initial cards")
            input("Press ENTER to continue ")

        # deal first card to players
        for spot in self._spots:
            if spot['player'] is None or len(spot['hands']) == 0:
                continue
            card = self.get_next_card()
            self.show_card(card)
            spot['hands'][0].add_card(card)
        
        # deal first card to dealer
        card = self.get_next_card()
        self.show_card(card)
        self._dealer_hand.add_card(card)

        # deal second cards to players
        for spot in self._spots:
            if spot['player'] is None or len(spot['hands']) == 0:
                continue
            card = self.get_next_card()
            self.show_card(card)
            spot['hands'][0].add_card(card)
        
        # deal second card to dealer
        card = self.get_next_card()
        # DO NOT SHOW, IT IS HIDDEN
        self._dealer_hand.add_card(card)

        if self._verbose:
            print(self)
            input("Press ENTER to continue ")

    # Insurance and even money are mathematically equivalent 
    # The only meaningful difference is that insurance forces you to actually bet chips where as even money does not
    # Therefore, it's possible that you might not have enough chips to buy insurance, but you could still take even money
    # However you can only take even money if you have BlackJack
    def _ask_for_insurance_and_even_money(self, dealer_upcard):
        if self._verbose:
            print("\nAsking for insurance and even money")
        
        for spot in self._spots:
            player = spot['player']
            if player is None:
                continue
            for hand in spot['hands']:
                if hand.is_blackjack():
                    # technically, a player with blackjack could take insurance, but they are mathematically equivalent
                    # and even money is better in some instances because you don't have to have money to bet
                    if player.take_even_money(hand, dealer_upcard):
                       hand.take_even_money()
                       self._pay_out_player(player, hand.bet, multiplier=2, info="from even money")
                    else:
                        if self._verbose:
                            print(f"\t{player.name} rejects even money")
                else:
                    if player.take_insurance(hand, dealer_upcard):
                        hand.take_insurance()
                        player.bet_chips(hand.bet // 2)
                        if self._verbose:
                            print(f"\t{player.name} took insurance and bets ${hand.bet // 2}")
                    else:
                        if self._verbose:
                            print(f"\t{player.name} rejects insurance")
        
        if self._verbose:
            input("\nPress ENTER to continue ")

    def _pay_out_insurance(self):
        if self._verbose:
            print("Paying out insurance and even money")
        for spot in self._spots:
            player = spot['player']
            if player is None:
                continue
            for hand in spot['hands']:
                if hand.insurance:
                    self._pay_out_player(player, bet=hand.bet//2, multiplier=3, info="from insurance bet")
                    hand.insurance = False  # I just have to set this so it doesn't display anymore
        
        if self._verbose:
            input("Press ENTER to continue ")

    def _resolve_player_spot(self, spot, dealer_upcard):
        player = spot['player']
        if player is None:
            return
        
        all_hands_resolved = False
        while not all_hands_resolved:

            for i in range(len(spot['hands'])):
                hand = spot['hands'][i]
                self._resolve_player_hand(player, spot, hand, i, dealer_upcard)

                # This only occurs if there was a split, in which case, the code just starts over and evaluates hands left-to-right
                if not hand.is_resolved:
                    if self._verbose:
                        print(self)
                        input("Press ENTER to continue ")
                    break
            else:
                # This only executes if we never break from the for-loop
                # Thus, all hands must be resolved
                all_hands_resolved = True
    
    def _resolve_player_hand(self, player, spot, hand, hand_index, dealer_upcard):
        if hand.is_resolved:
            return
        if hand.is_21():
            if self._verbose:
                print(f"\n{player.name} 21!")
                input("Press ENTER to continue ")
            hand.resolve()
            return
        if hand.is_busted():
            if self._verbose:
                print(f"\n{player.name} busted :(")
                input("Press ENTER to continue ")
            hand.resolve()
            return

        allowed_actions = self.get_allowed_player_actions(hand, len(spot['hands']), dealer_upcard)
        action =  allowed_actions[0] if len(allowed_actions) == 1 else player.action(hand, dealer_upcard, allowed_actions)

        if action not in allowed_actions:
            if self._verbose:
                print(f"\n{player.name} wants to {action}, but only {allowed_actions} is allowed. Thus, they will STAND")
                input("Press ENTER to continue ")

        if self._verbose:
            print(f"\n{player.name}: {action}")
            input("Press ENTER to continue ")

        if action == Action.STAND:
            hand.resolve()
        
        elif action == Action.HIT:
            card = self.get_next_card()
            self.show_card(card)
            hand.add_card(card)
        
        elif action == Action.DOUBLE:
            player.bet_chips(hand.bet)  # double the bet
            hand.double_down()

            card = self.get_next_card()
            self.show_card(card)
            hand.add_card(card)

            if self._verbose:
                print(self)
                input("Press ENTER to continue ")
            hand.resolve()  # the hand is finished because we doubled
        
        elif action == Action.SPLIT:
            player.bet_chips(hand.bet)  # double the bet
            h1 = Hand(hand.bet, hand.cards[0])
            h2 = Hand(hand.bet, hand.cards[1])
            spot['hands'] = spot['hands'][:hand_index] + [h1, h2] + spot['hands'][hand_index+1:]

        else:
            raise ValueError(f"Exptected one of {allowed_actions}, instead got {action}")

    def _resolve_dealer_spot(self):
        
        self._dealer_hand.reveal_hole_card()
        if self._verbose:
            print(self)
            input("Press ENTER to continue ")
        
        while not self._dealer_hand.is_resolved:
            self._resolve_dealer_hand()

            if self._verbose:
                print(self)
                input("Press ENTER to continue ")

    def _resolve_dealer_hand(self):
        if self._dealer_hand.is_resolved:
            return
        if self._dealer_hand.is_21():
            if self._verbose:
                print("\nDealer 21 :(")
                input("Press ENTER to continue ")
            self._dealer_hand.resolve()
            return
        if self._dealer_hand.is_busted():
            if self._verbose:
                print("\nDealer Bust!")
                input("Press ENTER to continue ")
            self._dealer_hand.resolve()
            return

        allowed_actions = self.get_allowed_dealer_actions(self._dealer_hand)
        action = self._dealer.action(self._dealer_hand, allowed_actions)
        if self._verbose:
            print(f"\n{self._dealer.name}: {action}")
            input("Press ENTER to continue ")

        if action == Action.STAND:
            self._dealer_hand.resolve()
        elif action == Action.HIT:
            card = self.get_next_card()
            self.show_card(card)
            self._dealer_hand.add_card(card)
        else:
            raise ValueError(f"Exptected one of {allowed_actions}, instead got {action}")

    # I had to move this to its over function because it made the logic much easier
    def _is_split_allowed(self, hand, number_of_hands):
        if self.table_rules["split_max"] < 2:
            return False
        if hand.cards[0].value != hand.cards[1].value:
            return False
        if hand.cards[0].pip == "A":
            return number_of_hands < self.table_rules["split_max_aces"]
        return number_of_hands < self.table_rules["split_max"]

    def get_allowed_player_actions(self, hand, number_of_hands, dealer_upcard):
        # len(hand) == 1 right after splits, the player automatically get another card
        if len(hand) == 1:
            return [Action.HIT]
        
        # Some casinos only let you get 1 card after splitting aces
        if number_of_hands > 1 and hand.cards[0].pip == 'A' and (not self.table_rules["hit_after_split_aces"]):
            return [Action.STAND]

        allowed_actions = [Action.STAND, Action.HIT]

        if len(hand) == 2:
            
            # Action.DOUBLE
            if number_of_hands == 1:                    # if it's our first hand, we can double
                allowed_actions.append(Action.DOUBLE)
            elif hand.cards[0].pip == "A" and self.table_rules["double_after_split_aces"]:              # we split aces
                allowed_actions.append(Action.DOUBLE)
            elif self.table_rules["double_after_split"]:
                allowed_actions.append(Action.DOUBLE)

            # Action.SPLIT
            if self._is_split_allowed(hand, number_of_hands):
                allowed_actions.append(Action.SPLIT)
            
            # Action.SURRENDER
            if dealer_upcard.pip == "A" and self.table_rules["surrender_against_ace"]:
                allowed_actions.append(Action.SURRENDER)
            elif self.table_rules["late_surrender"]:
                allowed_actions.append(Action.SURRENDER)
        
        return allowed_actions

    def get_allowed_dealer_actions(self, dealer_hand):
        return [Action.STAND, Action.HIT]

    def _evaluate_spots(self):
        if self._verbose:
            print("\nEvaluating Hands")

        for spot in self._spots:
            player = spot['player']
            if player is None:
                continue
            for hand in spot['hands']:
                self._evaluate_player_hand(player, hand, self._dealer_hand)

        if self._verbose:
            input("Press ENTER to continue ")

    def _pay_out_player(self, player, bet, multiplier, info="", push=False):
        player.recieve_chips(int(bet * multiplier))
        if self._verbose:
            if multiplier == 1:
                print(f"\t{player.name} PUSHES {info} (${bet})")
            else:
                print(f"\t{player.name} WINS {info} (${bet} * {multiplier})")

    def _evaluate_player_hand(self, player, hand, dealer_hand):
        
        # Note: BlackJack means you specifically have an A + 10-valued card. This is different than just a 21, which could be K, 5, 6 for example
        # Note that insurance and even money has already been paid out
        
        # If you have BlackJack then you win no matter what (even if the dealer has 21) and get your bet * the multiplyer
        if hand.is_blackjack():
            # The only exception is if the dealer also has a BlackJack
            if dealer_hand.is_blackjack():
                self._pay_out_player(player, hand.bet, multiplier=1, info=f"{hand.get_comparison_total()} = {dealer_hand.get_comparison_total()}")
                return
            
            # Also, if you took even money, then this was already paid out
            if hand.even_money:
                if self._verbose:
                    print(f"\t{player.name} took even money and was already paid out")
                return

            self._pay_out_player(player, bet=hand.bet, multiplier=1 + self.table_rules['blackjack_multiplier'], info="from BlackJack")
            return
        
        # If you bust, you lose no matter what (even if the dealer busts)
        if hand.is_busted():
            if self._verbose:
                print(f"\t{player.name} loses by busting :(")
            return
        
        # if you didn't bust, but the dealer does bust, then you win no matter what
        if dealer_hand.is_busted():
            if hand.is_doubled:
                self._pay_out_player(player, hand.bet, multiplier=4, info="by dealer bust")
            else:
                self._pay_out_player(player, hand.bet, multiplier=2, info="by dealer bust")
            return

        # otherwise, we compare hand totals
        if hand > dealer_hand:      # win
            if hand.is_doubled:
                self._pay_out_player(player, hand.bet*2, multiplier=2, info=f"{hand.get_comparison_total()} > {dealer_hand.get_comparison_total()}")
            else:
                self._pay_out_player(player, hand.bet, multiplier=2, info=f"{hand.get_comparison_total()} > {dealer_hand.get_comparison_total()}")
        elif hand == dealer_hand:   # push
            if hand.is_doubled:
                self._pay_out_player(player, hand.bet*2, multiplier=1, info=f"{hand.get_comparison_total()} = {dealer_hand.get_comparison_total()}", push=True)
            else:
                self._pay_out_player(player, hand.bet, multiplier=1, info=f"{hand.get_comparison_total()} = {dealer_hand.get_comparison_total()}", push=True)
        else:                       # lose
            # We don't need to take away more chips because this was already done
            # When you bet they are subtracted already
            if self._verbose:
                print(f"\t{player.name} LOSES {hand.get_comparison_total()} < {dealer_hand.get_comparison_total()}")

    def _play_round(self):
        
        # Initialize Table
        self._clear_table()
        self._initialize_bets_and_hands()
        self._initial_deal()

        dealer_upcard = self.get_dealer_upcard()

        # if the dealer shows an A, the players are allowed to take insurance
        # if the player has a blackjack, then they can take even money (which is mathematically the same as insurance)
        if dealer_upcard.pip == 'A':
            if self.table_rules["early_surrender"] and self.table_rules["dealer_peaks_for_blackjack"]:
                # TODO: implement early surrender
                pass

            # ask for insurance/even money
            if self.table_rules["insurance_and_even_money"]:
                self._ask_for_insurance_and_even_money(dealer_upcard)

        # if the dealer has an A or any 10-valued card, they check if they have a blackjack
        if dealer_upcard.pip in ['A', 'T', 'J', 'Q', 'K'] and self.table_rules["dealer_peaks_for_blackjack"]:
            if self._dealer_hand.is_21():
                
                self._dealer_hand.reveal_hole_card()
                if self._verbose:
                    print(self)
                    print("Dealer has BlackJack :(")
                    input("Press ENTER to continue ")

                if self.table_rules["insurance_and_even_money"]:
                    self._pay_out_insurance()
                    if self._verbose:
                        print(self)
                        input("Press ENTER to continue ")

                # No one gets action. Everyone loses unless they were dealt a 21, in which they push
                self._evaluate_spots()
                
                return
            else:
                if self._verbose:
                    print("\nDealer does not have BlackJack!")
        
        # Note: If we have reached this point, it means the dealer does not have a BlackJack
        # Even money is dealt with immediately when the player accepts it and insurance is resolved above
        # Since the player lost their insurance bet, we don't have to do anything (the chips were already taken)
        
        # Iterate through players and get their action
        if self._verbose:
            print("\nGetting player action")
            input("Press ENTER to continue ")
        for spot in self._spots:
            self._resolve_player_spot(spot, dealer_upcard)

        # dealer does their action
        if self._verbose:
            print("\nGetting dealer action")
            input("Press ENTER to continue ")
        self._resolve_dealer_spot()
        
        # compare player and dealer hands and pay/take bets
        self._evaluate_spots()

        if self._verbose:
            print(self)
            input("Press ENTER to continue ")

    def play(self, number_of_rounds=math.inf, count_rounds=True):
        self._prepare_new_shoe()
        round_number = 0
        while round_number < number_of_rounds:
            
            if self._last_hand:
                if self._verbose:
                    print("\nReshuffle")
                    input("Press ENTER to continue ")
                self._prepare_new_shoe()
                self._last_hand = False

                # let player functions know it's a new show
                for spot in self._spots:
                    player = spot['player']
                    if player is None:
                        continue
                    player.new_shoe()

            if count_rounds:
                print("Round:", round_number+1)
            self._play_round()
            round_number += 1


if __name__ == "__main__":
    from Players import HumanPlayer, BasicStrategyPlayer, CardCountingPlayer
    from Shoes import FairShoe, StackedShoe

    table_rules = {
        "hit_after_split_aces": True,
        "double_after_split_aces": True,
    }

    Table = BlackJackTable(shoe=StackedShoe(), number_of_spots=8, verbose=True, **table_rules)
    print(Table)
    input("Press ENTER to continue ")

    BS = BasicStrategyPlayer(name="BS", chips=0, **table_rules)
    Table.add_player( BS, 2 )

    CC = CardCountingPlayer(name="CC", chips=0, **table_rules)
    Table.add_player( CC, 5 )
    # Table.add_player( CC, 6 )

    # Eric = HumanPlayer(name="Eric", chips=0, **table_rules)
    # Table.add_player( Eric, 3 )
    
    Table.play()