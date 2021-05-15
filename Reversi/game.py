from board import *

def PNGtoCoord(png):
    x = -1
    y = -1
    if png[0] not in ['a','b','c','d','e','f','g','h']:
        print "Invalid input: first character needs to be a letter from a-h, try again."
        return False
    try:
        y = int(png[1]) - 1
        if y < 0 or y > 7:
            print "Invalid input: second character needs to be an integer from 1-8, try again."
            return False
    except:
        print "Invalid input: second character needs to be an integer, try again."
        return False
    x = ['a','b','c','d','e','f','g','h'].index(png[0])
    return [y,x]

def Game_HH():
    B = reversi()
    print
    B.Display()

    while not B.isComplete():
        
        # Getting Black's move (black actually goes first)
        valid = False
        while not valid:

            # Checking if there exists no legal moves
            if B.LegalMoves(1) == []:
                print "Black has no legal moves."
                break
            else:
                print "Black to move."

            m = raw_input("Position: ")
            # error checking for correct input is done by PNGtoCoord()
            m = PNGtoCoord(m)

            if m != False:
                if B.board[m[0]][m[1]] != 0:
                    print "That position is occupied, try again."
                elif not B.validMove(m, 1):
                    print "Invalid move."
                else:
                    B.Move(m, 1)
                    print
                    B.Display()
                    valid = True

        # Getting White's move
        if not B.isComplete():
            valid = False
            while not valid:
                
                # Checking if there exists no legal moves
                if B.LegalMoves(2) == []:
                    print "White has no legal moves."
                    break
                else:
                    print "White to move."

                m = raw_input("Position: ")
                # error checking for correct input is done by PNGtoCoord()
                m = PNGtoCoord(m)

                if m != False:
                    if B.board[m[0]][m[1]] != 0:
                        print "That position is occupied, try again."
                    elif not B.validMove(m, 2):
                        print "Invalid move." 
                    else:
                        B.Move(m, 2)
                        print
                        B.Display()
                        valid = True
        
    return True
