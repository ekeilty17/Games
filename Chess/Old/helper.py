#output: [[piece, row, col], [piece, row, col], ... ]
def GetPlayerPositions(board, player):
    out = []
    for i in range(0,8):
        for j in range(0,8):
            if 10 <= board[i][j] and board[i][j] < 20 and player == 10:
                out += [[board[i][j], i, j]]
            if 20 <= board[i][j] and player == 20:
                out += [[board[i][j], i, j]]
    return out

def outRange(i,j):
    if i < 0:
        return True
    if i > 7:
        return True
    if j < 0:
        return True
    if j > 7:
        return True
    return False

#output: [[row, col], [row, col], ... ]
def GetPieceLegalMoves(board, position):
    #I need to add a function that checks if the previous move
    #caused the king to go into check
    r = position[0]
    c = position[1]
    out = []
    if board[r][c] == 0: #position has no peice
        return out
    #pawns
    elif board[r][c]%10 == 0:
        #print "pawn"
        if board[r][c] == 10: #white pawn
            if (not outRange(r+1, c-1)) and (board[r+1][c-1] in range(20,26)):
                out += [[r+1, c-1]] #takes diagonally to the left
            if (not outRange(r+1, c)) and board[r+1][c] == 0:
                out += [[r+1, c]] #can move one step forward
            if (not outRange(r+1, c+1)) and (board[r+1][c+1] in range(20,26)):
                out += [[r+1, c+1]] #takes diagonally to the right
        if board[r][c] == 20:
            if (not outRange(r-1, c-1)) and (board[r-1][c-1] in range(10,20)):
                out += [[r-1, c-1]] #takes diagonally to the left
            if (not outRange(r-1, c)) and board[r-1][c] == 0:
                out += [[r-1, c]] #can move one step forward
            if (not outRange(r-1, c+1)) and (board[r-1][c+1] in range(10,20)):
                out += [[r-1, c+1]] #takes diagonally to the right
        return out
    #Knight
    elif board[r][c]%10 == 1:
        #print "Knight"
        possible = [[r+1,c+2], [r+2,c+1],
                    [r+2,c-1], [r+1,c-2],
                    [r-1,c-2], [r-2,c-1],
                    [r-2,c+1], [r-1,c+2]]
        #remove moves that are out of range
        particular = []
        for e in possible:
            if not outRange(e[0],e[1]):
                particular += [e]
        #removing squares occupied by own peices
        for e in particular:
            if board[e[0]][e[1]]/10 != board[r][c]/10:
                out += [e]
        return out
    #Bishop
    elif board[r][c]%10 == 2:
        #print "Bishop"
        #order is important here, must go closest to farthest
        possible = [[[r+1,c+1], [r+2,c+2], [r+3,c+3], [r+4,c+4], [r+5,c+5], [r+6,c+6], [r+7,c+7]],
                    [[r+1,c-1], [r+2,c-2], [r+3,c-3], [r+4,c-4], [r+5,c-5], [r+6,c-6], [r+7,c-7]],
                    [[r-1,c-1], [r-2,c-2], [r-3,c-3], [r-4,c-4], [r-5,c-5], [r-6,c-6], [r-7,c-7]],
                    [[r-1,c+1], [r-2,c+2], [r-3,c+3], [r-4,c+4], [r-5,c+5], [r-6,c+6], [r-7,c+7]]]
        #remove moves that are out of range
        particular = []
        for d in possible:
            temp = []
            for e in d:
                if not outRange(e[0],e[1]):
                    temp += [e]
            particular += [temp]
        #d stands for diagonal
        for d in particular:
            for i in range(0,len(d)):
                #this checks each diagonal
                #if there is something obstructing the diagonal,
                #then it stops checking the rest and doesnt add them
                if board[d[i][0]][d[i][1]] == 0:
                    out += [d[i]]
                elif board[d[i][0]][d[i][1]]/10 == board[r][c]/10: #obstructed by it's own piece
                    break
                else:
                    #opponent piece is obstructing it
                    out += [d[i]]
                    break
        return out
    #Rook
    elif board[r][c]%10 == 3:
        #print "Rook"
        possible = [[[r,c+1], [r,c+2], [r,c+3], [r,c+4], [r,c+5], [r,c+6], [r,c+7]],
                    [[r,c-1], [r,c-2], [r,c-3], [r,c-4], [r,c-5], [r,c-6], [r,c-7]],
                    [[r+1,c], [r+2,c], [r+3,c], [r+4,c], [r+5,c], [r+6,c], [r+7,c]],
                    [[r-1,c], [r-2,c], [r-3,c], [r-4,c], [r-5,c], [r-6,c], [r-7,c]]]
        #remove moves that are out of range
        particular = []
        for f in possible:
            temp = []
            for e in f:
                if not outRange(e[0],e[1]):
                    temp += [e]
            particular += [temp]
        #f stands for file
        for f in particular:
            for i in range(0,len(f)):
                #this checks each row or file
                #if there is something obstructing the row or file,
                #then it stops checking the rest and doesnt add them
                if board[f[i][0]][f[i][1]] == 0:
                    out += [f[i]]
                elif board[f[i][0]][f[i][1]]/10 == board[r][c]/10: #obstructed by it's own piece
                    break
                else:
                    #opponent is obstructing
                    out += [f[i]]
                    break
        return out
    #Queen
    elif board[r][c]%10 == 4:
        #print "Queen"
        #order is important here, must go closest to farthest
        possible = [[[r+1,c+1], [r+2,c+2], [r+3,c+3], [r+4,c+4], [r+5,c+5], [r+6,c+6], [r+7,c+7]],
                    [[r+1,c-1], [r+2,c-2], [r+3,c-3], [r+4,c-4], [r+5,c-5], [r+6,c-6], [r+7,c-7]],
                    [[r-1,c-1], [r-2,c-2], [r-3,c-3], [r-4,c-4], [r-5,c-5], [r-6,c-6], [r-7,c-7]],
                    [[r-1,c+1], [r-2,c+2], [r-3,c+3], [r-4,c+4], [r-5,c+5], [r-6,c+6], [r-7,c+7]]]
        #remove moves that are out of range
        particular = []
        for d in possible:
            temp = []
            for e in d:
                if not outRange(e[0],e[1]):
                    temp += [e]
            particular += [temp]
        #d stands for diagonal
        for d in particular:
            for i in range(0,len(d)):
                #this checks each diagonal
                #if there is something obstructing the diagonal,
                #then it stops checking the rest and doesnt add them
                if board[d[i][0]][d[i][1]] == 0:
                    out += [d[i]]
                elif board[d[i][0]][d[i][1]]/10 == board[r][c]/10: #obstructed by it's own piece
                    break
                else:
                    #opponent obstructing
                    out += [d[i]]
                    break

        possible = [[[r,c+1], [r,c+2], [r,c+3], [r,c+4], [r,c+5], [r,c+6], [r,c+7]],
                    [[r,c-1], [r,c-2], [r,c-3], [r,c-4], [r,c-5], [r,c-6], [r,c-7]],
                    [[r+1,c], [r+2,c], [r+3,c], [r+4,c], [r+5,c], [r+6,c], [r+7,c]],
                    [[r-1,c], [r-2,c], [r-3,c], [r-4,c], [r-5,c], [r-6,c], [r-7,c]]]
        #remove moves that are out of range
        particular = []
        for f in possible:
            temp = []
            for e in f:
                if not outRange(e[0],e[1]):
                    temp += [e]
            particular += [temp]
        #f stands for file
        for f in particular:
            for i in range(0,len(f)):
                #this checks each row or file
                #if there is something obstructing the row or file,
                #then it stops checking the rest and doesnt add them
                if board[f[i][0]][f[i][1]] == 0:
                    out += [f[i]]
                elif board[f[i][0]][f[i][1]]/10 == board[r][c]/10: #obstructed by it's own piece
                    break
                else:
                    #opponent obstructing
                    out += [f[i]]
                    break
        return out
    #King
    elif board[r][c]%10 == 5:
        #print "King"
        possible = [[r-1,c-1], [r-1,c], [r-1,c+1],
                    [r,c-1], [r,c+1],
                    [r+1,c-1], [r+1,c], [r+1,c+1]]
        #remove moves that are out of range
        particular = []
        for e in possible:
            if not outRange(e[0],e[1]):
                particular += [e]
        #remove moves that are obstructed by own pieces
        for e in particular:
            if board[e[0]][e[1]]/10 != board[r][c]/10:
                out += [e]
        """
        if outRange(r-1, c-1) and board[r-1][c-1] == 0:
            out += [[r-1, c-1]]
        if outRange(r-1, c) and board[r-1][c] == 0:
            out += [[r-1,c]]
        if outRange(r-1, c+1) and board[r-1][c+1] == 0:
            out += [[r-1,c+1]]
        if outRange(r, c-1) and board[r][c-1] == 0:
            out += [[r,c-1]]
        if outRange(r, c+1) and board[r][c+1] == 0:
            out += [[r,c+1]]
        if outRange(r+1, c-1) and board[r+1][c-1] == 0:
            out += [[r+1,c-1]]
        if outRange(r+1, c) and board[r+1][c] == 0:
            out += [[r+1,c]]
        if outRange(r+1, c+1) and board[r+1][c+1] == 0:
            out += [[r+1,c+1]]
        """
        return out

