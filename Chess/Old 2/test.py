from chess_lib import *
from chess_AI import *

def PNGtoCoord(png):
    x = -1
    y = -1
    if png[0] not in ['a','b','c','d','e','f','g','h']:
        print "invalid row input, try again"
        return False
    try:
        y = int(png[1]) - 1
        if y < 0 or y > 7:
            print "file is out of range, try again"
            return False
    except:
        print "file was not an integer, try again"
        return False
    x = ['a','b','c','d','e','f','g','h'].index(png[0])
    return [y,x]

def Test(custom_board):
    x = chess()
    x.board = custom_board
    x.Display()
    mate = False
    winner = 0

    while not mate:
        p1_valid = False
        while p1_valid == False:
            print "White to move"
            p1_piece = raw_input("Piece Position: ")
            p1_move = raw_input("Piece Destination: ")
            pos = PNGtoCoord(p1_piece)
            new_pos = PNGtoCoord(p1_move)

            if pos and new_pos:
                if x.board[pos[0]][pos[1]] not in range(10,16):
                    print "not one of your pieces, try again"
                elif not isLegalMove(x.board,pos,new_pos):
                    print "not a legal move, try again"
                else:
                    p1_valid = True
            if p1_valid:
                success = x.Move(pos,new_pos)
                #check if white's move causes white's king to be in check
                if not success:
                    print "The king is in check, try again"
                    p1_valid = False
            x.Display()
        mate = isCheckMate(x.board,20)
        if mate:
            winner = 10
            print "White Wins!"

        if not mate:
            p2_valid = False
            while p2_valid == False:
                print "Black to move"
                p2_piece = raw_input("Piece Position: ")
                p2_move = raw_input("Piece Destination: ")
                pos = PNGtoCoord(p2_piece)
                new_pos = PNGtoCoord(p2_move)

                if pos and new_pos:
                    if x.board[pos[0]][pos[1]] not in range(20,26):
                        print "not one of your pieces, try again"
                    elif not isLegalMove(x.board,pos,new_pos):
                        print "not a legal move, try again"
                    else:
                        p2_valid = True
                if p2_valid:
                    success = x.Move(pos,new_pos)
                    #check if black's move causes black's king to be in check
                    if not success:
                        print "The king is in check, try again"
                        p2_valid = False
                x.Display()
            mate = isCheckMate(x.board,10)
            if mate:
                winner = 20
                print "Black Wins!"
    return winner

castle_test = [     [13, 0, 0, 0, 15, 0, 0, 13],
                    [10, 10, 10, 10, 10, 10, 10, 10],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [20, 20, 20, 20, 20, 20, 20, 20],
                    [23, 0, 0, 0, 25, 0, 0, 23]
                 ]

queening_test = [   [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 20],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 10],
                    [0, 0, 0, 0, 0, 0, 0, 0]
                 ]

Test(queening_test)
