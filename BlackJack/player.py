import math
from copy import deepcopy
from prettytable import PrettyTable

from card import Card
from action import Action

class Player(object):

    STAND = 1
    SPLIT = 2
    DOUBLE = 3
    HIT = 4

    def __init__(self, name, chips=0, **table_rules):
        self.name = name

        if type(chips) != int:
            raise TypeError(f"Expecting second argument to be an integer, got {chips} instead")
        
        self.chips = chips
        
        self.table_rules = table_rules
        default_table_rules = {
            "min_bet": 10,
            "max_bet": math.inf,
            "hit_on_soft_17": False,
            "double_after_split": True,
            "late_surrender": True,
            "number_of_decks": 6,
            "blackjack_multiplier": 1.5,
        }
        for rule, default_value in default_table_rules.items():
            self.table_rules[rule] = self.table_rules.get(rule, default_value)
        
        self.chip_history = [self.chips]

    def __repr__(self):
        return f"{self.name.title()} (${self.chips})"

    # function called any time a player is recieving chips (should not be altered)
    def recieve_chips(self, chips):
        self.chips += chips
        self.chip_history.append(self.chips)
    
    # function called any time a player bets chips (should not be altered)
    def bet_chips(self, chips):
        self.chips -= chips
        self.chip_history.append(self.chips)

    # function called for all new players when a new shoe starts
    def new_shoe(self):
        pass

    # function called any time a card is dealt
    def see_dealt_card(self, card):
        pass

    # function called to obtain players bet before they get their cards
    # this function SHOULD NOT modify self.chips (this will be done by a different object). Just return the bet amount
    def bet(self):
        raise NotImplementedError("Not yet implemented...")

    # function called to obtain player action for their hand
    def action(self, hand, dealer_card, allowed_actions):
        raise NotImplementedError("Not yet implemented...")
    
    # I don't feel like implementing these right now
    # def take_insurance(self):
    #     pass
    
    # def take_even_money(self):
    #     pass

    # function called after a hand with its result
    def see_hand_result(self, result):
        pass


class HumanPlayer(Player):

    def bet(self, min_bet, max_bet):
        b = input("Bet: ")
        try:
            b = int(b)
        except:
            # raise TypeError(f"Expected an integer, instead got {b}")
            print(f"Expected an integer, instead got {b}. Try Again")
            return self.bet(min_bet, max_bet)
        if b <= 0:
            print("You are sitting out this hand")
            return 0
        if b < min_bet:
            print(f"Bet must be larger than {min_bet}, instead got {b}. Try Again")
            return self.bet(min_bet, max_bet)
        if b > self.chips:
            print("You don't have that many chips, please try again.")
            return self.bet(min_bet, max_bet)
        if b > max_bet:
            print(f"Bet must be less than {max_bet}, instead got {b}. Try Again")
            return self.bet(min_bet, max_bet)
        self.chips -= b
        return b
    
    def action(self, hand, dealer_card, allowed_actions):
        # The way this is written to to ensure that the same number input always corrsponds to the same action
        #     (1) STAND    (2) HIT    (3) DOUBLE    (4) SPLIT    (5) SURRENDER
        # if one of them is not allowed, we don't have this
        #     (1) STAND    (2) HIT    (3) DOUBLE    (4) SURRENDER
        # instead we have this
        #     (1) STAND    (2) HIT    (3) DOUBLE    (5) SURRENDER
        print('    '.join([f"({i+1}) {action}" for i, action in enumerate(Action.all_actions()) if action in allowed_actions]))
        a = input("Action: ")
        try:
            a = int(a)
        except:
            raise TypeError(f"Expected an integer, instead got {a}")
        allowed_action_indices = [i+1 for i, action in enumerate(Action.all_actions()) if action in allowed_actions]
        if a not in allowed_action_indices:
            raise ValueError(f"Expected one of {allowed_action_indices}, instead got {a}")
        return Action.all_actions()[a-1]


