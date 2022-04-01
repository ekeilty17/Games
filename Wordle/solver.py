import random
import math
import argparse
from termcolor import colored
from collections import defaultdict

def get_pattern_from_user(guesses, i):
    # Obtaining feedback from user/program
    feedback = ""
    good_feedback = False
    j = 0
    while not good_feedback:
        
        guess = guesses[j]
        print(f"Guess #{i+1}:", guess)
        feedback = input("feedback: ")
        feedback = feedback.upper()

        # This means this word is not in the game's vocab, so we need a new guess
        if feedback == 'FORCE':
            guess = input(f"Guess #{i+1}: ")
            feedback = input("feedback: ")
            feedback = feedback.upper()
        
        if feedback == "SKIP":
            j += 1
            good_feedback = False
        elif feedback == "EXIT":
            print("Game terminated")
            return '?' * word_length
        # This means the feedback had a bad form and couldn't be parsed
        elif set(feedback).difference(set(['G', 'Y', 'B'])) != set():
            print("Unable to parse feedback due to unrecognized characters")
            print("Please use the following convention:")
            print("\t- 'FORCE' means you want to provide the guess")
            print("\t- 'SKIP' means this word is not in the vocabulary of the game, so we need to select a new word")
            print("\t- 'EXIT' means you want to exit the game")
            print("\t- 'G' = 'g' = 'green'  meaning the letter is in the word and in the correct spot")
            print("\t- 'Y' = 'y' = 'yellow' meaning the letter is in the word, but not in the correct spot")
            print("\t- 'B' = 'b' = 'black'  meaning the letter is not in the word")
            print()
        elif len(feedback) != 5:
            print(f"unable to parse feedback. Expecting a length of 5 and recieved length of {len(feedback)}")
            print()
        else:
            good_feedback = True
    
    return guesses[j], feedback.lower()

def get_pattern_from_answer(guess, secret_word):
    if len(guess) != len(secret_word):
        raise ValueError(f"The lengths of the two words should be equal: {len(guess)} != {len(secret_word)}")
    N = len(guess)

    # initialize as everything being wrong
    secret_word = list(secret_word)
    pattern = ["b"] * N

    # catch all letters that are exactly correct (green)
    for i in range(N):
        if guess[i] == secret_word[i]:
            pattern[i] = "g"
            secret_word[i] = "_"  # we remove those letters for when we do our yellow pass

    # final pass catches all left-over letters
    for i in range(N):
        # If the letter was already marked as green, then we skip
        # otherwise, we check if that letter exists in the secret word
        # recall, if a letter was marked green, then we replaced it with '_', so when we do 
        #       `guess[i] in secret_word`
        # it won't repeate anything that was already marked green
        if (pattern[i] != "g") and (guess[i] in secret_word):
            pattern[i] = "y"
            secret_word[ secret_word.index(guess[i]) ] = "_"

    return "".join(pattern)

def get_display_pattern(guess, pattern):
    display_pattern = ""
    for g, p in zip(guess, pattern):
        if p == "g":
            display_pattern += colored(g, "green")
        if p == "y":
            display_pattern += colored(g, "yellow")
        if p == "b":
            display_pattern += colored(g, "red")
    return display_pattern

def filter_candidates(candidates, guess, pattern):
    candidates = list(candidates)
    letter_count = {letter: 0 for letter in set(guess)}
    black_letter = {letter: False for letter in set(guess)}

    # filtering words that don't have green letters in that exact location
    for i, (g, p) in enumerate(zip(guess, pattern)):
        if p == "g":
            candidates = list(filter(lambda word: word[i] == g, candidates))
            letter_count[g] += 1
        if p == "y":
            # it's important to note that yellow also tells us that the letter does not go in that location
            candidates = list(filter(lambda word: word[i] != g, candidates))
            letter_count[g] += 1
        if p == "b":
            black_letter[g] = True
    
    # filtering out words that don't have the correct number of yellow or green letters
    for letter, count in letter_count.items():
        if black_letter[letter]:
            candidates = list(filter(lambda word: list(word).count(letter) == count, candidates))
        else:
            candidates = list(filter(lambda word: list(word).count(letter) >= count, candidates))

    return candidates

