from tour import *
from blank_board import *
from time import sleep
import os

def PNGtoCoord(png, rows, cols):
    x = -1
    y = -1
    alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
             'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    if png[0] not in alpha[:cols]: 
        print "invalid row input, try again"
        return False
    try:
        y = int(png[1]) - 1
        if y < 0 or y >= rows:
            print "file is out of range, try again"
            return False
    except:
        print "file was not an integer, try again"
        return False
    x = alpha.index(png[0])
    return [y,x]


def getInitialBoard():

    #Getting board size
    rows = -1
    cols = -1

    possible_tour = False
    while not possible_tour:
        print
        valid = False
        while not valid:
            rows = raw_input("Number of rows: ")
            try:    
                if int(float(rows)) != float(rows) or int(rows) < 1:
                    print "invalid input"
                elif int(rows) > 26:
                    print "Bro...that's too big"
                else:
                    valid = True
            except:
                print "invalid input" 
        rows = int(rows)

        valid = False
        while not valid:
            cols = raw_input("Number of cols: ")
            try:
                if int(float(cols)) != float(cols) or int(cols) < 1:
                    print "invalid input"
                elif int(cols) > 26:
                    print "Bro...that's too big"
                else:
                    valid = True
            except:
                print "invalid input"  
        cols = int(cols)
    
        possible_tour = True
        """
        possible_tour = True
        if rows%2 == 1 and cols%2 == 1:
            possible_tour = False
        elif min(rows,cols) in [1,2,4]:
            possible_tour = False
        elif min(rows,cols) == 3 and max(rows,cols) in [4,6,8]:
            possible_tour = False

        if not possible_tour:
            print "A complete Knight's Tour is impossible with these dimensions."
        """

    #Displaying a blank board so user can pick a starting square
    B_blank = blank_board(rows, cols)
    B_blank.Display()
    
    #Getting starting square
    valid = False
    start = []
    while not valid:
        png = raw_input("Starting Square: ")
        if PNGtoCoord(png, rows, cols) != False:
            start = PNGtoCoord(png, rows, cols)
            #PNGtoCoord hands printing the error messages
            valid = True

    return board(rows, cols, start)

#L is a list of board classes
def Display_Tour(L):

    if L == []:
        return False

    os.system('clear')
    print "Ready?"
    sleep(0.8)
    os.system('clear')
    print 3
    sleep(0.8)
    os.system('clear')
    print 2
    sleep(0.8)
    os.system('clear')
    print 1
    sleep(1)

    for B in L:
        os.system('clear')
        B.Display()
        sleep(0.5)
    print
    return True


#Actually playing the game
def Human():
    B = getInitialBoard()
    print
    B.Display()
    print
    
    L = []
    while (not B.isComplete()) and (B.Num_Knight_Moves(B.curr) != 0):
        #Getting next square
        valid = False
        nxt = []
        while not valid:
            png = raw_input("Next Square: ")
            if PNGtoCoord(png, B.rows, B.cols) != False:
                nxt = PNGtoCoord(png, B.rows, B.cols)
                #PNGtoCoord hands printing the error messages
                valid = True
            #checking if it's a valid move
            if nxt not in B.Possible_Knight_Moves():
                valid = False
                print "Not a valid Knight move"

        #making move
        B.Move(nxt)
        B.Display()
        print
        
        #adding board to L
        L += [B.new()]

    print
    if B.isComplete():
        print "Congradulations! You Win!"
        x = raw_input("Hit enter to see full tour!")
        Display_Tour(L)
        return True
    else:
        print "No more moves. Better luck next time :("
        return False

def BruteForce(rows=-1, cols=-1, start=-1):
    #This is just a convient way to do things
    B = None
    if rows == -1 or cols == -1 or start == -1:
        B = getInitialBoard()
    else:
        B = board(rows, cols, start)
    
    Display_Tour(Knights_Tour(B))

def BruteForce_Closed(rows=-1, cols=-1, start=-1):
    #This is just a convient way to do things
    B = None
    if rows == -1 or cols == -1 or start == -1:
        B = getInitialBoard()
    else:
        B = board(rows, cols, start)

    Display_Tour(Closed_Knights_Tour(B))