#this one includes the players own pieces...useful for later functions
def GetPieceLegalMoves2(board, position):
    r = position[0]
    c = position[1]
    out = []
    if board[r][c] == 0: #position has no peice
        return out
    #pawns
    elif board[r][c]%10 == 0:
        if board[r][c] == 10: #white pawn
            if not outRange(r+1, c-1):
                out += [[r+1, c-1]] #takes diagonally to the left
            if not outRange(r+1, c+1):
                out += [[r+1, c+1]] #takes diagonally to the right
        if board[r][c] == 20:
            if not outRange(r-1, c-1):
                out += [[r-1, c-1]] #takes diagonally to the left
            if not outRange(r-1, c+1):
                out += [[r-1, c+1]] #takes diagonally to the right
        return out
    #Knight
    elif board[r][c]%10 == 1:
        possible = [[r+1,c+2], [r+2,c+1],
                    [r+2,c-1], [r+1,c-2],
                    [r-1,c-2], [r-2,c-1],
                    [r-2,c+1], [r-1,c+2]]
        particular = []
        for e in possible:
            if not outRange(e[0],e[1]):
                particular += [e]
        out = particular
        return out
    #Bishop
    elif board[r][c]%10 == 2:
        possible = [[[r+1,c+1], [r+2,c+2], [r+3,c+3], [r+4,c+4], [r+5,c+5], [r+6,c+6], [r+7,c+7]],
                    [[r+1,c-1], [r+2,c-2], [r+3,c-3], [r+4,c-4], [r+5,c-5], [r+6,c-6], [r+7,c-7]],
                    [[r-1,c-1], [r-2,c-2], [r-3,c-3], [r-4,c-4], [r-5,c-5], [r-6,c-6], [r-7,c-7]],
                    [[r-1,c+1], [r-2,c+2], [r-3,c+3], [r-4,c+4], [r-5,c+5], [r-6,c+6], [r-7,c+7]]]
        #remove moves that are out of range
        particular = []
        for d in possible:
            temp = []
            for e in d:
                if not outRange(e[0],e[1]):
                    temp += [e]
            particular += [temp]
        #d stands for diagonal
        for d in particular:
            for i in range(0,len(d)):
                if board[d[i][0]][d[i][1]] == 0:
                    out += [d[i]]
                elif board[d[i][0]][d[i][1]]/10 == board[r][c]/10: #obstructed by it's own piece
                    out += [d[i]]
                    break
                else:
                    #opponent piece is obstructing it
                    out += [d[i]]
                    break
        return out
    #Rook
    elif board[r][c]%10 == 3:
        possible = [[[r,c+1], [r,c+2], [r,c+3], [r,c+4], [r,c+5], [r,c+6], [r,c+7]],
                    [[r,c-1], [r,c-2], [r,c-3], [r,c-4], [r,c-5], [r,c-6], [r,c-7]],
                    [[r+1,c], [r+2,c], [r+3,c], [r+4,c], [r+5,c], [r+6,c], [r+7,c]],
                    [[r-1,c], [r-2,c], [r-3,c], [r-4,c], [r-5,c], [r-6,c], [r-7,c]]]
        particular = []
        for f in possible:
            temp = []
            for e in f:
                if not outRange(e[0],e[1]):
                    temp += [e]
            particular += [temp]
        #f stands for file
        for f in particular:
            for i in range(0,len(f)):
                if board[f[i][0]][f[i][1]] == 0:
                    out += [f[i]]
                elif board[f[i][0]][f[i][1]]/10 == board[r][c]/10: #obstructed by it's own piece
                    out += [f[i]]
                    break
                else:
                    #opponent is obstructing
                    out += [f[i]]
                    break
        return out
    #Queen
    elif board[r][c]%10 == 4:
        possible = [[[r+1,c+1], [r+2,c+2], [r+3,c+3], [r+4,c+4], [r+5,c+5], [r+6,c+6], [r+7,c+7]],
                    [[r+1,c-1], [r+2,c-2], [r+3,c-3], [r+4,c-4], [r+5,c-5], [r+6,c-6], [r+7,c-7]],
                    [[r-1,c-1], [r-2,c-2], [r-3,c-3], [r-4,c-4], [r-5,c-5], [r-6,c-6], [r-7,c-7]],
                    [[r-1,c+1], [r-2,c+2], [r-3,c+3], [r-4,c+4], [r-5,c+5], [r-6,c+6], [r-7,c+7]]]
        particular = []
        for d in possible:
            temp = []
            for e in d:
                if not outRange(e[0],e[1]):
                    temp += [e]
            particular += [temp]
        #d stands for diagonal
        for d in particular:
            for i in range(0,len(d)):
                if board[d[i][0]][d[i][1]] == 0:
                    out += [d[i]]
                elif board[d[i][0]][d[i][1]]/10 == board[r][c]/10: #obstructed by it's own piece
                    out += [d[i]]
                    break
                else:
                    #opponent obstructing
                    out += [d[i]]
                    break

        possible = [[[r,c+1], [r,c+2], [r,c+3], [r,c+4], [r,c+5], [r,c+6], [r,c+7]],
                    [[r,c-1], [r,c-2], [r,c-3], [r,c-4], [r,c-5], [r,c-6], [r,c-7]],
                    [[r+1,c], [r+2,c], [r+3,c], [r+4,c], [r+5,c], [r+6,c], [r+7,c]],
                    [[r-1,c], [r-2,c], [r-3,c], [r-4,c], [r-5,c], [r-6,c], [r-7,c]]]
        particular = []
        for f in possible:
            temp = []
            for e in f:
                if not outRange(e[0],e[1]):
                    temp += [e]
            particular += [temp]
        #f stands for file
        for f in particular:
            for i in range(0,len(f)):
                if board[f[i][0]][f[i][1]] == 0:
                    out += [f[i]]
                elif board[f[i][0]][f[i][1]]/10 == board[r][c]/10: #obstructed by it's own piece
                    out += [f[i]]
                    break
                else:
                    #opponent obstructing
                    out += [f[i]]
                    break
        return out
    #King
    elif board[r][c]%10 == 5:
        #print "King"
        possible = [[r-1,c-1], [r-1,c], [r-1,c+1],
                    [r,c-1], [r,c+1],
                    [r+1,c-1], [r+1,c], [r+1,c+1]]
        particular = []
        for e in possible:
            if not outRange(e[0],e[1]):
                particular += [e]
        out = particular
        return out

