import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

import json

def read_from_json_file(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        return data

def plot_chip_data(data, title='Earnings over Time'):

    # horizonal x-axis
    plt.axhline(0, color='black', linewidth=0.5)
    name_map = {'BS': "Basic Strategy", 'CC': "Card Counting"}

    for name, chip_history in data.items():

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
    # filename = "./data/BJ_fair_shoe_1000000.json"
    # filename = "./data/BJ_constantly_reshuffle_1000000.json"
    filename = "./data/BJ_evenly_distributed_high_cards_1000000 (3 hpb, 4 deck).json"
    data = read_from_json_file(filename)
    plot_chip_data(data, title='Earnings over Time (RSM, 25 groups)')