class BasicStrategyPlayer(Player):

    """
    These tables apply to 4-8 Deck where the dealer stands on soft 17 and double after split is not allowed. We calculate other variants as deviations from this.

    Note: I do not have basic strategy 1-3 Deck since that is rare

    Note: that I have included rows that are redundant so that indexing is straight forward. For example, a hard hand with a total of 2 will always be Aces which you will always split, so you'd never double, but that option still exists in the table
    """

    hard_hits = [
        #A  2  3  4  5  6  7  8  9  T
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 2
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 3
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 4
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 5
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 6
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 7
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 8
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 9
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 10
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 11
        [1, 1, 1, 0, 0, 0, 1, 1, 1, 1], # 12
        [1, 0, 0, 0, 0, 0, 1, 1, 1, 1], # 13
        [1, 0, 0, 0, 0, 0, 1, 1, 1, 1], # 14
        [1, 0, 0, 0, 0, 0, 1, 1, 1, 1], # 15
        [1, 0, 0, 0, 0, 0, 1, 1, 1, 1], # 16
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 17
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 18
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 19
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 20
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 21
    ]

    hard_doubles = [
        #A  2  3  4  5  6  7  8  9  T
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 2
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 3
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 4
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 5
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 6
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 7
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 8
        [0, 0, 1, 1, 1, 1, 0, 0, 0, 0], # 9
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0], # 10
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 11
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 12
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 13
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 14
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 15
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 16
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 17
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 18
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 19
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 20
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 21
    ]

    hard_surrenders = [
        #A  2  3  4  5  6  7  8  9  T
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 2
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 3
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 4
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 5
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 6
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 7
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 8
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 9
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 10
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 11
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 12
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 13
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 14
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # 15
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 1], # 16
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 17
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 18
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 19
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 20
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 21
    ]

    soft_hits = [
        #A  2  3  4  5  6  7  8  9  T
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # AA
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # A2
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # A3
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # A4
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # A5
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # A6
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 1], # A7
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # A8
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # A9
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # AT
    ]

    soft_doubles = [
        #A  2  3  4  5  6  7  8  9  T
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # AA
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], # A2
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], # A3
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0], # A4
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0], # A5
        [0, 0, 1, 1, 1, 1, 0, 0, 0, 0], # A6
        [0, 1, 1, 1, 1, 1, 0, 0, 0, 0], # A7
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # A8
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # A9
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # AT
    ]

    soft_surrenders = [
        #A  2  3  4  5  6  7  8  9  T
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # AA
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # A2
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # A3
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # A4
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # A5
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # A6
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # A7
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # A8
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # A9
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # AT
    ]

    splits = [
        #A  2  3  4  5  6  7  8  9  T
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # AA
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], # 22
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], # 33
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 44
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # 55
        [0, 0, 1, 1, 1, 1, 0, 0, 0, 0], # 66
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0], # 77
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # 88
        [0, 1, 1, 1, 1, 1, 0, 1, 1, 0], # 99
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # TT
    ]

    rule_deviations = {
        "double_after_split": [
            {"type": "splits", "player": 2, "dealer": 2},
            {"type": "splits", "player": 2, "dealer": 3},
            {"type": "splits", "player": 3, "dealer": 2},
            {"type": "splits", "player": 3, "dealer": 3},
            {"type": "splits", "player": 4, "dealer": 5},
            {"type": "splits", "player": 4, "dealer": 6},
            {"type": "splits", "player": 6, "dealer": 2},
        ],
        "hit_on_soft_17": [
            {"type": "hard_doubles", "player": 11, "dealer": 1},
            {"type": "soft_doubles", "player": 9, "dealer": 6},
            {"type": "hard_surrenders", "player": 17, "dealer": 1},
            # {"type": "splits", "player": 9, "dealer": 1}, # I'm not sure where this came from
        ]
    }

    def __init__(self, name, chips=0, **table_rules):
        super(BasicStrategyPlayer, self).__init__(name=name, chips=chips, **table_rules)
        # we have to modify the basic strategy tables based on the `table_rules`
        self._apply_rule_deviations()

    def _apply_deviations(self, dev_list):
        for dev in dev_list:
            i = dev["player"]-1 if dev["type"] == "splits" else dev["player"]-2
            j = dev["dealer"]-1
            getattr(self, dev["type"])[i][j] = (not getattr(self, dev["type"])[i][j])

    def _apply_rule_deviations(self):
        for rule, dev_list in self.rule_deviations.items():
            if self.table_rules[rule]:
                self._apply_deviations(dev_list)

    def _get_hard_totals_table(self):
        hard_totals = []
        reset = '\033[0m'
        for p in range(2, 22):  # represents hand total
            row = []
            for d in range(1, 11):  # represents dealer upcard value
                if self.hard_surrenders[p-2][d-1]:
                    if self.hard_hits[p-2][d-1]:
                        row.append(("\033[47m", " R ", reset))
                    else:
                        row.append(("\033[45m", " Rs", reset))
                    continue
                if self.hard_doubles[p-2][d-1]:
                    if self.hard_hits[p-2][d-1]:
                        row.append(("\033[42m", " D ", reset))
                    else:
                        row.append(("\033[44m", " Ds", reset))
                    continue
                if self.hard_hits[p-2][d-1]:
                    row.append(("", " H ", reset))
                else:
                    row.append(("\033[43m", " S ", reset))
            hard_totals.append(row)
        return hard_totals

    def _get_soft_totals_table(self):
        soft_totals = []
        reset = '\033[0m'
        for p in range(2, 12):  # represents hand total
            row = []
            for d in range(1, 11):  # represents dealer upcard value
                if self.soft_surrenders[p-2][d-1]:
                    if self.soft_hits[p-2][d-1]:
                        row.append(("\033[47m", " R ", reset))
                    else:
                        row.append(("\033[45m", " Rs", reset))
                    continue
                if self.soft_doubles[p-2][d-1]:
                    if self.soft_hits[p-2][d-1]:
                        row.append(("\033[42m", " D ", reset))
                    else:
                        row.append(("\033[44m", " Ds", reset))
                    continue
                if self.soft_hits[p-2][d-1]:
                    row.append(("", " H ", reset))
                else:
                    row.append(("\033[43m", " S ", reset))
            soft_totals.append(row)
        return soft_totals

    def _get_splits_table(self):
        splits = []
        reset = '\033[0m'
        for p in range(1, 11):  # represents splitting card value
            row = []
            for d in range(1, 11):  # represents dealer upcard value
                if self.splits[p-1][d-1]:
                    row.append(("\033[46m", " P ", reset))
                else:
                    row.append(("", " N ", reset))
            splits.append(row)
        return splits

    @staticmethod
    def _rotate_columns(array_2d):
        return [row[1:] + [row[0]] for row in array_2d]

    @staticmethod
    def _rotate_rows(array_2d):
        return array_2d[1:] + [array_2d[0]]

    def _display_table(self, data_table, row_labels, rotate_columns=False, rotate_rows=False):
        dealer_upcards = ["", "2", "3", "4", "5", "6", "7", "8", "9", "T", "A"]
        pretty_table = PrettyTable()
        pretty_table.field_names = dealer_upcards

        # We might have to rotate columns because we let A = 1 for indexing
        # but usually A's are displayed after T
        if rotate_columns:
            data_table = self._rotate_columns(data_table)
        if rotate_rows:
            data_table = self._rotate_rows(data_table)
        
        for label, data_row in reversed(list(zip(row_labels, data_table))):
            pretty_table.add_row([str(label)] + ["".join(t) for t in data_row])
        
        return pretty_table

    # This is a lot of gross formatting, I wouldn't read this
    def display_strategy(self):
        print("Double After Split:", self.table_rules['double_after_split'])
        print("Dealer Hits on Soft 17:", self.table_rules['hit_on_soft_17'])
        print()
        print("Hard Totals")
        hard_totals_row_labels = [str(p) for p in range(2, 22)]
        hard_totals_table = self._display_table(self._get_hard_totals_table(), hard_totals_row_labels, rotate_columns=True, rotate_rows=False)
        print(hard_totals_table)
        print()
        print("Soft Totals")
        soft_totals_row_labels = [f"A,{c}" for c in range(2, 10)] + ["A,T"] + ["A,A"]
        soft_totals_table = self._display_table(self._get_soft_totals_table(), soft_totals_row_labels, rotate_columns=True, rotate_rows=True)
        print(soft_totals_table)
        print()
        print("Splits")
        splits_row_labels = [f"{c},{c}" for c in range(2, 10)] + ["T,T"] + ["A,A"]
        splits_table = self._display_table(self._get_splits_table(), splits_row_labels, rotate_columns=True, rotate_rows=True)
        print(splits_table)

    def bet(self):
        multiplier = 1
        return self.table_rules["min_bet"] * multiplier

    def action(self, hand, dealer_card, allowed_actions):
        d = dealer_card.value
        p = hand.get_total()

        splits = self.splits
        doubles = self.soft_doubles if hand.is_soft_hand() else self.hard_doubles
        hits = self.soft_hits if hand.is_soft_hand() else self.hard_hits
        surrenders = self.soft_surrenders if hand.is_soft_hand() else self.hard_surrenders

        if (Action.SURRENDER in allowed_actions) and surrenders[p-2][d-1]:
            return Action.SPLIT
        if (Action.SPLIT in allowed_actions) and splits[(p//2)-1][d-1]:
            return Action.SPLIT
        if (Action.DOUBLE in allowed_actions) and doubles[p-2][d-1]:
            return Action.DOUBLE
        if hits[p-2][d-1]:
            return Action.HIT
        return Action.STAND


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
        true_count = self._calculate_true_count()
        return f"{self.name.title()} (${self.chips})\tRC: {self.running_count}\tTC: {true_count}"

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



class Dealer(Player):

    def __init__(self, **table_rules):
        super(Dealer, self).__init__(name="Dealer", chips=0, **table_rules)
    
    def __repr__(self):
        return f"Dealer: "

    def action(self, hand, allowed_actions):
        total = hand.get_total()

        if hand.is_soft_hand():
            if total < 6:
                return Action.HIT
            elif total == 7:
                return Action.HIT if self.table_rules["hit_on_soft_17"] else Action.STAND
            else:
                return Action.STAND
        else:
            if total < 17:
                return Action.HIT
            else:
                return Action.STAND



if __name__ == "__main__":
    from hand import Hand

    hand = Hand(Card("AC"), Card("9C"))
    # Eric = HumanPlayer("Eric", 1000)
    # print(Eric)
    # b = Eric.bet()
    # print(b)
    # a = Eric.action(None, None, [Action.STAND, Action.HIT, Action.SPLIT])
    # print(a)

    # Steven = BasicStrategyPlayer("Steven", **{'double_after_split': True, 'hit_on_soft_17': False})
    Steven = CardCountingPlayer("Steven", **{'double_after_split': True, 'hit_on_soft_17': False})
    Steven.display_strategy(true_count=0)
    # print("\n\n")
    # Steven.display_strategy(true_count=0)

    # print()
    # actions = [Action.HIT, Action.STAND, Action.DOUBLE, Action.SURRENDER, Action.SPLIT]
    # action = Steven.action(Hand(0, Card("AD"), Card("AH")), Card(f"2D"), allowed_actions=actions)
    # print(action)

    # print(Steven.splits[1-1][2-1])
    # for row in Steven.splits:
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
    #         Steven.action(hand, Card(f"{dealer_pip}D"), allowed_actions=actions) for dealer_pip in ["2", "3", "4", "5", "6", "7", "8", "9", "J", "K", "A"]
    #     ])