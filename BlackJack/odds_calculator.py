from blackjack_table import BlackJackTable
from card import Card
from hand import DealerHand
from Shoes import StackedShoe
from Players import BasicStrategyPlayer

def odds_calculator(player_card_1, player_card_2, dealer_upcard, table_rules, number_of_simulations=1000):

    chips = 0
    for i in range(number_of_simulations):
        print("Simulation Number:", i+1)
        stacked_cards = ["??", player_card_1, dealer_upcard, player_card_2]
        shoe = StackedShoe(stacked_cards=stacked_cards)
        
        Table = BlackJackTable(shoe=shoe, number_of_spots=8, **table_rules)
        BS = BasicStrategyPlayer(name="BS", chips=0, **table_rules)
        Table.add_player( BS )

        Table.play(number_of_rounds=1, count_rounds=False)
        chips += BS.chips
    
    EV = chips / 10 / number_of_simulations
    return EV

if __name__ == "__main__":

    table_rules = {
        "min_bet": 10,
        "max_bet": 1000,
        "number_of_decks": 6,
        "blackjack_multiplier": 1.5,
        "hit_on_soft_17": False,
        "dealer_peaks_for_blackjack": True,
        "insurance_and_even_money": True,
        "early_surrender": False,
        "late_surrender": True,
        "double_after_split": True,
        "split_max": 4,
        "surrender_against_ace": True,
        "split_max_aces": 2,
        "hit_after_split_aces": False,
        "double_after_split_aces": False,
    }

    player_card_1, player_card_2 = "2?", "8?"
    dealer_upcard = "6?"
    number_of_simulations = 1_000
    EV = odds_calculator(player_card_1, player_card_2, dealer_upcard, table_rules, number_of_simulations)
    print(EV)