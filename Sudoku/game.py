from board import *

def Sudoku(game_board):

    B = board(game_board)
    print
    B.Display()
    while not B.isComplete():

        """Getting next move"""
        print
        # Getting row
        valid = False
        while not valid:
            row = raw_input("row: ")
            try:
                if int(float(row)) != float(row) or int(row) < 1 or int(row) > 9:
                    print "invalid input"
                else:
                    valid = True
            except:
                print "invalid input"
        row = int(row)-1

        # Getting col
        valid = False
        while not valid:
            col = raw_input("col: ")
            try:
                if int(float(col)) != float(col) or int(col) < 1 or int(col) > 9:
                    print "invalid input"
                else:
                    valid = True
            except:
                print "invalid input"
        col = int(col)-1

        # Getting num
        valid = False
        while not valid:
            num = raw_input("number: ")
            try:
                if int(float(num)) != float(num) or int(num) < 1 or int(num) > 9:
                    print "invalid input"
                else:
                    valid = True
            except:
                print "invalid input"
        num = int(num)

        # Checking if it's a valid move
        if B.store[row][col] == 0:
            temp = B.copy()
            temp[row][col] = num
            if isValidSudokuBoard(temp):
                B.move(num,[row,col])
                print
                B.Display()
            else:
                print "Invalid move"
        else:
            print "That spot is already occupied"
