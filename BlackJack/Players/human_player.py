from .player import Player
from action import Action

class HumanPlayer(Player):

    """
    An interface so that a human player can play via the CLI
    """

    def bet(self):
        min_bet = self.table_rules['min_bet']
        max_bet = self.table_rules['max_bet']
        b = input("Bet: ")
        try:
            b = int(b)
        except:
            # raise TypeError(f"Expected an integer, instead got {b}")
            print(f"Expected an integer, instead got {b}. Try Again")
            return self.bet()
        if b <= 0:
            print("You are sitting out this hand")
            return 0
        if b < min_bet:
            print(f"Bet must be larger than {min_bet}, instead got {b}. Try Again")
            return self.bet()
        # if b > self.chips:
        #     print("You don't have that many chips, please try again.")
        #     return self.bet()
        if b > max_bet:
            print(f"Bet must be less than {max_bet}, instead got {b}. Try Again")
            return self.bet()
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

if __name__ == "__main__":
    from ..hand import Hand
    from ..card import Card

    Eric = HumanPlayer("Eric", 1000)
    print(Eric)
    b = Eric.bet()
    print(b)

    hand = Hand(Card("AH"), Card("AC"))
    dealer_card = Card("6D")
    a = Eric.action(hand, dealer_card, Action.all_actions())
    print(a)