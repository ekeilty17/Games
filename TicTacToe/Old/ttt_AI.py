from tree import *
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
        #rows
        if ((board[0+3*i] == board[1+3*i] == player) and (board[2+3*i] == 0)):
            return 2+3*i
        elif ((board[1+3*i] == board[2+3*i] == player) and (board[0+3*i] == 0)):
            return 0+3*i
        elif ((board[0+3*i] == board[2+3*i] == player) and (board[1+3*i] == 0)):
            return 1+3*i
        #columns
        if ((board[0+i] == board[3+i] == player) and (board[6+i] == 0)):
            return 6+i
        elif ((board[3+i] == board[6+i] == player) and (board[0+i] == 0)):
            return 0+i
        elif ((board[0+i] == board[6+i] == player) and (board[3+i] == 0)):
            return 3+i

    #diagonal 1
    if ((board[0] == board[4] == player) and (board[8] == 0)):
        return 8
    elif ((board[4] == board[8] == player) and (board[0] == 0)):
        return 0
    elif ((board[0] == board[8] == player) and (board[4] == 0)):
        return 4

    #diagonal 2
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
# We are only using this function to evaluate a completed board
# We will us it to run a max-min back propogation up a heuristric tree
def AnalyzeBoard(T):
    #return list
    #1: X wins
    #-1: O wins
    #0: draw

    #unfortunately this is specific to a 3x3
    #bc I couldn't be bottered to find a general way
    for i in range(0,3):
        #rows
        if (T[0+i*3] == T[1+i*3] == T[2+i*3] == 1):
            return 1
        if (T[0+i*3] == T[1+i*3] == T[2+i*3] == 2):
            return -1

        #collumns
        if (T[0+i] == T[3+i] == T[6+i] == 1):
            return 1
        if (T[0+i] == T[3+i] == T[6+i] == 2):
            return -1

    #diagonals
    if (T[0] == T[4] == T[8] == 1):
        return 1
    if (T[0] == T[4] == T[8] == 2):
        return -1
    if (T[2] == T[4] == T[6] == 1):
        return 1
    if (T[2] == T[4] == T[6] == 2):
        return -1

    return 0

#get unoccupied squares on the board
def get_empty(board):
    out = []
    for i in range(len(board)):
        if board[i] == 0:
            out += [i]
    return out

#make a move without affecting the game board
def make_move(board, move, player):
    new_board = list(board)
    new_board[move] = player
    return new_board

#generate a search tree
def genTree(root, player):
    if root == None:
        return False

    #enumerate child list with all possible moves
    empty = get_empty(root.val)
    #The base case to stop the recursion
    if empty == []:
        return False

    #adding a child for each element in empty
    for m in empty:
        root.AddSuccessor(tree(make_move(root.val,m,player)))

    #calling function recursively on each child
    other_player = 0
    if player == 1:
        other_player = 2
    elif player == 2:
        other_player = 1
    for b in root.children:
        genTree(b,other_player)

    return True

#add heuristics to the search tree
def addHeuristic(root,player):
    if root == None:
        return False

    other_player = 0
    if player == 10:
        other_player = 20
    else:
        other_player = 10

    for child in root.children:
        addHeuristic(child,other_player)

    # base case
    if root.children == []:
        # This means we made it to the end of the trees
        # Therefore I evaluate the results and assign a hueristic
        root.heuristic = AnalyzeBoard(root.val)
    else:
        #Otherwise I take the maximum heuristric of the parent and
        heuristic_list = []
        for child in root.children:
            heuristic_list += [child.heuristic]
        if player == 1:
            root.heuristic = root.children[heuristic_list.index(max(heuristic_list))].heuristic
        else:
            root.heuristic = root.children[heuristic_list.index(min(heuristic_list))].heuristic

#compare the root with the child to figure out what the move that was made was
def get_move(original_board, altered_board):
    for i in range(len(original_board)):
        if original_board[i] != altered_board[i]:
            return i
    return -1

""" Looks at every possible move to determine what the best next move is """
def Brute_Force(board,player):
    #get easy instances out of the way
    if genWinningMove(board,player) != -1:
        return genWinningMove(board,player)
    if genNonLoser(board,player) != -1:
        return genNonLoser(board,player)

    #creating a tree of all possible board and assigning heuristics
    board_tree = tree(board)
    genTree(board_tree, player)
    addHeuristic(board_tree, player)

    #If it comes up with no moves
    if board_tree.children == []:
        return Competent(board,player)

    #getting child with highest heuristic
    heuristic_list = []
    for child in board_tree.children:
        heuristic_list += [child.heuristic]
    move = -1
    if player == 1:
        move = get_move(board, board_tree.children[heuristic_list.index(max(heuristic_list))].val)
    else:
        move = get_move(board, board_tree.children[heuristic_list.index(min(heuristic_list))].val)

    if move != -1:
        return move
    else:
        return Competent(board,player)
