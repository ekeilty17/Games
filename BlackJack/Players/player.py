import math

from action import Action

class Player(object):

    """
    This is an abstract class mean to be implemented by various player strategies
    """

    def __init__(self, name, chips=0, insurance_frequency=0.5, even_money_frequency=0.5, **table_rules):
        self.name = name

        if type(chips) != int:
            raise TypeError(f"Expecting second argument to be an integer, got {chips} instead")
        
        self.chips = chips
        self.insurance_frequency = insurance_frequency
        self.even_money_frequency = even_money_frequency
        
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
        return f"{self.name} (${self.chips})"

    # function called any time a player is recieving chips (should not be altered)
    def recieve_chips(self, chips):
        self.chips += chips
        self.chip_history.append(self.chips)
    
    # function called any time a player bets chips (should not be altered)
    def bet_chips(self, chips):
        self.chips -= chips
        self.chip_history.append(self.chips)
    
    """ Functions to Implement """

    # function called for all new players when a new shoe starts
    def new_shoe(self):
        pass

    # function called any time a card is dealt
    def see_dealt_card(self, card):
        pass
    
    # function called if the player has the option for insurance
    def take_insurance(self, hand, dealer_upcard):
        return random.random() < self.insurance_frequency

    # function called if the player has the option for even money
    # This is essentially the same thing as insurance, except you have 21
    def take_even_money(self, hand, dealer_upcard):
        return random.random() < self.even_money_frequency
    
    # function called to obtain players bet before they get their cards
    # this function SHOULD NOT modify self.chips (this will be done by a different object). Just return the bet amount
    def bet(self):
        raise NotImplementedError("Not yet implemented...")

    # function called to obtain player action for their hand
    def action(self, hand, dealer_upcard, allowed_actions):
        raise NotImplementedError("Not yet implemented...")
    
    # I don't feel like implementing these right now
    # def take_insurance(self):
    #     pass
    
    # def take_even_money(self):
    #     pass

    # function called after a hand with its result
    def see_hand_result(self, result):
        pass