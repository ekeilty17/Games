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
            print(f"Expected an integer, instead got '{b}'. Try Again")
            return self.bet()
        if b <= 0:
            print("You are sitting out this hand")
            return 0
        if b < min_bet:
            print(f"Bet must be larger than {min_bet}, instead got {b}. Try Again")
            return self.bet()
        # if b > self.chips:
        #     print("You don't have that many chips to make this bet. Try Again or bet 0 to skip this round.")
        #     return self.bet()
        if b > max_bet:
            print(f"Bet must be less than {max_bet}, instead got {b}. Try Again")
            return self.bet()
        return b
    
    def action(self, hand, dealer_upcard, allowed_actions):
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
            print(f"Expected an integer, instead got '{a}'. Try Again")
            return self.action(hand, dealer_upcard, allowed_actions)
        allowed_action_indices = [i+1 for i, action in enumerate(Action.all_actions()) if action in allowed_actions]
        if a not in allowed_action_indices:
            print(f"Expected one of {allowed_action_indices}, instead got {a}. Try Again")
            return self.action(hand, dealer_upcard, allowed_actions)
        return Action.all_actions()[a-1]

    def take_insurance(self, hand, dealer_upcard):
        response = input("Do you want to take insurance (y/n): ")
        if response in ['y', 'Y']:
            return True
        elif response in ['n', 'N']:
            return False
        else:
            print(f"Expected one of 'y' or 'n'. Instead got '{response}'. Try Again")
            return self.take_insurance()

    def take_even_money(self, hand, dealer_upcard):
        response = input("Do you want to take even money (y/n): ")
        if response in ['y', 'Y']:
            return True
        elif response in ['n', 'N']:
            return False
        else:
            print(f"Expected one of 'y' or 'n'. Instead got '{response}'. Try Again")
            return self.take_even_money()

if __name__ == "__main__":
    from hand import Hand
    from card import Card

    Eric = HumanPlayer("Eric", 1000)
    print(Eric)
    b = Eric.bet()
    print(b)

    hand = Hand(Card("AH"), Card("AC"))
    dealer_upcard = Card("6D")
    a = Eric.action(hand, dealer_upcard, Action.all_actions())
    print(a)

    print(Eric.take_insurance())
    print(Eric.take_even_money())