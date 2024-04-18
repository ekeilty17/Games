from blackjack_table import BlackJackTable
from player import Player, HumanPlayer, BasicStrategyPlayer, CardCountingPlayer
from shoe import FairShoe, LowRunningCountShoe, ConstantlyReshufflingShoe, EvenlyDistributedHighCards

import json
from datetime import datetime

from analyze import plot_chip_data

def write_to_json_file(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    table_rules = {
        "min_bet": 10,
        "max_bet": 1000,
        "hit_on_soft_17": False,
        "double_after_split": True,
        "late_surrender": True,
        "number_of_decks": 8,
        "blackjack_multiplier": 1.5,
    }

    Table = BlackJackTable(shoe=EvenlyDistributedHighCards(high_cards_per_bucket=4), number_of_spots=8, verbose=False, **table_rules)

    BS = BasicStrategyPlayer(name="BS", chips=0, **table_rules)
    CC = CardCountingPlayer(name="CC", chips=0, **table_rules)
    Table.add_player( BS, 1 )
    Table.add_player( CC, 2 )
    
    Table.play(number_of_rounds=1_000_000)

    # save result
    data = {}
    for spot in Table._spots:
        player = spot['player']
        if player is None:
            continue
        data[player.name] = player.chip_history

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"BJ_{formatted_datetime}.json"
    write_to_json_file(data, f"./data/{file_name}")

    plot_chip_data(data)

if __name__ == "__main__":
    main()