def isLegalMove(board,pos,new_pos):
    if new_pos in GetPieceLegalMoves(board, pos):
        return True
    return False

def isInCheck(board,player):
    #finding the position of the king
    king = []
    for i in range(0,8):
        for j in range(0,8):
            if board[i][j] == player + 5:
                king = [i,j]

    other_player = 0
    if player == 10:
        other_player = 20
    if player == 20:
        other_player = 10

    #checking if the king is in check
    #technically we could check for every piece on the board
    #but so save time we will just check the valid moves of 
    #the opposing player
    for i in range(0,8):
        for j in range(0,8):
            #only care if other player is attacking our king
            if board[i][j]/10 == other_player/10:
                if king in GetPieceLegalMoves(board, [i,j]):
                    return True
    return False

def findOutCheck(board,player):
    allLegalMoves = []
    out = []
    #this will be of the form [ [[i,j], [legal_move, legal_move, ...]], ... ]
    #this will give us the index of all players and then 
    for i in range(0,8):
        for j in range(0,8):
            #only care if other player is attacking our king
            if board[i][j]/10 == player/10:
                allLegalMoves += [ [[i,j], GetPieceLegalMoves(board, [i,j])] ]

    #now we iterate thorugh all legal moves and see if any cause the king to not be in check
    for e in allLegalMoves:
        for i in range(0, len(e[1])):
            #need to construt a duplicate board
            #since it's a list of lists I need to need to de-couple all the inner lists
            temp = []
            for l in range(0,len(board)):
                temp += [list(board[l])]
            #making the move
            pos = e[0]
            new_pos = e[1][i]
            temp[new_pos[0]][new_pos[1]] = temp[pos[0]][pos[1]]
            temp[pos[0]][pos[1]] = 0
            #checking if it can cause the king to not be in check
            if not isInCheck(temp,player):
                out += [[pos,new_pos]]
    return out 

