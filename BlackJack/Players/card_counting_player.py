from .basic_strategy_player import BasicStrategyPlayer
from action import Action

from prettytable import PrettyTable

class CardCountingPlayer(BasicStrategyPlayer):

    # they are almost identical, with only a few differences, but I took the lazy approach
    S17_deviations = {
        "-1-": [
            {"type": "hard_hits", "player": 13, "dealer": 2},
            {"type": "hard_surrenders", "player": 16, "dealer": 9},
        ],
        "-1+": [],
        "0-": [
            {"type": "hard_hits", "player": 12, "dealer": 4},
            {"type": "hard_surrenders", "player": 15, "dealer": 10},
        ],
        "0+": [
            {"type": "hard_hits", "player": 16, "dealer": 10},
        ],
        "1+": [
            {"type": "hard_doubles", "player": 9, "dealer": 2},
            {"type": "hard_doubles", "player": 11, "dealer": 1},
            {"type": "soft_doubles", "player": 7, "dealer": 2},
            {"type": "soft_doubles", "player": 9, "dealer": 5},
            {"type": "soft_doubles", "player": 9, "dealer": 6},
        ],
        "2+": [
            {"type": "hard_hits", "player": 12, "dealer": 3},
            {"type": "hard_doubles", "player": 8, "dealer": 6},
            {"type": "hard_surrenders", "player": 15, "dealer": 9},
            {"type": "hard_surrenders", "player": 15, "dealer": 1},
        ],
        "3+": [
            {"type": "hard_hits", "player": 12, "dealer": 2},
            {"type": "hard_hits", "player": 16, "dealer": 1},
            {"type": "hard_doubles", "player": 9, "dealer": 7},
            {"type": "soft_doubles", "player": 9, "dealer": 4},
            {"type": "splits", "player": 9, "dealer": 7},
            
        ],
        "4+": [
            {"type": "hard_hits", "player": 15, "dealer": 10},
            {"type": "hard_hits", "player": 16, "dealer": 9},
            {"type": "hard_doubles", "player": 10, "dealer": 10},
            {"type": "hard_doubles", "player": 10, "dealer": 1},
            {"type": "hard_surrenders", "player": 16, "dealer": 8},
            {"type": "splits", "player": 10, "dealer": 6},
        ],
        "5+": [
            {"type": "hard_hits", "player": 15, "dealer": 1},
            {"type": "splits", "player": 10, "dealer": 5},
        ],
        "6+": [
            {"type": "splits", "player": 10, "dealer": 4},
        ],
    }
    
    H17_deviations = {
        "-1-": [
            {"type": "hard_hits", "player": 13, "dealer": 2},
            {"type": "hard_surrenders", "player": 16, "dealer": 9},
        ],
        "-1+": [
            {"type": "hard_surrenders", "player": 15, "dealer": 1},
        ],
        "0-": [
            {"type": "hard_hits", "player": 12, "dealer": 4},
            {"type": "hard_surrenders", "player": 15, "dealer": 10},
            {"type": "soft_doubles", "player": 9, "dealer": 6},
        ],
        "0+": [
            {"type": "hard_hits", "player": 16, "dealer": 10},
        ],
        "1+": [
            {"type": "hard_doubles", "player": 9, "dealer": 2},
            {"type": "soft_doubles", "player": 7, "dealer": 2},
            {"type": "soft_doubles", "player": 9, "dealer": 5},
        ],
        "2+": [
            {"type": "hard_hits", "player": 12, "dealer": 3},
            {"type": "hard_doubles", "player": 8, "dealer": 6},
            {"type": "hard_surrenders", "player": 15, "dealer": 9},
        ],
        "3+": [
            {"type": "hard_hits", "player": 12, "dealer": 2},
            {"type": "hard_hits", "player": 16, "dealer": 1},
            {"type": "hard_doubles", "player": 9, "dealer": 7},
            {"type": "hard_doubles", "player": 10, "dealer": 1},
            {"type": "soft_doubles", "player": 9, "dealer": 4},
            {"type": "splits", "player": 9, "dealer": 7},
            
        ],
        "4+": [
            {"type": "hard_hits", "player": 15, "dealer": 10},
            {"type": "hard_hits", "player": 16, "dealer": 9},
            {"type": "hard_doubles", "player": 10, "dealer": 10},
            {"type": "splits", "player": 10, "dealer": 6},
            {"type": "hard_surrenders", "player": 16, "dealer": 8},
        ],
        "5+": [
            {"type": "hard_hits", "player": 15, "dealer": 1},
            {"type": "splits", "player": 10, "dealer": 5},
        ],
        "6+": [
            {"type": "splits", "player": 10, "dealer": 4},
        ],
    }

    def __init__(self, name, chips=0, **table_rules):
        super(CardCountingPlayer, self).__init__(name=name, chips=chips, **table_rules)
        self.running_count = 0
        self.num_cards_dealt = 1

    def __repr__(self):
        player_str = super(CardCountingPlayer, self).__repr__()
        true_count = self._calculate_true_count()
        return f"{player_str}\tRC: {self.running_count}\tTC: {true_count}"

    def _get_hard_totals_table(self):
        hard_totals = super(CardCountingPlayer, self)._get_hard_totals_table()
        if not self.show_deviations:
            return hard_totals
        deviations = self.H17_deviations if self.table_rules["hit_on_soft_17"] else self.S17_deviations
        fg = '\033[31m'
        for TC, dev_list in deviations.items():
            if len(TC) == 2:
                TC = " " + TC
            for dev in dev_list:
                p, d = dev["player"], dev["dealer"]
                if dev["type"] in ["hard_hits", "hard_doubles", "hard_surrenders"]:
                    color, text, reset = hard_totals[p-2][d-1]
                    hard_totals[p-2][d-1] = (color+fg, TC, reset)
        return hard_totals
    
    def _get_soft_totals_table(self):
        soft_totals = super(CardCountingPlayer, self)._get_soft_totals_table()
        if not self.show_deviations:
            return soft_totals
        deviations = self.H17_deviations if self.table_rules["hit_on_soft_17"] else self.S17_deviations
        fg = '\033[31m'
        for TC, dev_list in deviations.items():
            if len(TC) == 2:
                TC = " " + TC
            for dev in dev_list:
                p, d = dev["player"], dev["dealer"]
                if dev["type"] in ["soft_hits", "soft_doubles", "soft_surrenders"]:
                    color, text, reset = soft_totals[p-2][d-1]
                    soft_totals[p-2][d-1] = (color+fg, TC, '\033[0m')
        return soft_totals

    def _get_splits_table(self):
        splits = super(CardCountingPlayer, self)._get_splits_table()
        if not self.show_deviations:
            return splits
        deviations = self.H17_deviations if self.table_rules["hit_on_soft_17"] else self.S17_deviations
        fg = '\033[31m'
        for TC, dev_list in deviations.items():
            if len(TC) == 2:
                TC = " " + TC
            for dev in dev_list:
                c = dev["player"]
                d = dev["dealer"]
                if dev["type"] == "splits":
                    color, text, reset = splits[c-1][d-1]
                    splits[c-1][d-1] = (color+fg, TC, '\033[0m')
        return splits

    def display_strategy(self, true_count=0, show_deviations=True):
        self._toggle_deviations(true_count)
        self.show_deviations = show_deviations
        print("True Count:", true_count)
        super(CardCountingPlayer, self).display_strategy()
        self._toggle_deviations(true_count)

    def _calculate_true_count(self):
        num_decks_remaining = (self.table_rules["number_of_decks"]) - (self.num_cards_dealt/52)
        if num_decks_remaining == 0:
            return -10
        return self.running_count / num_decks_remaining

    # The deviations essentially flip 1 bit. So, call this function, calcualte your action, then call it again so that the tables all go back to basic strategy
    def _toggle_deviations(self, true_count):
        deviations = self.H17_deviations if self.table_rules["hit_on_soft_17"] else self.S17_deviations
        if true_count <= -1:
            self._apply_deviations(deviations["-1-"])
        if true_count >= -1:
            self._apply_deviations(deviations["-1+"])
        if true_count < 0:
            self._apply_deviations(deviations["0-"])
        if true_count > 0:
            self._apply_deviations(deviations["0+"])
        for i in range(1, 7):
            if true_count > 1:
                self._apply_deviations(deviations[f"{i}+"])
        
    def new_shoe(self):
        self.running_count = 0
        self.num_cards_dealt = 1    # initialize at 1 bc of the burn card at the beginning of a new shoe

    def see_dealt_card(self, card):
        self.num_cards_dealt += 1

        # make update to running count
        if 2 <= card.value <= 6:
            self.running_count += 1
        if card.value == 1 or card.value == 10:
            self.running_count -= 1

    def action(self, hand, dealer_card, allowed_actions):
        true_count = self._calculate_true_count()
        self._toggle_deviations(true_count)
        action = super(CardCountingPlayer, self).action(hand=hand, dealer_card=dealer_card, allowed_actions=allowed_actions)
        self._toggle_deviations(true_count)
        return action
    
    def bet(self):
        # index from -3 to +6
        multipliers = [0, 0, 0, 1, 1, 2, 3, 4, 5, 5, 5]  # I made this up, there are probably better spreads
        true_count = self._calculate_true_count()
        TC = max(min(int(true_count), 6), -3)
        return self.table_rules["min_bet"] * multipliers[TC + 3]

