import os
import math

from card import CutCard
from shoe import Shoe
from player import Dealer
from hand import Hand, DealerHand
from action import Action

class BlackJackTable(object):

    """
    This is essentially the game engine
    """

    def __init__(self, shoe, number_of_spots=8, verbose=False, **table_rules):
        
        self.table_rules = table_rules
        default_table_rules = {
            "min_bet": 10,
            "max_bet": 1000,
            "hit_on_soft_17": False,
            "double_after_split": True,
            "late_surrender": True,
            "number_of_decks": 6,
            "blackjack_multiplier": 1.5,
        }
        for rule, default_value in default_table_rules.items():
            self.table_rules[rule] = self.table_rules.get(rule, default_value)

        self._shoe = shoe
        self._shoe.set_number_of_decks(self.table_rules['number_of_decks'])

        self.number_of_spots = number_of_spots
        self._spots = [{
            "player": None,
            "hands": [],
        } for _ in range(self.number_of_spots)]

        self._dealer_spot = {
            "player": Dealer(**self.table_rules),
            "hand": None,
        }

        self.verbose = verbose
        self.last_hand = False

    def __repr__(self):
        os.system('cls||clear')
        out = ""
        out += f"Dealer: {'' if self._dealer_spot['hand'] is None else self._dealer_spot['hand']}\n"
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

    def add_player(self, player, spot_index):
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
        if self._dealer_spot['hand'] is None:
            return None
        return self._dealer_spot['hand'].cards[0]
    
    def get_dealer_hole_card(self):
        if self._dealer_spot['hand'] is None:
            return None
        if len(self._dealer_spot['hand']) < 2:
            return None
        return self._dealer_spot['hand'].cards[1]

    def get_next_card(self):
        card = self._shoe.deal()
        if card == CutCard():
            if self.verbose:
                print("\nDealer pulled cut card, this is the last hand")
                input("Press ENTER to continue ")
            self.last_hand = True
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
        self._shoe.cut()
        self._shoe.place_cut_card()

    def _clear_table(self):
        for spot in self._spots:
            if spot['player'] is None:
                continue
            spot['hands'] = []
        
        self._dealer_spot['hand'] = None

    def _initialize_bets_and_hands(self):
        # Initialize players' hands and bets
        for spot in self._spots:
            player = spot['player']
            if player is None:
                continue
            
            bet = player.bet()
            if bet < self.table_rules['min_bet']:
                if self.verbose:
                    print(f"\n{player.name}'s bet of ${bet} is less than the minimum, they are sitting out this round")
                    input("Press ENTER to continue ")
                player.recieve_chips(bet)
                continue
            # we are going to ignore this case so it's easier to see the differential
            # if bet > player.chips:
            #     print("You don't have enough chips to make that bet, you are sitting out this round")
            #     player.recieve_chips(bet)
            #     continue
            if bet > self.table_rules['max_bet']:
                if self.verbose:
                    print(f"\n{player.name} bet over the maximum, the bet of {bet} is being reduced to {self.table_rules['max_bet']}")
                    input("Press ENTER to continue ")
                player.recieve_chips(bet - self.table_rules['max_bet'])
                bet = self.table_rules['max_bet']
                continue
            
            if self.verbose:
                print(f"\n{player.name} bets ${bet}")
                input("Press ENTER to continue ")
            player.bet_chips(bet)
            spot['hands'] = [Hand(bet)]
        
        # Initialize dealer's hand
        self._dealer_spot['hand'] = DealerHand()

    def _initial_deal(self):
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
        self._dealer_spot['hand'].add_card(card)

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
        self._dealer_spot['hand'].add_card(card)

    def _resolve_player_spot(self, spot, dealer_upcard):
        player = spot['player']
        if player is None:
            return
        
        all_hands_resolved = False
        while not all_hands_resolved:

            for i in range(len(spot['hands'])):
                hand = spot['hands'][i]
                self._resolve_player_hand(player, hand, dealer_upcard)

                if self.verbose:
                    print(self)
                    input("Press ENTER to continue ")
                
                # This isn't super elegant, but it works
                if hand.is_split:
                    h1 = Hand(hand.bet, hand.cards[0])
                    h2 = Hand(hand.bet, hand.cards[1])
                    spot['hands'] = spot['hands'][:i] + [h1, h2] + spot['hands'][i+1:]

                    if self.verbose:
                        print(self)
                        input("Press ENTER to continue ")
                    break
                if not hand.is_resolved:
                    break
            else:
                # This only executes if we never break from the for-loop
                # Thus, all hands must be resolved
                all_hands_resolved = True
    
    def _resolve_player_hand(self, player, hand, dealer_card):
        if hand.is_resolved:
            return
        if hand.is_21():
            if self.verbose:
                print(f"\n{player.name} 21!")
                input("Press ENTER to continue ")
            hand.resolve()
            return
        if hand.is_busted():
            if self.verbose:
                print(f"\n{player.name} busted :(")
                input("Press ENTER to continue ")
            hand.resolve()
            return

        allowed_actions = self.get_allowed_player_actions(hand)
        action = player.action(hand, dealer_card, allowed_actions)
        if self.verbose:
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

            hand.resolve()  # the hand is finished because we doubled
        
        elif action == Action.SPLIT:
            player.bet_chips(hand.bet)  # double the bet
            hand.split()

        else:
            raise ValueError(f"Exptected one of {allowed_actions}, instead got {action}")

    def _resolve_dealer_spot(self, dealer_spot):
        dealer = dealer_spot['player']
        if dealer is None:
            return
        
        hand = dealer_spot['hand']
        while not hand.is_resolved:
            self._resolve_dealer_hand(dealer, hand)

            if self.verbose:
                print(self)
                input("Press ENTER to continue ")

    def _resolve_dealer_hand(self, dealer, hand):
        if hand.is_resolved:
            return
        if hand.is_21():
            if self.verbose:
                print("\nDealer 21 :(")
                input("Press ENTER to continue ")
            hand.resolve()
            return
        if hand.is_busted():
            if self.verbose:
                print("\nDealer Bust!")
                input("Press ENTER to continue ")
            hand.resolve()
            return

        allowed_actions = self.get_allowed_dealer_actions(hand)
        action = dealer.action(hand, allowed_actions)
        if self.verbose:
            print(f"\n{dealer.name}: {action}")
            input("Press ENTER to continue ")

        if action == Action.STAND:
            hand.resolve()
        elif action == Action.HIT:
            card = self.get_next_card()
            self.show_card(card)
            hand.add_card(card)
        else:
            raise ValueError(f"Exptected one of {allowed_actions}, instead got {action}")

    def get_allowed_player_actions(self, hand):
        allowed_actions = [Action.STAND, Action.HIT]
        if len(hand) == 2:
            allowed_actions.append(Action.DOUBLE)
            if hand.cards[0].value == hand.cards[1].value:
                allowed_actions.append(Action.SPLIT)
        return allowed_actions

    def get_allowed_dealer_actions(self, hand):
        return [Action.STAND, Action.HIT]

    def _evaluate_spots(self):
        dealer_hand = self._dealer_spot['hand']
        for spot in self._spots:
            player = spot['player']
            if player is None:
                continue
            for hand in spot['hands']:
                self._evaluate_player_hand(player, hand, dealer_hand)

                if self.verbose:
                    print(self)
                    input("Press ENTER to continue ")

    def _evaluate_player_hand(self, player, hand, dealer_hand):
        # If you are dealt a 21 then you win no matter what and get your bet * the multiplyer
        if len(hand) == 2 and hand.is_21():
            if self.verbose:
                    print(f"\n{player.name} has 21! and wins ${int(hand.bet * (1 + self.table_rules['blackjack_multiplier']))}")
                    input("Press ENTER to continue ")
            player.recieve_chips(int(hand.bet * (1 + self.table_rules['blackjack_multiplier'])))
            return
        
        # If you bust, you lose no matter what (even if the dealer busts)
        if hand.is_busted():
            if self.verbose:
                print(f"\n{player.name} busted")
                input("Press ENTER to continue ")
            return
        
        # if you didn't bust, but the dealer does bust, then you win no matter what
        if dealer_hand.is_busted():
            if self.verbose:
                print(f"\nDealer busted")
                input("Press ENTER to continue ")
            if hand.is_doubled:
                if self.verbose:
                    print(f"\n{player.name} wins ${hand.bet * 4}")
                    input("Press ENTER to continue ")
                player.recieve_chips(hand.bet * 4)
            else:
                if self.verbose:
                    print(f"\n{player.name} wins ${hand.bet * 2}")
                    input("Press ENTER to continue ")
                player.recieve_chips(hand.bet * 2)
            return

        # otherwise, we compare hand totals
        if hand > dealer_hand:      # win
            if hand.is_doubled:
                if self.verbose:
                    print(f"\n{player.name} wins ${hand.bet * 4}")
                    input("Press ENTER to continue ")
                player.recieve_chips(hand.bet * 4)
            else:
                if self.verbose:
                    print(f"\n{player.name} wins ${hand.bet * 2}")
                    input("Press ENTER to continue ")
                player.recieve_chips(hand.bet * 2)
        elif hand == dealer_hand:   # push
            if hand.is_doubled:
                if self.verbose:
                    print(f"\n{player.name} wins ${hand.bet * 2}")
                    input("Press ENTER to continue ")
                player.recieve_chips(hand.bet * 2)
            else:
                if self.verbose:
                    print(f"\n{player.name} wins ${hand.bet}")
                    input("Press ENTER to continue ")
                player.recieve_chips(hand.bet)
        else:                       # lose
            # We don't need to take away more chips because this was already done
            # When you bet they are subtracted already
            if self.verbose:
                print(f"\n{player.name} lost")
                input("Press ENTER to continue ")

    def _play_round(self):
        
        # Initialize Table
        self._clear_table()

        if self.verbose:
            print(self)
            input("Press ENTER to continue ")
        
        if self.verbose:
            print("\nPlace your bets")
            input("Press ENTER to continue ")
        self._initialize_bets_and_hands()
        
        if self.verbose:
            print("\nDealing initial cards")
            input("Press ENTER to continue ")
        self._initial_deal()

        if self.verbose:
            print(self)
            input("Press ENTER to continue ")

        # Iterate through players and get their action
        if self.verbose:
            print("\nGetting player action")
            input("Press ENTER to continue ")
        dealer_upcard = self.get_dealer_upcard()
        for spot in self._spots:
            self._resolve_player_spot(spot, dealer_upcard)

        # dealer does their action
        if self.verbose:
            print("\nGetting dealer action")
            input("Press ENTER to continue ")
        
        self._dealer_spot['hand'].reveal_hole_card()
        if self.verbose:
            print(self)
            input("Press ENTER to continue ")
        
        self._resolve_dealer_spot(self._dealer_spot)
        
        # compare player and dealer hands and pay/take bets
        self._evaluate_spots()

        if self.verbose:
            print(self)
            input("Press ENTER to continue ")

    def play(self, number_of_rounds=math.inf):
        self._prepare_new_shoe()
        round_number = 0
        while True:
            if round_number > number_of_rounds:
                break
            
            if self.last_hand:
                if self.verbose:
                    print("\nReshuffle")
                    input("Press ENTER to continue ")
                self._prepare_new_shoe()
                self.last_hand = False

                # let player functions know it's a new show
                for spot in self._spots:
                    player = spot['player']
                    if player is None:
                        continue
                    player.new_shoe()

            print("Round:", round_number)
            self._play_round()
            round_number += 1


if __name__ == "__main__":
    from player import Player, HumanPlayer, BasicStrategyPlayer, CardCountingPlayer
    from shoe import FairShoe, LowRunningCountShoe, ConstantlyReshufflingShoe

    table_rules = {
        "min_bet": 10,
        "max_bet": 1000,
        "hit_on_soft_17": False,
        "double_after_split": True,
        "late_surrender": True,
        "number_of_decks": 1,
        "blackjack_multiplier": 1.5,
    }

    Table = BlackJackTable(shoe=ConstantlyReshufflingShoe(), number_of_spots=8, verbose=True, **table_rules)
    print(Table)
    input("Press ENTER to continue ")

    Eric = BasicStrategyPlayer(name="Eric", chips=0, **table_rules)
    Table.add_player( Eric, 2 )

    Steven = CardCountingPlayer(name="Steven", chips=0, **table_rules)
    Table.add_player( Steven, 5 )
    
    Table.play()