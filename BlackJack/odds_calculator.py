from blackjack_table import BlackJackTable
from card import Card
from hand import DealerHand
from Shoes import StackedShoe
from Players import BasicStrategyPlayer

from prettytable import PrettyTable
from datetime import datetime
import json

def write_to_json_file(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def read_from_json_file(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        return data

def odds_calculator(player_card_1, player_card_2, dealer_upcard, table_rules, number_of_simulations=1000, count_rounds=True):

    stacked_cards = ["??", player_card_1, dealer_upcard, player_card_2]
    shoe = StackedShoe(stacked_cards=stacked_cards, ultilized_shoe_percent=0)   # reshuffle every hand
    
    Table = BlackJackTable(shoe=shoe, number_of_spots=8, **table_rules)
    BS = BasicStrategyPlayer(name="BS", chips=0, **table_rules)
    Table.add_player( BS )

    Table.play(number_of_rounds=number_of_simulations, count_rounds=count_rounds)
    
    EV = BS.chips / 10 / number_of_simulations
    return EV

def hard_hands_EV(table_rules, number_of_simulations=1000):

    EV_table = [[] for _ in range(21-4)]

    for total in range(4, 21):
        if total < 12:
            player_card_1 = "2?"
            player_card_2 = f"{total - 2}?"
        elif total == 20:
            player_card_1 = "T?"
            player_card_2 = f"T?"
        else:
            player_card_1 = "T?"
            player_card_2 = f"{total - 10}?"

        for d in range(1, 11):
            if d == 1:
                dealer_upcard = "A?"
            elif d == 10:
                dealer_upcard = "T?"
            else:
                dealer_upcard = f"{d}?"
        
            EV = odds_calculator(player_card_1, player_card_2, dealer_upcard, table_rules, number_of_simulations, count_rounds=False)
            print(f"{player_card_1[0]} {player_card_2[0]} vs {dealer_upcard[0]}: {EV}")
            EV_table[total-4].append(EV)

    hard_hands_row_labels = [str(total) for total in range(4, 22)]
    display_table = display_EV_table(EV_table, hard_hands_row_labels)
    print(display_table)

    # Saving data
    obj = {
        "table_rules": table_rules,
        "number_of_simulations": number_of_simulations,
        "hard_hands_EV_table": EV_table,
    }

    # save the data if we want
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"BJ_EV_{formatted_datetime}.json"

    save_success = False
    while not save_success:
        try:
            write_to_json_file(obj, f"./data/{file_name}")
            print("Data saved.")
            save_success = True
        except:
            x = input("Save failed. Create a directory /data and try again. You can Control C to exit this loop, but nothing will be saved.")


def rotate_columns(array_2d):
    return [row[1:] + [row[0]] for row in array_2d]

def rotate_rows(array_2d):
    return array_2d[1:] + [array_2d[0]]

def EV_color_map(EV):
    if EV < -0.5:
        color = '\033[41m'
    elif EV < 0:
        color = '\033[43m'
    elif EV == 0:
        color = '\033[47m'
    elif EV < 0.5:
        color = '\033[42m'
    else:
        color = '\033[44m'
    return color

def display_EV_table(EV_table, row_labels):

    # put A last instead of first
    EV_table = rotate_columns(EV_table)

    dealer_upcards = ["", "2", "3", "4", "5", "6", "7", "8", "9", "T", "A"]
    pretty_table = PrettyTable()
    pretty_table.field_names = dealer_upcards

    
    for label, row in reversed(list(zip(row_labels, EV_table))):
        pretty_table.add_row([str(label)] + [EV_color_map(EV) + (f" {round(EV, 3):<5}" if EV >= 0 else f"{round(EV, 3):<6}")  + '\033[0m' for EV in row])
    
    return pretty_table


if __name__ == "__main__":

    table_rules = {
        "min_bet": 10,
        "max_bet": 1000,
        "number_of_decks": 1,           # Making this small really speeds up the simulation, but it also can change the EV
        "blackjack_multiplier": 1.5,
        "hit_on_soft_17": False,
        "dealer_peaks_for_blackjack": True,
        "insurance_and_even_money": True,
        "early_surrender": False,
        "late_surrender": False,
        "double_after_split": True,
        "split_max": 4,
        "surrender_against_ace": True,
        "split_max_aces": 2,
        "hit_after_split_aces": False,
        "double_after_split_aces": False,
    }
    number_of_simulations = 10_000

    # player_card_1 = "2?"
    # player_card_2 = "8?"
    # dealer_upcard = "6?"
    # EV = odds_calculator(player_card_1, player_card_2, dealer_upcard, table_rules, number_of_simulations)
    # print(EV)

    # hard_hands_EV(table_rules, number_of_simulations=10_000)
    obj = read_from_json_file("./data/BJ_EV_2024-04-23_09-31-05.json")
    hard_hands_EV_table = obj["hard_hands_EV_table"]
    hard_hands_row_labels = [str(total) for total in range(4, 22)]
    display_table = display_EV_table(hard_hands_EV_table, hard_hands_row_labels)
    print(display_table)
    