    def getRow(self, pos):
        return self.board[pos[0]]

    def getCol(self, pos):
        out = []
        for row in self.board:
            out += row[pos[1]]
        return out

    # top left to bottom right
    def getDiagonal(self, pos):
        out = [self.board[pos[0]][pos[1]]]

        #Going up the diagonal
        r = pos[0]+1
        c = pos[1]+1
        while r < 8 and c < 8:
            out += [self.board[r][c]]
            r += 1
            c += 1

        #going down the diagonal
        r = pos[0]-1
        c = pos[1]-1
        while r >= 0 and c >= 0:
            out = [self.board[r][c]] + out
            r -= 1
    # top right to bottom left
    def getSkewDiagonal(self, pos):
        out = [self.board[pos[0]][pos[1]]]

        #Going up the diagonal
        r = pos[0]-1
        c = pos[1]+1
        while r >= 0 and c < 8:
            out += [self.board[r][c]]
            r -= 1
            c += 1

        #going down the diagonal
        r = pos[0]+1
        c = pos[1]-1
        while r < 8 and c >= 0:
            out = [self.board[r][c]] + out
            r += 1
            c -= 1


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
                            pos = [i,j]
                            #avoid repetition
                            if pos in legal:
                                break
                            pos = step(pos)
                            # Doesn't count in that direction if we are right next to our own player
                            if self.inRange(pos):
                                if self.board[pos[0]][pos[1]] == player:
                                    break
                            while self.board[pos[0]][pos[1]] != 0 and self.inRange(pos):
                                pos = step(pos) 
                                if self.board[pos[0]][pos[1]] == player:
                                    legal += [[i,j]]
                                    break
        return legal
