from random import randint

def rule(val, neighbors):
    if val == 0:
        return 0
    elif val == 1:
        return 2
    elif val == 2:
        return 3
    elif val == 3:
        e_heads = 0
        for n in neighbors:
            if n == 1:
                e_heads += 1
        if e_heads == 1 or e_heads == 2:
            return 1
        else:
            return 3
    else:
        raise TypeError("This shouldn't be happening")

class wireworld:

    # Possible States:
    #   0:  empty           black
    #   1:  electron head   blue
    #   2:  electron tail   red
    #   3:  conductor       yellow
    
    def __init__(self, rows, cols, board=[]):
        self.rows = rows
        self.cols = cols
        self.board = board

        if board == []:
            for i in range(0,self.rows):
                temp = []
                for j in range(0,self.cols):
                    temp += [0]
                self.board += [temp]
        else:
           self.rows = len(self.board)
           self.cols = len(self.board[0])
    
    def setBoard(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
    
    def Display(self):
        board = ""
        for p in self.board:
            for i in range(0,len(p)):
                if p[i] == 0:
                    board += "\033[0m   \033[0m"
                elif p[i] == 1:
                    board += "\033[43m\033[34m * \033[0m"
                elif p[i] == 2:
                    board += "\033[43m\033[31m * \033[0m"
                elif p[i] == 3:
                    board += "\033[43m   \033[0m"
                else:
                    raise TypeError("Value in variable self.board that should not be there")
            board += "\n"
        print board
        return board
    
    def setPos(self, row, col, val):
        if (val != 0) and (val != 1):
            return False
        if (row >= self.rows) or (col >= self.cols):
            return False
        self.board[row][col] = val
        return True
    
    def getNeighbors(self, row, col):
        # Check if out of range
        if( (row > (self.rows-1)) or (col > (self.cols-1)) or (row < 0) or (col < 0) ):
            return []
        neighbors = []
        neighbor_coord = [  [row-1,col-1], [row-1,col], [row-1,col+1],
                            [row,  col-1],              [row,  col+1],
                            [row+1,col-1], [row+1,col], [row+1,col+1]
                         ]
        for p in neighbor_coord:
            if not ( (p[0] > (self.rows-1)) or (p[1] > (self.cols-1)) or (p[0] < 0) or (p[1] < 0) ):
                neighbors += [ self.board[p[0]][p[1]] ]
        
        return neighbors
    
    def evolve(self, rule):
        next_state = []
        for i in range(0,self.rows):
            temp = []
            for j in range(0,self.cols):
                temp += [rule(self.board[i][j], self.getNeighbors(i,j))]
            next_state += [temp]
        self.board = next_state