def analyze_candidates(full_dictionary, word_of_the_day_dictionary, guesses, secret_word, tolerance=50):
    candidates1 = list(full_dictionary)
    candidates2 = list(word_of_the_day_dictionary)

    for guess in guesses:
        pattern = get_pattern_from_answer(guess, secret_word)
        candidates1 = filter_candidates(candidates1, guess, pattern)
        candidates2 = filter_candidates(candidates2, guess, pattern)

        print(get_display_pattern(guess, pattern))

        if len(candidates1) > tolerance:
            print("[...many candidates...]")
        else:
            print(candidates1)

        if len(candidates2) > tolerance:
            print("[...many candidates...]")
        else:
            print(candidates2)
        print()

def normalize_distribution(distribution):
    S = sum(distribution.values())
    return {key: value/S for key, value in distribution.items()}

def get_entropy(distribution):
    return -sum([p * math.log(p, 2) for p in distribution.values() if p > 0])

def solve(dictionary, start_word=None, secret_word=None, word_length=5, tries=6, hardmode=False):
    candidates = list(dictionary)
    guesses = []
    
    if start_word is None:
        start_word = "crane"
    
    for i in range(tries):
        
        if i == 0:
            guesses = [start_word]
        elif len(candidates) == 1:
            guesses = [candidates[0]]
        else:
            entropy_dict = {}
            for guess in dictionary:
                pattern_distribution = defaultdict(lambda: 0)
                for possible_answer in candidates:
                    pattern = get_pattern_from_answer(guess, possible_answer)
                    #new_candidates = filter_candidates(candidates, guess, pattern)

                    pattern_distribution[pattern] += 1
                
                pattern_distribution = normalize_distribution(pattern_distribution)
                entropy_dict[guess] = get_entropy(pattern_distribution)

            # There's probably a better way to do this, but I want to break ties by choosing words in the candidates dictionary first
            #guesses = [guess for guess, _ in reversed(sorted(entropy_dict.items(), key=lambda t: t[1]))]
            inverse_index = defaultdict(list)
            for word, entropy in entropy_dict.items():
                inverse_index[entropy].append(word)
            for entropy in inverse_index.keys():
                inverse_index[entropy] = list(reversed(sorted(inverse_index[entropy], key=lambda word: int(word in candidates))))

            guesses = []
            for _, words in reversed(sorted(inverse_index.items(), key=lambda t: t[0])):
                guesses.extend(words)
        
        # getting pattern from guess
        guess, pattern = "", ""
        if secret_word is None:
            guess, pattern = get_pattern_from_user(guesses, i)
        else:
            guess = guesses[0]
            pattern = get_pattern_from_answer(guess, secret_word)
        
        # updating candidates list
        candidates = filter_candidates(candidates, guess, pattern)
        if hardmode:
            dictionary = list(candidates)

        # displaying guess
        print(f"Guess #{i+1}: {get_display_pattern(guess, pattern)}")
        print()

        # breaking if the answer is correct
        if pattern == "g" * word_length:
            return True

        # only print if you are curious
        print(candidates)
    
    print("The secret word was:", secret_word)
    return False

def get_args():
    # Commandline Arguments
    parser = argparse.ArgumentParser(description='Terminal Arguments for solving Wordle')
    
    #parser.add_argument('start_word', type=str, help='the first word')
    #parser.add_argument('secret_word', type=str, help='the secret word we are trying to find')
    parser.add_argument('words', type=str, nargs='+', help='sequence of guesses to be analyzed, the first word is assumed to be the starting word and the last word is assumed to be the secret word')
    parser.add_argument('--analyze', action='store_true', default=False, help='if included, the sequence of words will be assumed to be a complete game and be analyzed')
    parser.add_argument('--hardmode', action='store_true', default=False, help='if included, hardmode will be on')

    args = parser.parse_args()
    return args

def main(full_dictionary, word_of_the_day_dictionary, args):
    if len(args.words) < 2:
        raise ValueError("The number of words needs to be greater than 2, only received", len(args.words))
    
    start_word = args.words[0]
    secret_word = args.words[-1] 
    if args.analyze:
        analyze_candidates(full_dictionary, word_of_the_day_dictionary, args.words, secret_word)
    else:
        solve(full_dictionary, start_word, secret_word, hardmode=args.hardmode)


if __name__ == "__main__":
    with open('wordle_word_of_the_day_dictionary.txt', 'r') as f:
        lines = f.readlines()
    word_of_the_day_dictionary = [word.strip() for word in lines]

    with open('wordle_full_dictionary.txt', 'r') as f:
        lines = f.readlines()
    full_dictionary = [word.strip() for word in lines]
    
    args = get_args()
    main(full_dictionary, word_of_the_day_dictionary, args)
