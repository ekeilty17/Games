from random import randint

terminal_colors = {
                    0: '\033[91m',      #red
                    1: '\033[93m',      #yellow (no orange in terminal :/ )
                    2: '\033[92m',      #green
                    3: '\033[96m',      #cyan
                    4: '\033[94m',      #dark blue/ indigo
                    5: '\033[95m',      #pink/ magenta
                    6: '\033[37m',      #light grey
                    7: '\033[90m',      #dark grey
                    8: '\033[30m',      #black
                    9: '\033[33m'       #dark yellow (I ran out of terminal colors...best I could do)
                }

class board():

    def __init__(self,rows,cols,colors):
        if rows < 1 or int(rows) != rows:
            raise TypeError("the number of rows must be a positive integer greater than 0")
        if cols < 1 or int(cols) != cols:
            raise TypeError("the number of columns must be a positive integer greater than 0")
        if colors < 1 or int(colors) != colors:
            raise TypeError("the number of colors must be a positive integer greater than 0")

        self.rows = rows
        self.cols = cols
        self.colors = colors
        self.store = [[randint(0,self.colors-1) for y in range(self.cols)] for x in range(self.rows)]
        self.expected = int( 2*min(self.rows,self.cols) + (2*self.colors)**0.5 + self.colors ) + 1    

    
    def Display(self):
        out = ""
        for i in range(self.rows):
            temp = ""
            for j in range(self.cols):
                temp += terminal_colors[self.store[i][j]%10]
                temp += str(self.store[i][j])
                temp += '\033[0m  '
            out += temp + '\n'
        print out
        return out
    
    def isComplete(self):
        first = self.store[0][0]
        for i in range(self.rows):
            for j in range(self.cols):
                if first != self.store[i][j]:
                    return False
        return True
    
    #Everything below is the logic to make a move in the game
    def isInRange(self, pos):
        if pos[0] < 0 or pos[1] < 0:
            return False
        if pos[0] >= self.rows or pos[1] >= self.cols:
            return False
        return True

    def get_neighbors(self, i, j):
        possible = [             [i-1, j],
                     [i,   j-1],           [i,   j+1],
                                 [i+1, j]
                   ]
        return [pos for pos in possible if self.isInRange(pos)]
        

    def move_rec(self, i, j, prev_color, new_color):
        neighbors = self.get_neighbors(i, j)
        for pos in neighbors:
            #We only care about neighbors that are the previous color. 
            #If they are, then we change it to the new color
            #       and call the function recursively on its neighbors.
            #The recurrsion will stop either when it hits a boundary and there are no more neihbors
            #       or when no neighbors are the previous color.
            if self.store[pos[0]][pos[1]] == prev_color:
                self.store[pos[0]][pos[1]] = new_color
                self.move_rec(pos[0],pos[1], prev_color, new_color)
        
    def move(self, new_color):
        if new_color >= self.colors:
            return None
        prev_color = self.store[0][0]
        if new_color == prev_color:
            return None
        self.store[0][0] = new_color
        return self.move_rec(0, 0, prev_color, new_color)
