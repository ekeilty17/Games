
#The set of rules I'm using is also known as Othello
class reversi:

    def __init__(self):
        self.blank_board = [ ['_', '#', '_', '#', '_', '#', '_', '#'],
                             ['#', '_', '#', '_', '#', '_', '#', '_'],
                             ['_', '#', '_', '#', '_', '#', '_', '#'],
                             ['#', '_', '#', '_', '#', '_', '#', '_'],
                             ['_', '#', '_', '#', '_', '#', '_', '#'],
                             ['#', '_', '#', '_', '#', '_', '#', '_'],
                             ['_', '#', '_', '#', '_', '#', '_', '#'],
                             ['#', '_', '#', '_', '#', '_', '#', '_']
                           ]
        
        self.board = [  [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 2, 1, 0, 0, 0],
                        [0, 0, 0, 1, 2, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0]
                     ]
    
    
    def Display(self):
        out = "\x1b[90m" + "   a  b  c  d  e  f  g  h" + "\x1b[0m" + "\n"
        for i in range(8):
            s_temp =  "\x1b[90m" + str(i+1) + " " + "\x1b[0m"
            for j in range(8):
                if self.board[i][j] == 0:
                    if self.blank_board[i][j] == '_':
                        s_temp += " \x1b[30m" + self.blank_board[i][j] + "\x1b[0m "
                    else:
                        s_temp += " \x1b[90m" + self.blank_board[i][j] + "\x1b[0m "
                elif self.board[i][j] == 1:
                    s_temp += " \x1b[34m" + 'O' + "\x1b[0m "
                elif self.board[i][j] == 2:
                    s_temp += " \x1b[97m" + 'O' + "\x1b[0m "
            out += s_temp
            if i != 7:
                out += "\n"
        print out
        return out
    
    # The following functions are helper functions for the isOutflankedDirection() function 
    def inRange(self, pos):
        r = pos[0]
        c = pos[1]
        if r < 0 or r > 7:
            return False
        if c < 0 or c > 7:
            return False
        return True
    
    def getNeighbors(self, pos):
        r = pos[0]
        c = pos[1]

        out = [ [r-1,c-1], [r-1,c], [r-1,c+1],
                 [r,  c-1],          [r,  c+1],
                 [r+1,c-1], [r+1,c], [r+1,c+1]]
        return [p for p in out if self.inRange(p)]

    def PosRowStep(self, pos):
        return [pos[0]+1, pos[1]]
    def NegRowStep(self, pos):
        return [pos[0]-1, pos[1]]
    
    def PosColStep(self, pos):
        return [pos[0], pos[1]+1]
    def NegColStep(self, pos):
        return [pos[0], pos[1]-1]
    
    def PosDiagStep(self, pos):
        return [pos[0]+1, pos[1]+1]
    def NegDiagStep(self, pos):
        return [pos[0]-1, pos[1]-1]
    
    def PosSkewDiagStep(self, pos):
        return [pos[0]+1, pos[1]-1]
    def NegSkewDiagStep(self, pos):
        return [pos[0]-1, pos[1]+1]
    
    # This function makes writing the rest of the code very easy
    def isOutflankedDirection(self, pos, step, player):
        # getting off the starting square
        pos = step(pos)

        # Doesn't count in that direction if we are right next to our own player
        if self.inRange(pos):
            if self.board[pos[0]][pos[1]] == player:
                return False
        else:
            #return false if out of range
            return False

        # moving up/down the row/col/diag/skew diag
        # If we hit the other players peice, we keep going
        # If we hit our own peice, then we have outflanked our opponent
        # If we hit an empty sqaure or the end of the board then we have not outflanked our opponent
        while self.inRange(pos) and self.board[pos[0]][pos[1]] != 0:
            pos = step(pos)
            if self.board[pos[0]][pos[1]] == player:
                return True
        return False
    
    def LegalMoves(self, player):
        other_player = -1
        if player == 1:
            other_player = 2
        else:
            other_player = 1

        legal = []
        directions = [self.PosRowStep, self.NegRowStep, self.PosColStep, self.NegColStep,
                      self.PosDiagStep, self.NegDiagStep, self.PosSkewDiagStep, self.NegSkewDiagStep]
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 0:
                    if other_player in [self.board[p[0]][p[1]] for p in self.getNeighbors([i,j])]:
                        for step in directions:
                            if self.isOutflankedDirection([i,j], step, player):
                                legal += [[i,j]]
                                break
        return legal
    
    def validMove(self, pos, player):
        if pos in self.LegalMoves(player):
            return True
        return False

    def Move(self, pos, player):
        # Making the move
        self.board[pos[0]][pos[1]] = player
        
        # Getting other player
        other_player = -1
        if player == 1:
            other_player = 2
        else:
            other_player = 1
        
        # Flipping the outflanked discs
        original_pos = list(pos)
        directions = [self.PosRowStep, self.NegRowStep, self.PosColStep, self.NegColStep,
                      self.PosDiagStep, self.NegDiagStep, self.PosSkewDiagStep, self.NegSkewDiagStep]
        for step in directions:
            pos = list(original_pos)
            if self.isOutflankedDirection(pos, step, player):
                pos = step(pos)
                while self.board[pos[0]][pos[1]] == other_player:
                    self.board[pos[0]][pos[1]] = player
                    pos = step(pos)
        
   
    def isComplete(self):
        if self.LegalMoves(1) == [] and self.LegalMoves(2) == []:
            return True
        return False

    def Winner(self):
        black = 0
        white = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 1:
                    black += 1
                    if self.board[i][j] == 2:
                        white += 1
        if black > white:
            return 1
        elif white > black:
            return 2
        else:
            return 0
