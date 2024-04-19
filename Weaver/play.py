from solver import solver_bidirectional, valid_next_word
import argparse
import random

def get_args():
    # Commandline Arguments
    parser = argparse.ArgumentParser(description='Terminal Arguments for solving Weaver')

    parser.add_argument('-word_length', nargs='?', type=int, help='length of words')

    args = parser.parse_args()
    return args

def main(dictionary):

    # Game instructions
    print("You must go from the start word to the end word only changing one letter at a time.")
    print("For example: east --> vast --> vest --> west")
    print("Obviously, there is a set of optimal, so as well as finding any solution, an additional challenge is to find an optimal solution.")
    print("For example: east --> wast --> west is optimal")
    print()

    start_word, end_word = random.sample(dictionary, 2)
    print(f"Goal: {start_word} --> ... --> {end_word}")

    optimal_length, solutions = solver_bidirectional(dictionary, start_word, end_word, verbose=False)

    while True:

        user_solution = [start_word]
        while True:
            print()
            print("--> ".join(user_solution), end="--> ")
            next_word = input("")
            
            if next_word in ["!exit", "!quit"]:
                break
            
            if next_word in ["!solution"]:
                print()
                print(f"All Optimal Solutions ({len(solutionsls)} total):")
                solution_strings = [" --> ".join(solution) for solution in solutions]
                for solution_string in sorted(solution_strings):
                    print('\t', solution_string)
                break

            if next_word in ["!reset", "!start over", "!play again"]:
                user_solution = [start_word]
                continue

            if next_word in ["!back", "!undo"]:
                user_solution = user_solution[:-1]
                continue
            
            if not valid_next_word(user_solution[-1], next_word):
                print(f"Cannot change more than 1 character")
                continue

            if next_word not in dictionary:
                print(f"'{next_word}' is not in the wordlist")
                continue
            
            user_solution.append(next_word)

            if next_word == end_word:
                print()
                print("Your solution:", "--> ".join(user_solution))
                print("Your solution length:", len(user_solution)-1)
                print("Optimal Solution Length:", optimal_length)
                break
        
        if next_word in ["!solution", "!quit", "!exit"]:
            break

        print()
        play_again = input("play again? 'y' or 'n'\n")
        print()
        if play_again == 'n':
            break
        else:
            print(f"Goal: {start_word} --> ... --> {end_word}")
        
    
    # To see the solution, you can use the solver

if __name__ == "__main__":
    args = get_args()
    
    n = 4 if args.word_length is None else args.word_length
    word_file = ""
    if n == 4:
        word_file = "words4.txt"
    elif n == 5:
        word_file = "words5.txt"
    else:
        raise ValueError(f"Words of length {n} is not supported")
    
    with open(word_file, 'r') as f:
        lines = f.readlines()
    dictionary = [word.strip() for word in lines]
    
    main(dictionary)