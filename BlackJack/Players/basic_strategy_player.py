from .player import Player
from action import Action

from prettytable import PrettyTable

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

    def __init__(self, name, chips=0, base_bet=None, **table_rules):
        super(BasicStrategyPlayer, self).__init__(name=name, chips=chips, **table_rules)
        # we have to modify the basic strategy tables based on the `table_rules`
        self._apply_rule_deviations()

        self.base_bet = self.table_rules['min_bet'] if base_bet is None else base_bet
            

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
        return self.base_bet

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


if __name__ == "__main__":
    from hand import Hand
    from card import Card

    hand = Hand(Card("AC"), Card("9C"))

    BS = BasicStrategyPlayer("BS", **{'double_after_split': True, 'hit_on_soft_17': False})
    BS.display_strategy()

    # print()
    # actions = [Action.HIT, Action.STAND, Action.DOUBLE, Action.SURRENDER, Action.SPLIT]
    # action = BS.action(Hand(0, Card("AD"), Card("AH")), Card(f"2D"), allowed_actions=actions)
    # print(action)

    # print(BS.splits[1-1][2-1])
    # for row in BS.splits:
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
    #         BS.action(hand, Card(f"{dealer_pip}D"), allowed_actions=actions) for dealer_pip in ["2", "3", "4", "5", "6", "7", "8", "9", "J", "K", "A"]
    #     ])