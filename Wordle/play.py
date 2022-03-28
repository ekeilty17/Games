import random
import string
from termcolor import colored

def get_pattern(guess, secret_word):
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

def play_wordle(word_of_the_day_dictionary, full_dictionary, hardmode=False, tries=6):

    secret_word = random.choice(word_of_the_day_dictionary)
    word_length = len(secret_word)

    letters_used = set()
    position_info = ["?"] * word_length
    letter_info = {letter : 0 for letter in string.ascii_lowercase}

    print()
    if hardmode:
        print("Note that you are playing in hardmode, which means you must use the information that you are given")
        print()

    for i in range(tries):

        # displaying information about letters
        letter_str = ""
        for letter in string.ascii_lowercase:
            if letter in position_info:
                letter_str += colored(letter, "green", attrs=['bold'])
            elif letter_info[letter] > 0:
                letter_str += colored(letter, "yellow", attrs=['bold'])
            elif letter in letters_used:
                letter_str += colored(letter, "red", attrs=['bold'])
            else:
                letter_str += colored(letter, "white", attrs=['bold'])

        # get user's guess
        valid_input = False
        guess = ""
        while not valid_input:
            print(letter_str)
            guess = input(f"Guess #{i+1}: ").strip().lower()

            # check if the input is valid
            if len(guess) != word_length:
                print(f"The word must be of length {word_length}, please try again.")
                print()
            elif guess not in full_dictionary:
                print("This is not a valid word, please try again.")
                print()
            else:
                if hardmode:
                    for j in range(word_length):
                        if position_info[j] != "?":
                            if position_info[j] != guess[j]:
                                print(f"Must use '{position_info[j]}' at letter {j+1}")
                                print()
                                break
                    else:
                        guess_list = list(guess)
                        for letter, count in letter_info.items():
                            if count > 0:
                                if count > guess_list.count(letter):
                                    print(f"Must use '{letter}' in your guess")
                                    print()
                                    break
                        else:
                            valid_input = True
                else:
                    valid_input = True
        
        # getting pattern of guess
        pattern = get_pattern(guess, secret_word)
        print("Feedback:", get_display_pattern(guess, pattern))
        print()
        
        # checking if the user won
        if pattern == "g"*word_length:
            print("You win!")
            return True
        
        # updating given info for hardmode
        letters_used = letters_used.union(list(guess))
        letter_info = {letter : 0 for letter in string.ascii_lowercase}
        for i, p in enumerate(pattern):
            if p == "g":
                position_info[i] = guess[i]
                letter_info[guess[i]] += 1
            if p == "y":
                letter_info[guess[i]] += 1
    
    print(f"The word was {secret_word}, Better luck next time :(")
    return False


if __name__ == "__main__":
    with open('wordle_word_of_the_day_dictionary.txt', 'r') as f:
        lines = f.readlines()
    word_of_the_day_dictionary = [word.strip() for word in lines]

    with open('wordle_full_dictionary.txt', 'r') as f:
        lines = f.readlines()
    full_dictionary = [word.strip() for word in lines]

    play_wordle(word_of_the_day_dictionary, full_dictionary, hardmode=True)