if __name__ == "__main__":
    from hand import Hand
    from card import Card

    CC = CardCountingPlayer("CC", **{'double_after_split': True, 'hit_on_soft_17': False})
    CC.display_strategy(true_count=0)
    # print("\n\n")
    # CC.display_strategy(true_count=0)

    # print()
    # actions = [Action.HIT, Action.STAND, Action.DOUBLE, Action.SURRENDER, Action.SPLIT]
    # action = CC.action(Hand(0, Card("AD"), Card("AH")), Card(f"2D"), allowed_actions=actions)
    # print(action)

    # print(CC.splits[1-1][2-1])
    # for row in CC.splits:
    #     print(row)

    # print("\n\n")
    # first_card = Card("2C")
    # for pip in ["2", "3", "4", "5", "6", "7", "8", "9", "J", "K", "A"]:
    #     second_card = Card(f"{pip}D")
    #     if first_card.value == second_card.value:
    #         actions = [Action.HIT, Action.STAND, Action.DOUBLE, Action.SURRENDER, Action.SPLIT]
    #     else:
    #         actions = [Action.HIT, Action.STAND, Action.DOUBLE, Action.SURRENDER]
    #     hand = Hand(0, first_card, second_card)
        
    #     print(hand, [
    #         CC.action(hand, Card(f"{dealer_pip}D"), allowed_actions=actions) for dealer_pip in ["2", "3", "4", "5", "6", "7", "8", "9", "J", "K", "A"]
    #     ])