def isCheckMate(board, player):
    if not isInCheck(board, player):
        return False
    allLegalMoves = []
    
    #this will be of the form [ [[i,j], [legal_move, legal_move, ...]], ... ]
    #this will give us the index of all players and then 
    for i in range(0,8):
        for j in range(0,8):
            #only care if other player is attacking our king
            if board[i][j]/10 == player/10:
                allLegalMoves += [ [[i,j], GetPieceLegalMoves(board, [i,j])] ]
    
    #now we iterate thorugh all legal moves and see if any cause the king to not be in check
    for e in allLegalMoves:
        for i in range(0, len(e[1])):
            #need to construt a duplicate board
            #since it's a list of lists I need to need to de-couple all the inner lists
            temp = []
            for l in range(0,len(board)):
                temp += [list(board[l])]
            #making the move
            pos = e[0]
            new_pos = e[1][i]
            temp[new_pos[0]][new_pos[1]] = temp[pos[0]][pos[1]]
            temp[pos[0]][pos[1]] = 0 
            #checking if it can cause the king to not be in check
            if not isInCheck(temp,player):
                return False
    return True

def copyBoard(board):
    out = []
    for r in board:
        out += [list(r)]
    return out

pieceValue = {  0: 1,
                1: 3,
                2: 3,
                3: 5,
                4: 9,
                5: 1000
              }

