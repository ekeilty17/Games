class TicTacToe:
    #board is a 1 dim array, not a 2 dim array
    #easier for users that way
    board = []
    row = 0
    col = 0

    def __init__(self):
        self.board = []
        self.row = 3
        self.col = 3
        for i in range(0,3):
            temp = []
            for j in range(0,3):
                temp += [0]
            self.board += temp

    def Display(self):
        out = ""
        for i in range(0,len(self.board)):
            player = " "
            if self.board[i] == 0:
                player = "\x1b[31m" + str(i) + "\x1b[0m"
            if self.board[i] == 1:
                player ="X"
            if self.board[i] == 2:
                player = "O"

            out += " " + player
            if (i+1) % self.col == 0:
                out += " \n"
                if i != len(self.board)-1:
                    out += "---|---|---\n"
            else:
                out += " |"
        print out
        return out

    def Move(self,Pos,player):
        if Pos < 0:
            return False
        if Pos >= len(self.board):
            return False
        if player != 1 and player != 2:
            return False
        if self.board[Pos] != 0:
            return False
        self.board[Pos] = player
        return True

    def AnalyzeBoard(self):
        #return list
        #   -1: Error
        #   0: incomplete game
        #   1: X wins
        #   2: O wins
        #   3: draw

        T = self.board
        for i in T:
            if (type(i) != int or i < 0 or i > 2):
                return -1

        for i in range(0,3):
            #rows
            if (T[0+i*3] == T[1+i*3] == T[2+i*3] == 1):
                return 1
            if (T[0+i*3] == T[1+i*3] == T[2+i*3] == 2):
                return 2
            #collumns
            if (T[0+i] == T[3+i] == T[6+i] == 1):
                return 1
            if (T[0+i] == T[3+i] == T[6+i] == 2):
                return 2
        #diagonals
        if (T[0] == T[4] == T[8] == 1):
            return 1
        if (T[0] == T[4] == T[8] == 2):
            return 2
        if (T[2] == T[4] == T[6] == 1):
            return 1
        if (T[2] == T[4] == T[6] == 2):
            return 2

        for i in T:
            if i == 0:
                return 0

        return 3
