from general_alphabeta_tree import *
from ttt_lib import *
from random import randint


#__________________ "Random" AI __________________#
""" Just makes a random move """
def Random(board,player):
    possible_moves = []
    for i in range(0,len(board)):
        if board[i] == 0:
            possible_moves += [i]
    return possible_moves[randint(0,len(possible_moves)-1)]


#__________________ "Competent" AI __________________#
def genWinningMove(board,player):
    for i in range(0,3):
        # rows
        if ((board[0+3*i] == board[1+3*i] == player) and (board[2+3*i] == 0)):
            return 2+3*i
        elif ((board[1+3*i] == board[2+3*i] == player) and (board[0+3*i] == 0)):
            return 0+3*i
        elif ((board[0+3*i] == board[2+3*i] == player) and (board[1+3*i] == 0)):
            return 1+3*i
        # columns
        if ((board[0+i] == board[3+i] == player) and (board[6+i] == 0)):
            return 6+i
        elif ((board[3+i] == board[6+i] == player) and (board[0+i] == 0)):
            return 0+i
        elif ((board[0+i] == board[6+i] == player) and (board[3+i] == 0)):
            return 3+i

    # diagonal 1
    if ((board[0] == board[4] == player) and (board[8] == 0)):
        return 8
    elif ((board[4] == board[8] == player) and (board[0] == 0)):
        return 0
    elif ((board[0] == board[8] == player) and (board[4] == 0)):
        return 4

    # diagonal 2
    if ((board[2] == board[4] == player)) and (board[6] == 0):
        return 6
    elif ((board[4] == board[6] == player) and (board[2] == 0)):
        return 2
    elif ((board[2] == board[6] == player) and (board[4] == 0)):
        return 4

    return -1

def genNonLoser(board,player):
    if (player == 1):
        return genWinningMove(board,2)
    elif (player == 2):
        return genWinningMove(board,1)
    else:
        return -1

""" If it can win it will win and it will block obvious attempts to win
    However, it has no fore-sight and therefore can be tricked          """
def Competent(board, player):
    if genWinningMove(board,player) != -1:
        return genWinningMove(board,player)
    if genNonLoser(board,player) != -1:
        return genNonLoser(board,player)
    return Random(board,player)


#__________________ "Brute Force" AI __________________#
class TicTacToe_alphabeta_tree(general_alphabeta_tree):

    def __init__(self, val, isMaximizingPlayer=True):
        general_alphabeta_tree.__init__(self, val, isMaximizingPlayer)

    def evaluation(self):
        x = self.val.AnalyzeBoard()
        if x == 1:
            return 1
        elif x == 2:
            return -1
        elif x == 3:
            return 0
        else:
            return None

    def isLeaf(self):
        if self.val.AnalyzeBoard() == 0:
            return False
        return True

    def getEdges(self):
        player = None
        if self.isMaximizingPlayer == True:
            player = 1
        else:
            player = 2
        empty = []
        for i in range(len(self.val.board)):
            if self.val.board[i] == 0:
                empty += [[i, player]]
        return empty

    def copy_node(self):
        return TicTacToe_alphabeta_tree( self.val.copy(), self.isMaximizingPlayer )

    def evolve(self, E):
        self.val.Move(E[0], E[1])
        return self

""" Uses an alpha-beta pruning algorithm to search through all possible possible
    and finds the best move in the position. Should never lose.                 """
def Brute_Force(board_state, player):
    B = TicTacToe()
    B.board = list(board_state)

    isMax = None
    if player == 1:
        isMax = True
    else:
        isMax = False

    # Getting child with maximum evaluation
    C = TicTacToe_alphabeta_tree( B, isMax ).getBestChild(-1)

    # If there exist no children
    if C == False:
        return False

    # Finding the edge from the current board state to the child board state
    for i in range(len(B.board)):
        if B.board[i] != C.val.board[i]:
            return i