def whoAttacking(board,position,player):
    squaresAttacked = []
    out = []
    #this will be of the form [[piece_loc, [legal_move, legal_move, ...]], [piece_loc, [legal_move, legal_move, ...]], ...]
    #this will give us the index of all players and then 
    for i in range(0,8):
        for j in range(0,8):
            #iterating through all white positions
            if board[i][j]/10 == player/10:
                squaresAttacked += [[[i,j], GetPieceLegalMoves2(board, [i,j])]]
    #if the piece exists in the legal moves list, then it is being attacked (or defended)
    for L in squaresAttacked:
        if position in L[1]:
            out += [L[0]]
    #so we need to account for the situation where pieces are lined up and attacking/defending
    #I am removing all attackers from the board
    new_board = copyBoard(board)
    for attacker in out:
        new_board[attacker[0]][attacker[1]] = 0
    #and then running the same code again basically
    squaresAttacked = []
    for i in range(0,8):
        for j in range(0,8):
            #iterating through all white positions in the new board that doesnt have the previous attackers
            if board[i][j]/10 == player/10:
                squaresAttacked += [[[i,j], GetPieceLegalMoves2(new_board, [i,j])]]
    for L in squaresAttacked:
        if position in L[1]:
            out += [L[0]] 
    
    #and technically I should check an arbitrary number of times, but realistically you will only
    #ever have 3 pieces in a line: queen, rook, rook or queen, bishop, pawn
    #so we do it one more time
    for attacker in out:
        new_board[attacker[0]][attacker[1]] = 0
    #and then running the same code again basically
    squaresAttacked = []
    for i in range(0,8):
        for j in range(0,8):
            #iterating through all white positions in the new board that doesnt have the previous attackers
            if board[i][j]/10 == player/10:
                squaresAttacked += [[[i,j], GetPieceLegalMoves2(new_board, [i,j])]]
    for L in squaresAttacked:
        if position in L[1]:
            out += [L[0]] 
    return out

def numAttackers(board,position,player):
    return len(whoAttacking(board,position,player))

