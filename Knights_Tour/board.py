class board:
    
    def __init__(self, rows, cols, start):
        
        # Board dimension error checks
        if type(rows) != int or type(cols) != int:
            raise TypeError("Rows and columns of board must be integers.")
        if rows < 1  or cols < 1:
            raise TypeError("Rows and columns of board must be positive integers.")
        if rows > 26 or cols > 26:
            raise TypeError("Bro...a little too big.")
        # Start position error checks
        if type(start) != list:
            raise TypeError("Input is not a list.")
        if len(start) != 2:
            raise TypeError("Input is not a list of length 2.")
        if type(start[0]) != int or type(start[1]) != int:
            raise TypeError("Input list does not contain integers.")
        if (start[0] < 0 or start[0] >= rows) or (start[1] < 0 or start[1] >= cols):
            raise TypeError("Input values are out of range.")

        # board dimensions
        self.rows = rows
        self.cols = cols
        
        # to keep track of knight and display purposes
        self.start = start
        self.curr = start
        self.cnt = 1
        
        # setting up the board
        self.visited = [[0]*self.cols for i in range(self.rows)]
        self.visited[self.start[0]][self.start[1]] = 'K'
        
        # getting the black board
        self.blank_board = []
        for i in range(self.rows):
            temp = []
            for j in range(self.cols):
                if (i+j)%2 == 0:
                    temp += ['_']
                else:
                    temp += ['#']
            self.blank_board += [temp]

    def copy(self):
        out = []
        for r in self.visited:
            out += [list(r)]
        return out
    
    def new(self):
        B_new = board(self.rows, self.cols, self.start)
        B_new.visited = self.copy()
        B_new.curr = self.curr
        B_new.cnt = self.cnt
        return B_new
    
    def Display(self):
        alpha = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                  'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z' ]
        #print " ".join(alpha)
        out = "  ".join(alpha[:self.cols])
        out = "\x1b[90m" + "   " + out + "\x1b[0m" + "\n"
        for i in range(self.rows-1,-1,-1):
            s_temp =  "\x1b[90m" + str(i+1) 
            if i+1 < 10:
                s_temp += " "
            s_temp += "\x1b[0m"
            for j in range(self.cols):
                if self.visited[i][j] == 'K':
                    #Check to make sure this part works...see the end of the tour
                    #if self.visited == [[True]*9]*9:
                    #    s_temp += '\033[43m K \033[30m'
                    #else:
                    s_temp += '\033[93m K \033[0m'
                elif self.visited[i][j] == 0:
                    if self.blank_board[i][j] == '_':
                        s_temp += " \x1b[30m" + self.blank_board[i][j] + " \x1b[0m"
                    else:
                        s_temp += " \x1b[0m" + self.blank_board[i][j] + " \x1b[0m"
                else:
                    if self.visited[i][j] < 10:
                        s_temp += '\033[43m\033[30m ' + str(self.visited[i][j]) + ' \033[0m'
                    elif self.visited[i][j] < 100:
                        s_temp += '\033[43m\033[30m ' + str(self.visited[i][j]) + '\033[0m'
                    else:
                        s_temp += '\033[43m\033[30m' + str(self.visited[i][j]) + '\033[0m'
            out += s_temp
            if i != 0:
                out += "\n"
        print out
        return out
    
    def isComplete(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.visited[i][j] == 0:
                    return False
        return True

    def isClosed(self):
        if (self.start in self.All_Knight_Moves()) and self.isComplete():
            return True
        return False
    
    def Move(self,pos):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.visited[i][j] == 'K':
                    self.visited[i][j] = self.cnt
                    self.cnt += 1
        self.visited[pos[0]][pos[1]] = 'K'
        self.curr = pos
        return self
    
    def outRange(self,i,j):
        if i < 0:
            return True
        if i >= self.rows:
            return True
        if j < 0:
            return True
        if j >= self.cols:
            return True
        return False
    
    def All_Knight_Moves(self):
        r = self.curr[0]
        c = self.curr[1]

        out = [ [r+1,c+2], [r+2,c+1],
                [r+2,c-1], [r+1,c-2],
                [r-1,c-2], [r-2,c-1],
                [r-2,c+1], [r-1,c+2] ]

        # remove moves that are out of range
        return [m for m in out if not self.outRange(m[0],m[1])]

    def Possible_Knight_Moves(self):
        r = self.curr[0]
        c = self.curr[1]
        
        out = [ [r+1,c+2], [r+2,c+1],
                [r+2,c-1], [r+1,c-2],
                [r-1,c-2], [r-2,c-1],
                [r-2,c+1], [r-1,c+2] ]
        
        # remove moves that are out of range
        out = [m for m in out if not self.outRange(m[0],m[1])]
        
        # remove square that were already visited
        return [m for m in out if self.visited[m[0]][m[1]] == 0]

    def Num_Knight_Moves(self,pos):
        r = pos[0]
        c = pos[1]
        
        out = [ [r+1,c+2], [r+2,c+1],
                [r+2,c-1], [r+1,c-2],
                [r-1,c-2], [r-2,c-1],
                [r-2,c+1], [r-1,c+2] ]

        # remove moves that are out of range
        out = [m for m in out if not self.outRange(m[0],m[1])]
        
        # remove square that were already visited
        return len([m for m in out if self.visited[m[0]][m[1]] == 0 or self.visited[m[0]][m[1]] == 'K'])
