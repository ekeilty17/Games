def getRow(L,i):
    if i < 0 or i > 8:
        raise TypeError("Index out of range")
    out = L[i]
    #return out
    return [x for x in out if x != 0]

def getCol(L,j):
    if j < 0 or j > 8:
        raise TypeError("Index out of range")
    out = []
    for row in L:
        out += [row[j]]
    #return out
    return [x for x in out if x != 0]

def getSquare(L,s):
    # 0 1 2
    # 3 4 5
    # 6 7 8
    if s < 0 or s > 8:
        raise TypeError("Index out of range")
    #unfortunately, I think this is the best way to do it
    out = []
    if s == 0:
        out = [ L[0][0], L[0][1], L[0][2],
                L[1][0], L[1][1], L[1][2],
                L[2][0], L[2][1], L[2][2] ]
    elif s == 1:
        out = [ L[0][3], L[0][4], L[0][5],
                L[1][3], L[1][4], L[1][5],
                L[2][3], L[2][4], L[2][5] ]
    elif s == 2:
        out = [ L[0][6], L[0][7], L[0][8],
                L[1][6], L[1][7], L[1][8],
                L[2][6], L[2][7], L[2][8] ]
    elif s == 3:
        out = [ L[3][0], L[3][1], L[3][2],
                L[4][0], L[4][1], L[4][2],
                L[5][0], L[5][1], L[5][2] ]
    elif s == 4:
        out = [ L[3][3], L[3][4], L[3][5],
                L[4][3], L[4][4], L[4][5],
                L[5][3], L[5][4], L[5][5] ]
    elif s == 5:
        out = [ L[3][6], L[3][7], L[3][8],
                L[4][6], L[4][7], L[4][8],
                L[5][6], L[5][7], L[5][8] ]
    elif s == 6:
        out = [ L[6][0], L[6][1], L[6][2],
                L[7][0], L[7][1], L[7][2],
                L[8][0], L[8][1], L[8][2] ]
    elif s == 7:
        out = [ L[6][3], L[6][4], L[6][5],
                L[7][3], L[7][4], L[7][5],
                L[8][3], L[8][4], L[8][5] ]
    elif s == 8:
        out = [ L[6][6], L[6][7], L[6][8],
                L[7][6], L[7][7], L[7][8],
                L[8][6], L[8][7], L[8][8] ]
    #return out
    return [x for x in out if x != 0]


def isValidSudokuBoard(L):
    #This function assumes it's a 9x9 array of integers ... not gonne do those checks again
    for i in range(9):
        row = getRow(L,i)
        col = getCol(L,i)
        square = getSquare(L,i)
        #Basically just need to check if any repeats exist
        if list(sorted(row)) != list(sorted(set(row))) or list(sorted(col)) != list(sorted(set(col))) or list(sorted(square)) != list(sorted(set(square))):
            #print row,list(set(row))
            #print col,list(set(col))
            #print square,list(set(square))
            return False
    return True

class board():

    def __init__(self, L):

        """Make sure L is a 9x9 array or integers"""
        if type(L) != list:
            raise TypeError("Input is not a list")
        if len(L) != 9:
            raise TypeError("Number of rows in input does not equal 9")

        for i in range(9):
            if len(L[i]) != 9:
                raise TypeError("Number of columns in input does not equal 9")
            for j in range(9):
                if L[i][j] not in range(0,10):
                    #The zero indicates an empty cell
                    raise TypeError("Input list does not contain integers between 0 and 9 (inclusive)")

        if not isValidSudokuBoard(L):
            raise TypeError("Not a valid Sudoku board")
        self.store = L

    def copy(self):
        out = []
        for row in self.store:
            out += [list(row)]
        return out

    def new(self):
        return board(self.copy())

    def Display(self):
        out =  "\t \033[90m   1 2 3   4 5 6   7 8 9\033[0m\n"
        out += "\t \033[90m  -----------------------\033[0m\n"
        for i in range(9):
            temp = '\t\033[90m' + str(i+1) + ' |\033[0m '
            for j in range(9):
                if self.store[i][j] == 0:
                    temp += '  '
                else:
                    temp += str(self.store[i][j]) + ' '
                if j == 2 or j == 5:
                    temp += '\033[90m|\033[0m '
                elif j == 8:
                    temp += '\033[90m|\033[0m\n'
            out += temp
            if i == 2 or i == 5:
                out += "\t\033[90m  |-------+-------+-------|\033[0m\n"
            if i == 8:
                out += "\t\033[90m   -----------------------\033[0m"
        print out
        return out

    def isComplete(self):
        for i in range(9):
            for j in range(9):
                if self.store[i][j] == 0:
                    return False
        return True

    # Need this to match the general search tree syntax
    def move_search(self, L):
        self.move(L[0], L[1])

    def move(self, num, pos):
        self.store[pos[0]][pos[1]] = num
