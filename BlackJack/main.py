from blackjack_table import BlackJackTable
from Players import HumanPlayer, BasicStrategyPlayer, CardCountingPlayer, NeverBustPlayer
from Shoes import FairShoe, LowRunningCountShoe, ConstantlyReshufflingShoe, EvenlyDistributedHighCardsShoe

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

from datetime import datetime
import json

def write_to_json_file(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def read_from_json_file(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        return data

def simulate(shoe, players, number_of_rounds, table_rules):

    Table = BlackJackTable(shoe=shoe, number_of_spots=8, verbose=False, **table_rules)

    for spot_index, P in enumerate(players, 1):
        Table.add_player( P, spot_index )
    
    Table.play(number_of_rounds=number_of_rounds)

    # organize the data
    data = {}
    for spot in Table._spots:
        player = spot['player']
        if player is None:
            continue
        data[player.name] = player.chip_history

    data['meta_data'] = {
        'table_rules': table_rules,
        'shoe': shoe.name,
        'number_of_rounds': number_of_rounds,
    }

    # plot the simulation
    plot_chip_data(data, title=f"Earnings over Time ({shoe.name})")

    # save the data if we want
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"BJ_{formatted_datetime}.json"

    save_success = False
    while not save_success:
        try:
            write_to_json_file(data, f"./data/{file_name}")
            print("Data saved.")
            save_success = True
        except:
            x = input("Save failed. Create a directory /data and try again. You can Control C to exit this loop, but nothing will be saved.")


def plot_chip_data(data, title='Earnings over Time'):

    # horizonal x-axis
    plt.axhline(0, color='black', linewidth=0.5)
    name_map = {'BS': "Basic Strategy", 'CC': "Card Counting", 'NB': "Never Bust"}

    for name, chip_history in data.items():
        if name == "meta_data":
            continue

        # Generate x values for the scatter plot
        x_values = np.arange(len(chip_history))

        # Create scatter plot
        #plt.scatter(x_values, chip_history, zorder=200)

        # Calculate the coefficients (slope and y-intercept) of the line of best fit
        coefficients = np.polyfit(x_values, chip_history, 1)
        slope = coefficients[0]
        intercept = coefficients[1]

        # Create the line of best fit equation
        line_of_best_fit = slope * x_values + intercept

        # Smooth the line using cubic spline interpolation
        spl = make_interp_spline(x_values, chip_history)
        x_smooth = np.linspace(0, len(chip_history)-1, 100)  # Generate 100 points for smoother line
        y_smooth = spl(x_smooth)
        plt.plot(x_smooth, y_smooth, label=name_map[name], zorder=100)

        # Plot the scatter plot and the line of best fit
        # plt.plot(x_values, line_of_best_fit, color='black', alpha=0.5, linestyle='--', zorder=50, label=round(slope, 2))

    # Add labels and legend
    plt.xlabel('Hands')
    plt.ylabel('Earnings')
    plt.title(title)
    plt.legend()

    # Show plot
    plt.grid(True, zorder=0)
    plt.show()

if __name__ == "__main__":
    table_rules = {
        "min_bet": 10,
        "max_bet": 1000,
        "hit_on_soft_17": False,
        "double_after_split": True,
        "late_surrender": True,
        "number_of_decks": 4,
        "blackjack_multiplier": 1.5,
    }
    shoe = FairShoe(ultilized_shoe_percent=0.75)
    NB = NeverBustPlayer(name="NB", chips=0, **table_rules)
    BS = BasicStrategyPlayer(name="BS", chips=0, **table_rules)
    CC = CardCountingPlayer(name="CC", chips=0, **table_rules)
    number_of_rounds = 1_000_000
    simulate(shoe=shoe, players=[NB, BS, CC], number_of_rounds=number_of_rounds, table_rules=table_rules)

    # filename = "./data/<filename here>.json"
    # data = read_from_json_file(filename)
    # plot_chip_data(data)