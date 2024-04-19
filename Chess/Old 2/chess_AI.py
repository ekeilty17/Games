from chess_lib import *
from helper import *
from general_alphabeta_tree import *
from random import randint

#_______________________ "Random" AI _______________________#
def Random(board,player):
    other_player = 0
    if player == 10:
        other_player = 20
    if player == 20:
        other_player = 10

    count = 0
    out = []
    while out == [] and count < 20:
        #getting a random peice
        possible_piece = GetPlayerPositions(board, player)
        piece_pos = possible_piece[randint(0,len(possible_piece)-1)][1:3]

        #getting a random move
        possible_moves = GetPieceLegalMoves(board, piece_pos)
        #print possible_moves
        #some pieces will have no legal moves, and will throw an error
        if possible_moves != []:
            piece_new_pos = possible_moves[randint(0,len(possible_moves)-1)]

            #making an uncoupled temparay board
            temp = []
            for i in range(0,len(board)):
                temp += [list(board[i])]

            #make the move
            old_pos_val = temp[piece_new_pos[0]][piece_new_pos[1]]
            temp[piece_new_pos[0]][piece_new_pos[1]] = temp[piece_pos[0]][piece_pos[1]]
            temp[piece_pos[0]][piece_pos[1]] = 0
            #if move causes king to go into check, then we pick another move
            if not isInCheck(temp,player):
                out = [piece_pos, piece_new_pos]
        count += 1
    return out

#________________________ "Brute Force" _______________________#
#This is my main heuristic function that takes in a board state and outputs a rating
def countMaterial(board):
    accum = 0
    for i in range(0,8):
        for j in range(0,8):
            if board[i][j]/10 == 1:
                accum += pieceValue[board[i][j]%10]
            if board[i][j]/10 == 2:
                accum -= pieceValue[board[i][j]%10]
    return accum

#Another lower-weighted heuristic function
def positional(board):
    accum = 0
    for i in range(0,8):
        for j in range(0,8):
            #white
            if board[i][j]/10 == 1:
                #knight on the rim is dim
                if board[i][j]%10 == 1:
                    if j == 0 or j == 7:
                        accum -= 0.5
                #I want bishops back near own position
                elif board[i][j]%10 == 2:
                    if i == 1 or i == 2:
                        accum += 0.1
                if i > 4:
                    accum -= 0.1
            #black
            elif board[i][j]/10 == 2:
                #knight on the rim is dim
                if board[i][j]%10 == 1:
                    if j == 0 or j == 7:
                        accum += 0.5
                #I want bishops back near own position
                elif board[i][j]%10 == 2:
                    if i == 6 or i == 5:
                        accum -= 0.1
                if i < 3:
                    accum += 0.1
    if isCheckMate(board,10):
        accum -= 100
    elif isCheckMate(board,20):
        accum += 100
    return accum

class BruteForce_alphabeta_tree(general_alphabeta_tree):

    def __init__(self, val, player):
        isMaximizingPlayer = None
        if player == 10:
            isMaximizingPlayer = True
        else:
            isMaximizingPlayer = False
        general_alphabeta_tree.__init__(self, val, isMaximizingPlayer)
        self.player = player
        self.move = []

    def evaluation(self):
        return countMaterial(self.val.board) + positional(self.val.board)

    def isLeaf(self):
        if isCheckMate(self.val.board, self.player):
            return True
        # There are other cases, but I'm going to ignore them for now
        return False

    def getEdges(self):
        legal = []
        for i in range(0,8):
            for j in range(0,8):
                if self.val.board[i][j]/10 == self.player/10:
                    L = GetPieceLegalMoves(self.val.board, [i,j])
                    for pos in L:
                        legal += [[ [i,j], pos ]]
        return legal

    def copy_node(self):
        B = chess()
        B.board = self.val.gameboard()
        return BruteForce_alphabeta_tree( B, self.player )

    def evolve(self, E):
        # Parameter:        An Edge
        # Return Type:      Child class that implements the general_alphabeta_tree
        # Implementation:   REQUIRED
        self.val.Move(E[0], E[1])
        self.move = E
        return self

