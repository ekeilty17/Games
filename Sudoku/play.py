from board import SudokuBoard
from solver import SudokuLogicManager, SudokuSearchTree
from puzzles import *

board = Extreme_3

def human_player(game_board):

    B = SudokuBoard(game_board)
    print()
    print(B)
    while not B.is_complete():

        """Getting next move"""
        print
        # Getting row
        valid = False
        while not valid:
            r = input("row: ")
            try:
                if int(float(r)) != float(r) or int(r) < 1 or int(r) > 9:
                    print("invalid input")
                else:
                    valid = True
            except:
                print("invalid input")
        r = int(r)

        # Getting col
        valid = False
        while not valid:
            c = input("col: ")
            try:
                if int(float(c)) != float(c) or int(c) < 1 or int(c) > 9:
                    print("invalid input")
                else:
                    valid = True
            except:
                print("invalid input")
        c = int(c)

        # Getting num
        valid = False
        while not valid:
            num = input("number: ")
            try:
                if int(float(num)) != float(num) or int(num) < 1 or int(num) > 9:
                    print("invalid input")
                else:
                    valid = True
            except:
                print("invalid input")
        num = int(num)

        # Checking if it's a valid move
        if B.get_cell(r, c) == 0:
            temp = B.copy()
            temp.move(r, c, num)
            if temp.is_consistent():
                B.move(r, c, num)
                print()
                print(B)
            else:
                print("This move causes a repeated value in either a row, column, or square")
        else:
            print("That spot is already occupied")



def main(player):
    game_board = Extreme_3

    if player == "human":
        human_player(game_board)

    elif player == "AI logic only":
        B = SudokuBoard(game_board)
        L = SudokuLogicManager(B)
        print(L)

        changing = True
        while changing:
            changing = L.logical_step()
            print(L)
        
        print(L)

    elif player == "AI" or player == "AI bifercating":
        # instantiating all necessary classes
        B = SudokuBoard(game_board)
        L = SudokuLogicManager(B)
        T = SudokuSearchTree(L)
        print(T)

        # doing bifercated search
        leaf = T.search()
        if leaf == False:
            print("Could not find a solution :(")
            raise Exception("Could not find a solution :(")
        else:
            print(leaf.val)
            print("Solution Found!")

    else:
        raise ValueError(f"Expected either 'human' or 'player', got {player}")

if __name__ == "__main__":
    main("AI")