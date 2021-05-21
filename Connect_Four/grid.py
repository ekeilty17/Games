import numpy as np

class ConnectFourGrid(object):

    p1_color = '\033[91m'       # red
    p2_color = '\033[93m'       # yellow
    outline_color = '\033[90m'  # grey

    def __init__(self, size=(6, 7)):
        self.h, self.w = size
        self.board = np.zeros(size, dtype=int)
    
    def __repr__(self):
        out = self.outline_color
        out += '\n' + ' ' * 4
        out += "+   " * (self.w) + '+'
        out += '\n'
        for r in reversed(range(self.h)):       # reversed so row 0 prints to the bottom
            row = ' ' * 4
            for c in range(self.w):
                if self.board[r][c] == 1:
                    row += '|' + self.p1_color + ' o ' + self.outline_color
                elif self.board[r][c] == 2:
                    row += '|' + self.p2_color + ' o ' + self.outline_color
                else:
                    row += '|   '
            row += '|\n' + ' ' * 4
            row += "+ - " * (self.w) + '+'
            out += row + '\n'
        
        out += "\033[0m"        # resets terminal colors
        out += ' ' * 4
        out += '  ' + "   ".join([str(i+1) for i in range(self.w)])
        out += '\n'
        return out

    def copy(self):
        C = ConnectFourGrid(size=(self.h, self.w))
        C.board = self.board.copy()
        return C
    
    def move(self, player, c):

        if player not in [1, 2]:
            raise ValueError(f"Value of player must be either 1 or 2, got value {player}")

        # find first non-zero value in the indicated col
        idx = np.argmin(self.board, axis=0)[c-1]

        if self.board[idx, c-1] != 0:
            raise ValueError("This column is full")
        
        # making move
        self.board[idx, c-1] = player

    def check_win(self):
        
        # checking columns (connect 4 vertically)
        for r in range(self.h):
            for c in range(self.w-3):
                if self.board[r, c] == 0:
                    continue
                if self.board[r, c] == self.board[r, c+1] == self.board[r, c+2] == self.board[r, c+3]:
                    return self.board[r, c]
        
        # checking for rows (connect 4 horizontally)
        for c in range(self.w):
            for r in range(self.h-3):
                if self.board[r, c] == 0:
                    continue
                if self.board[r, c] == self.board[r+1, c] == self.board[r+2, c] == self.board[r+3, c]:
                    return self.board[r, c]

        # checking diagonals
        for k in range(0, self.w-3):
            diagonal = np.diag(self.board, k=k)
            for i in range(len(diagonal)-3):
                if diagonal[i] == 0:
                    continue
                if diagonal[i] == diagonal[i+1] == diagonal[i+2] == diagonal[i+3]:
                    return diagonal[i]
        
        for k in range(1, self.h-3):
            diagonal = np.diag(self.board, k=-k)
            for i in range(len(diagonal)-3):
                if diagonal[i] == 0:
                    continue
                if diagonal[i] == diagonal[i+1] == diagonal[i+2] == diagonal[i+3]:
                    return diagonal[i]

        # checking skew-diagonals
        for k in range(0, self.w-3):
            skew_diagonal = np.diag(np.flip(self.board, axis=1), k=k)
            for i in range(len(skew_diagonal)-3):
                if skew_diagonal[i] == 0:
                    continue
                if skew_diagonal[i] == skew_diagonal[i+1] == skew_diagonal[i+2] == skew_diagonal[i+3]:
                    return skew_diagonal[i]
        for k in range(1, self.h-3):
            skew_diagonal = np.diag(np.flip(self.board, axis=1), k=-k)
            for i in range(len(skew_diagonal)-3):
                if skew_diagonal[i] == 0:
                    continue
                if skew_diagonal[i] == skew_diagonal[i+1] == skew_diagonal[i+2] == skew_diagonal[i+3]:
                    return skew_diagonal[i]
        
        # if we didn't find anything
        return 0

    def is_full(self):
        return np.all(self.board)

if __name__ == "__main__":

    C = ConnectFourGrid()
    print(C)

    C.move(1, 4)
    C.move(1, 4)
    C.move(2, 4)
    C.move(1, 4)
    C.move(2, 4)
    C.move(2, 4)

    C.move(1, 5)
    C.move(1, 3)
    C.move(2, 5)
    C.move(2, 3)

    C.move(1, 5)
    C.move(1, 3)

    C.move(2, 6)
    C.move(1, 6)
    
    #C.move(1, 2)
    #C.move(2, 3)
    print(C)

    print(C.check_win())