def Brute_Force(board, player):
    B = chess()
    B.board = board

    #depth = 2          # instantaneous
    depth = 3           # takes a few seconds
    bestChild = BruteForce_alphabeta_tree( B, player ).getBestChild(depth)
    print
    print "Computer Evaluation:",bestChild.evaluation()
    return bestChild.move


#_______________________ "Defensive" AI _______________________#

#Philosophy of the AI:
#       I coded this AI to make it as hard to beat as possible
#       However, it does not have an aggressive bone in it's body
#       It will not try to checkmate you or attack it
#       I equipt it with the most defensive opening in chess: the Hippopotamus Defense
#       It's actually quite hard to beat tbh

""" Starting with all the helper functions """

#Adding an opening book so that it has some direction at the beginning of the game
def Opening(board, player):
    if player == 10:
        hyppo_defence = [   [[1,6],[2,6]], #pawn up
                            [[0,5],[1,6]], #fienccetto bishop
                            [[1,3],[2,3]], #pawn up
                            [[1,0],[2,0]], #pawn up
                            [[0,1],[1,3]], #knight
                            [[1,4],[2,4]], #pawn up
                            [[0,6],[1,4]], #knight
                            [[1,1],[2,1]], #pawn up
                            [[0,2],[1,1]], #fienccetto biship
                            [[1,7],[2,7]], #pawn up
                            [[0,4],[0,5]], #king over
                            [[0,5],[0,6]], #king over
                            [[0,6],[1,7]], #king over
                            [[0,7],[0,5]], #rook over
                            [[1,7],[0,6]]  #king castled
                        ]
        hyppo_piece = [ 1, 3, 1, 1, 3, 1, 3, 1, 3, 1, 1000, 1000, 1000, 5, 1000, 0, 0, 0 ]
        for i in range(0,len(hyppo_defence)):
            m = hyppo_defence[i]
            if isLegalMove(board,m[0],m[1]) and pieceValue[board[m[0][0]][m[0][1]]%10] == hyppo_piece[i]:
                return [True, m]
    if player == 20:
        hyppo_defence = [   [[6,6],[5,6]], #pawn up
                            [[7,5],[6,6]], #fienccetto bishop
                            [[6,3],[5,3]], #pawn up
                            [[6,0],[5,0]], #pawn up
                            [[7,1],[6,3]], #knight
                            [[6,4],[5,4]], #pawn up
                            [[7,6],[6,4]], #knight
                            [[6,1],[5,1]], #pawn up
                            [[7,2],[6,1]], #fienccetto biship
                            [[6,7],[5,7]], #pawn up
                            [[7,4],[7,5]], #king over
                            [[7,5],[7,6]], #king over
                            [[7,6],[6,7]], #king over
                            [[7,7],[7,5]], #rook over
                            [[6,7],[7,6]]  #king castled
                        ]
        hyppo_piece = [ 1, 3, 1, 1, 3, 1, 3, 1, 3, 1, 1000, 1000, 1000, 5, 1000, 0, 0, 0 ]
        for i in range(0,len(hyppo_defence)):
            m = hyppo_defence[i]
            if isLegalMove(board,m[0],m[1]) and pieceValue[board[m[0][0]][m[0][1]]%10] == hyppo_piece[i]:
                return [True, m]
    return [False, []]

