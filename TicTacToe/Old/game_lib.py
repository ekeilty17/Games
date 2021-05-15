from ttt_lib import *

def Game_HC(human,AI):
    if human != 1 and human != 2:
        return -1
    x = TicTacToe()
    print
    x.Display()
    state = 0

    if human == 1:
        while state == 0:
            #getting input from player 1
            p1_valid = False
            while p1_valid == False:
                p1 = raw_input("player 1 move: ")
                try:
                    Pos1 = int(p1)
                    if 0 > Pos1 or Pos1 >= len(x.board):
                        print "input is out of range, try again"
                    elif x.board[Pos1] != 0:
                        print "That spot is already taken! try again"
                    else:
                        p1_valid = True
                except:
                    print "input is not an integer, try again"
            x.Move(Pos1, 1)
            x.Display()
            state = x.AnalyzeBoard()

            #computer move
            if state == 0:
                comp = AI(x.board,2)
                x.Move(comp,2)
                x.Display()
                state = x.AnalyzeBoard()

    if human == 2:
        while state == 0:
            #computer move
            comp = AI(x.board,1)
            x.Move(comp,1)
            x.Display()
            state = x.AnalyzeBoard()

            if state == 0:
                p2_valid = False
            else:
                p2_valid = True
            #getting input from player 2
            while p2_valid == False:
                p2 = raw_input("player 2 move: ")
                try:
                    Pos2 = int(p2)
                    if 0 > Pos2 or Pos2 >= len(x.board):
                        print "input is out of range, try again"
                    elif x.board[Pos2] != 0:
                        print "That spot is already taken! try again"
                    else:
                        p2_valid = True
                except:
                    print "input is not an integer, try again"
            x.Move(Pos2, 2)
            x.Display()
            state = x.AnalyzeBoard()
    return state

def Game_CC(AI1, AI2):
    x = TicTacToe(3,3)
    print
    x.Display()
    state = 0

    while state == 0:
        #computer 1 move
        comp = AI1(x.board)
        x.Move(comp,1)
        x.Display()
        state = x.AnalyzeBoard()

        #computer 2 move
        if state == 0:
            comp = AI2(x.board)
            x.Move(comp,2)
            x.Display()
            state = x.AnalyzeBoard()
    return state

def Game_HH():
    x = TicTacToe()
    print
    x.Display()
    state = 0

    while state == 0:
        #getting input from player 1
        p1_valid = False
        while p1_valid == False:
            p1 = raw_input("player 1 move: ")
            try:
                Pos1 = int(p1)
                if 0 > Pos1 or Pos1 >= len(x.board):
                    print "input is out of range, try again"
                elif x.board[Pos1] != 0:
                    print "That spot is already taken! try again"
                else:
                    p1_valid = True
            except:
                print "input is not an integer, try again"
        x.Move(Pos1, 1)
        x.Display()
        state = x.AnalyzeBoard()

        if state == 0:
            p2_valid = False
        else:
            p2_valid = True
        #getting input from player 2
        while p2_valid == False:
            p2 = raw_input("player 2 move: ")
            try:
                Pos2 = int(p2)
                if 0 > Pos2 or Pos2 >= len(x.board):
                    print "input is out of range, try again"
                elif x.board[Pos2] != 0:
                    print "That spot is already taken! try again"
                else:
                    p2_valid = True
            except:
                print "input is not an integer, try again"
        x.Move(Pos2, 2)
        x.Display()
        state = x.AnalyzeBoard()
    return state

def output(state):
    if state == -1:
        return "Error"
    elif state == 0:
        return "Incomplete"
    elif state == 1:
        return "X Wins"
    elif state == 2:
        return "O Wins"
    else:
        return "Draw"
