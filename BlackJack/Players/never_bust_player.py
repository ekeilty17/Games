from .basic_strategy_player import BasicStrategyPlayer
from action import Action

class NeverBustPlayer(BasicStrategyPlayer):

    """
    The idea of this strategy is to never bust, which was a popular strategy in the early days of BlackJack. Unfortunately, it has been shown to be extremely unprofitable.

    Essentially, the only difference between this player and a basic strategy player is that they STAND on hands such as a 16 vs a dealer 10. While STAND and HIT both lose over the long run, HIT loses less often. But this player chooses to STAND, taking the lower EV play.

    I've played around with this in simulations, you wouldn't believe how losing this is over the long run. You lose about 8x faster, and over many, many hands that compounds very quickly
    """

    # A player like this is probably scared, so they might take insurance
    def take_insurance(self, hand, dealer_upcard):
        return True
    def take_even_money(self, hand, dealer_upcard):
        return True

    # bet() is implemented in BasicStrategyPlayer

    def action(self, hand, dealer_upcard, allowed_actions):
        basic_strategy_action = super(NeverBustPlayer, self).action(hand, dealer_upcard, allowed_actions)

        # I'll give this player the best odds they can have by telling them when they should at least be splitting and doubling since this never risks busting
        # I can't decide if this type of player would surrender...I suspect not
        if basic_strategy_action in [Action.SPLIT, Action.DOUBLE]:
            return basic_strategy_action

        # we can't bust on soft hands, so we will do whatever basic strategy says to do in order to give this player their best chances
        if hand.is_soft_hand():
            return basic_strategy_action

        # If we don't have a split, double, or soft hand then this strategy says we should never risk busting
        # therefore, any hand over 11 is a stay, regardless of what the dealer has
        total = hand.get_total()
        return Action.STAND if total > 11 else Action.HIT