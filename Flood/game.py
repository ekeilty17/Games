from board import *

def flood():

    """Getting set up info"""
    rows = 0
    cols = 0
    colors = 0
    cnt = 0

    #number of rows
    valid = False
    while not valid:
        print
        rows = raw_input("number of rows: ")
        try: 
            if int(float(rows)) != float(rows) or int(rows) < 1:
                print "invalid input"
            else:
                valid = True
        except:
            print "invalid input"

    #number of columns
    valid = False
    while not valid:
        print
        cols = raw_input("number of columns: ")
        try:
            if int(float(cols)) != float(cols) or int(cols) < 1:
                print "invalid input"
            else:
                valid = True
        except:
            print "invalid input"

    #number of colors
    valid = False
    while not valid:
        print
        colors = raw_input("number of colors: ")
        try:
            if int(float(colors)) != float(colors) or int(colors) < 1:
                print "invalid input"
            else:
                valid = True
        except:
            print "invalid input"

    B = board(int(rows), int(cols), int(colors))
    print
    print
    B.Display()
    print str(cnt) + '/' + str(B.expected)
    while not B.isComplete():
        
        #Getting next move
        next_color = -1
        valid = False
        while not valid:
            next_color = raw_input("color: ")
            try:
                if int(float(next_color)) != float(next_color) or int(next_color) < 0 or int(next_color) >= int(colors):
                    print "invalid input"
                elif int(next_color) == B.store[0][0]:
                    print "invalid move"
                else:
                    valid = True
            except:
                print "invalid input"

        
        B.move(int(next_color))
        cnt += 1
        B.Display()
        print str(cnt) + '/' + str(B.expected)

    if cnt < B.expected:
        print "You Win!"
        return True
    else:
        print "You Lose, better luck next time"
        return False
