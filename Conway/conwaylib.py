from random import randint

# Rules
#   if cell is alive:
#       if number of alive neighbors equals 2 or 3, cell stays alive
#       if number of alive neighbors less than 2, dies from lack of resources
#       if number of alive neighbors greater than 3, dies from over-population
#
#   if call is dead:
#       if number of equals 3, then cell becomes alive
#       otherwise cell stays dead

def rule(p, neighbors):
    friends = 0
    for i in neighbors:
        friends += i
    
    if p == 1:
        if friends == 2 or friends == 3:
            return 1
        else:
            return 0
    else:
        if friends == 3:
            return 1
        else:
            return 0

class conway:
    
    # Possible States
    #   0:  empty   black
    #   1:  alive   white

    def __init__(self, rows, cols, init_random=False):
        self.rows = rows
        self.cols = cols
        self.board = []
        
        if init_random:
            for i in range(0,self.rows):
                temp = []
                for j in range(0,self.cols):
                    temp += [randint(0,1)]
                self.board += [temp]
        else:
            for i in range(0,self.rows):
                temp = []
                for j in range(0,self.cols):
                    temp += [0]
                self.board += [temp]
    
    def setBoard(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])

    def Display(self):
        out = ""
        for r in self.board:
            for e in r:
                if (e == 0):
                    out += "   "
                elif (e == 1):
                    out += " * "
                else:
                    raise TypeError("Invalid board.")
            out += "\n"
        print out
        return out
    
    """
    def printDisp2(self):
        board = "  "
        for i in range(0,len(self.store[0])):
            board += str(i)
        board += "\n"
        counter = 0
        for e in self.store:
            board += str(counter) + " "
            for i in range(0,len(e)):
                if (e[i] == 0):
                    board += "0"
                elif (e[i] == 1):
                    board += "1"
                else:
                    return False
            board += "\n"
            counter += 1
        print board
    """

    def setPos(self,row,col,val):
        if (val != 0) and (val != 1):
            return False
        if (row >= self.rows) or (col >= self.cols):
            return False
        self.board[row][col] = val
        return True

    # Helper function: gets all neighbors
    # The board is like a Pacman board, the edges wrap to the other side
    def getNeighbors(self,row,col):
        
        # check if out of range
        if( (row > (self.rows-1)) or (col > (self.cols-1)) or
             (row < 0) or (col < 0) ):
            return False
        
        neighbors = []
        neighbor_coord = [  [row-1,col-1], [row-1,col], [row-1,col+1], 
                            [row,  col-1],              [row,  col+1], 
                            [row+1,col-1], [row+1,col], [row+1,col+1] 
                        ]
        for p in neighbor_coord:
            neighbors += [ self.board[ p[0]%self.rows ][ p[1]%self.cols ] ]
        
        return neighbors

    def evolve(self, rule):
        next_state = []
        for i in range(0,self.rows):
            temp = []
            for j in range(0,self.cols):
                temp += [rule(self.board[i][j], self.getNeighbors(i,j))]
            next_state += [temp]
        self.board = next_state