# This is really where the magic happens
# n is the min number of candidate moves I want to return
def candidateMoves(board, player, n):
    other_player = 0
    if player == 10:
        other_player = 20
    elif player == 20:
        other_player = 10

    player_pieces = []                  #positions of AI pieces
    other_player_pieces = []            #positions of opponent pieces
    legal = []                          #AI legal moves
    player_under_threat = []            #[ [pos, [players_attacking]], ... ]
    other_player_under_threat = []      #[ [pos, [players_attacking]], ... ]
    candidate = []                      #candidate moves
    #getting positions of AI player and of other player
    #getting legal moves of AI player
    for i in range(0,8):
        for j in range(0,8):
            if board[i][j]/10 == player/10:
                player_pieces += [[i,j]]
                legal += [[ [i,j], GetPieceLegalMoves(board, [i,j]) ]]
            if board[i][j]/10 == other_player/10:
                other_player_pieces += [[i,j]]

    #make sure the king isn't in check
    #if he is, we will deal with that in the loop after the one right below
    #check = isInCheck(board,player)
    #checking if AI's players are protected
    for L in legal:
        protected = isProtected(board,L[0])
        if not protected[0]:
            player_under_threat += [[L[0], protected[1]]]
    #iterating through legal moves and finding ones that causes
    #any of the threatened positions to become protected --> add to candidate moves
    if player_under_threat != []: #this is technically unnecarry, but better for time effieciency
        for L in legal:
            pos = L[0]
            for i in range(0,len(L[1])):
                new_pos = L[1][i]
                temp_board = copyBoard(board)
                temp_board[new_pos[0]][new_pos[1]] = temp_board[pos[0]][pos[1]]
                temp_board[pos[0]][pos[1]] = 0
                for p in player_under_threat:
                    #there are two scenarios:
                    #you moved the piece being attacked,
                    #   in which case you want to check if new_pos is protected
                    #or you moved a piece which blocked the attack
                    #   in which case you want to check if p[0] is protected
                    if pos == p[0]:
                        protected = isProtected(temp_board,new_pos)
                        if protected[0]:
                            candidate += [[pos,new_pos]]
                    else:
                        protected = isProtected(temp_board,p[0])
                        if protected[0]:
                            candidate += [[pos,new_pos]]
                #might not be clean, but computationally the
                #best way I could come up with
                #if check:
                    #if not isInCheck(temp_board,player):
                        #candidate += [[pos,new_pos]]


    #check if any of opponent's pieces are unprotected
    #if there is, add taking them to the list of candidate moves
    for p in other_player_pieces:
        protected = isProtected(board,p)
        if protected[0] != None:
            if not protected[0]:
                other_player_under_threat += [p]
    for L in legal:
        for i in range(0,len(L[1])):
            for p in other_player_under_threat:
                if p == L[1][i]:
                    candidate += [[L[0], L[1][i]]]

    #figure out what stage we are in in the opening,
    #and add the next stage to the list of candiate moves
    O = Opening(board,player)
    if O[0] == True:
        candidate += [O[1]]

    #add a random move just for fun
    while len(candidate) < n:
        out = Random(board,player)
        if out == []:
            break
        candidate += [Random(board,player)]

    return candidate


class Defensive_alphabeta_tree(general_alphabeta_tree):

    def __init__(self, val, player):
        isMaximizingPlayer = None
        if player == 10:
            isMaximizingPlayer = True
        else:
            isMaximizingPlayer = False
        general_alphabeta_tree.__init__(self, val, isMaximizingPlayer)
        self.player = player
        self.move = []

    def evaluation(self):
        return countMaterial(self.val.board) + positional(self.val.board)

    def isLeaf(self):
        if isCheckMate(self.val.board, self.player):
            return True
        # There are other cases, but I'm going to ignore them for now
        return False

    def getEdges(self):
        return candidateMoves(self.val.board, self.player, 5)

    def copy_node(self):
        B = chess()
        B.board = self.val.gameboard()
        return Defensive_alphabeta_tree( B, self.player )

    def evolve(self, E):
        # Parameter:        An Edge
        # Return Type:      Child class that implements the general_alphabeta_tree
        # Implementation:   REQUIRED
        self.val.Move(E[0], E[1])
        self.move = E
        return self



""" The actual AI """
def Defensive(board, player):
    B = chess()
    B.board = board

    #depth = 2          # instantaneous
    #depth = 3           # takes a few seconds
    depth = 4           # takes a few seconds
    bestChild = Defensive_alphabeta_tree( B, player ).getBestChild(depth)
    print
    if bestChild.isMaximizingPlayer:
        print "Computer Evaluation:",bestChild.beta
    else:
        print "Computer Evaluation:",bestChild.alpha
    return bestChild.move
