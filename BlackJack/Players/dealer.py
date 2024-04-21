from .player import Player
from action import Action

class Dealer(Player):

    """
    My code treats the dealer the same as a player, they just never bet chips
    """

    def __init__(self, **table_rules):
        super(Dealer, self).__init__(name="Dealer", chips=0, **table_rules)
    
    def __repr__(self):
        return f"Dealer: "

    def bet(self):
        return 0

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