def isProtected(board, pos):
    #if position contains a white peice
    if board[pos[0]][pos[1]]/10 == 1:
        #getting attackers and defenders
        white_attack = whoAttacking(board,pos,10)
        black_attack = whoAttacking(board,pos,20)
        #getting values of all attackers and defenders
        white_val = []
        black_val = []
        for i in range(0,len(white_attack)):
            p = white_attack[i]
            white_val += [pieceValue[board[p[0]][p[1]]%10]]
        for i in range(0,len(black_attack)):
            p = black_attack[i]
            black_val += [pieceValue[board[p[0]][p[1]]%20]]
        
        #if there are no attackers --> protected
        if black_val == []:
            return [True, black_attack]
        
        #if there exists attackers and no defenders --> not protected
        if white_val == [] and black_val != []:
            return [False, black_attack]

        #if exists Value[attacker] < Value[piece] --> not protected
        for p in black_val:
            if p < pieceValue[board[pos[0]][pos[1]]%10]:
                return [False, black_attack]

        #make lists that we can manipulate
        white_take = list(white_val)
        black_take = list(black_val)
        
        #first we order the lists to be in the order that they would take in
        white_take.sort()
        white_take = [pieceValue[board[pos[0]][pos[1]]%10]] + white_take
        #white_tae = white_take[:len(white_take)-1] #since the last piece cannot be taken
        black_take.sort()
        
        #okay so here's the premise, black can stop taking whenever he wants
        #so if there ever exists a time where black can stop taking and be up material
        #then the piece is not protected
        white_lost = []
        black_lost = []
        while True:
            if black_take != []:
                white_lost += [white_take[0]]
                white_take = white_take[1:]
            else:
                #black can't take any more peices
                #if white lost more material than black, the piece was not protected
                if sum(white_lost) > sum(black_lost):
                    return [False, black_attack]
                else:
                    return [True, black_attack]
            if white_take != []:
                black_lost += [black_take[0]]
                black_take = black_take[1:]
            else:
                if sum(white_lost) > sum(black_lost):
                    return [False, black_attack]
                else:
                    return [True, black_attack]
        return [True, black_attack]
        
    #if position contains a black piece
    if board[pos[0]][pos[1]]/10 == 2:
        #getting attackers and defenders
        white_attack = whoAttacking(board,pos,10)
        black_attack = whoAttacking(board,pos,20)
        #getting values of all attackers and defenders
        white_val = []
        black_val = []
        for i in range(0,len(white_attack)):
            p = white_attack[i]
            white_val += [pieceValue[board[p[0]][p[1]]%10]]
        for i in range(0,len(black_attack)):
            p = black_attack[i]
            black_val += [pieceValue[board[p[0]][p[1]]%20]]
        
        #if there are no attackers --> protected
        if white_val == []:
            return [True, white_attack]

        #if there exists attackers and no defenders --> not protected
        if black_val == [] and white_val != []:
            return [False, white_attack]

        #if exists Value[attacker] < Value[piece] --> not protected
        for p in white_val:
            if p < pieceValue[board[pos[0]][pos[1]]%20]:
                return [False, white_attack]

        #make lists that we can manipulate
        black_take = list(black_val)
        white_take = list(white_val)

        #first we order the lists to be in the order that they would take in
        black_take.sort()
        black_take = [pieceValue[board[pos[0]][pos[1]]%10]] + black_take
        #black_take = white_take[:len(white_take)-1] #since the last piece cannot be taken
        white_take.sort()

        #okay so here's the premise, black can stop taking whenever he wants
        #so if there ever exists a time where black can stop taking and be up material
        #then the piece is not protected
        black_lost = []
        white_lost = []
        while True:
            if white_take != []:
                black_lost += [black_take[0]]
                black_take = black_take[1:]
            else:
                #black can't take any more peices
                #if white lost more material than black, the piece was not protected
                if sum(black_lost) > sum(white_lost):
                    return [False, white_attack]
                else:
                    return [True, white_attack]
            if black_take != []:
                white_lost += [white_take[0]]
                white_take = white_take[1:]
            else:
                if sum(black_lost) > sum(white_lost):
                    return [False, white_attack]
                else:
                    return [True, white_attack]
        return [True, white_attack]
    
    #if position does not contain any pieces, return Nothing
    return [None, []]

def isEverthingProtected(board,player):
    out = []
    for i in range(0,8):
        for j in range(0,8):
            if board[i][j]/10 == player/10:
                protected = isProtected(board,[i,j])
                if not protected[0]:
                    out += [[i,j]]
    if out == []:
        return [True, []]
    else:
        return [False, out]

def isSquareSafe(board,pos,new_pos,player):
    temp_board = copyBoard(board)
    temp_board[new_pos[0]][new_pos[1]] = temp_board[pos[0]][pos[1]]
    temp_board[pos[0]][pos[1]] = 0
    return  isProtected(temp_board, new_pos)[0]
