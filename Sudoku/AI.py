from board import *
from puzzles import *
from general_search_tree import *



""" Beginner AI """

def pos2sqaure(pos):
    if pos in [[0,0], [0,1], [0,2],
               [1,0], [1,1], [1,2],
               [2,0], [2,1], [2,2]]:
        return 0
    elif pos in [[0,3], [0,4], [0,5],
                 [1,3], [1,4], [1,5],
                 [2,3], [2,4], [2,5]]:
        return 1
    elif pos in [[0,6], [0,7], [0,8],
                 [1,6], [1,7], [1,8],
                 [2,6], [2,7], [2,8]]:
        return 2
    elif pos in [[3,0], [3,1], [3,2],
                 [4,0], [4,1], [4,2],
                 [5,0], [5,1], [5,2]]:
        return 3
    elif pos in [[3,3], [3,4], [3,5],
                 [4,3], [4,4], [4,5],
                 [5,3], [5,4], [5,5]]:
        return 4
    elif pos in [[3,6], [3,7], [3,8],
                 [4,6], [4,7], [4,8],
                 [5,6], [5,7], [5,8]]:
        return 5
    elif pos in [[6,0], [6,1], [6,2],
                 [7,0], [7,1], [7,2],
                 [8,0], [8,1], [8,2]]:
        return 6
    elif pos in [[6,3], [6,4], [6,5],
                 [7,3], [7,4], [7,5],
                 [8,3], [8,4], [8,5]]:
        return 7
    elif pos in [[6,6], [6,7], [6,8],
                 [7,6], [7,7], [7,8],
                 [8,6], [8,7], [8,8]]:
        return 8

def isPossible(L, num, pos):
    if L[pos[0]][pos[1]] != 0:
        return False
    if num in getRow(L, pos[0]):
        return False
    if num in getCol(L, pos[1]):
        return False
    if num in getSquare(L, pos2sqaure(pos)):
        return False
    return True

# When a number can only be put in a sinlge cell bc instances of that same number
# appear in the rows or cols surrounding it
def Unique_Candidate(B):
    for n in range(1,10):
        #A list of all possible places the number n could go
        possible = [[isPossible(B.store,n,[i,j]) for j in range(9)] for i in range(9)]

        # For any cell st possible[i][j] == True
        # If it is the only such cell in it's row, col, or square, then it has to go there
        for i in range(9):
            for j in range(9):
                if possible[i][j] == True:
                    # The way I wrote the below functions, it gets rid of all False when returning the list
                    if getRow(possible,i) == [True]:
                        B.move(n,[i,j])
                    elif getCol(possible,j) == [True]:
                        B.move(n,[i,j])
                    elif getSquare(possible,pos2sqaure([i,j])) == [True]:
                        B.move(n,[i,j])

# Can solve puzzles I label as "Easy"
# Only implements the method of unique candidates
def beginner_AI(game_board):
    B = board(game_board)
    B.Display()
    print
    last = []

    while (not B.isComplete()) and last != B.store:
        last = B.copy()

        # Unique Candidate Method
        Unique_Candidate(B)
        B.Display()
        print
        if B.isComplete():
            break
    return B.store



""" Intermediate AI """

def getCandidates(L, pos):
    if L[pos[0]][pos[1]] != 0:
        return []

    out = []
    out += getRow(L,pos[0])
    out += getCol(L,pos[1])
    out += getSquare(L,pos2sqaure(pos))
    return list(sorted(list(set([1,2,3,4,5,6,7,8,9]) - set(out))))

# When a number can only be put in a single cell bc instances of all other numbers
# appear in the rows, cols, and squares that are shared with that number
def Soul_Candidate(B, pos):
    C = getCandidates(B.store, pos)
    if len(C) == 1:
        B.move(list(C)[0],pos)
        return True
    return False

# Can solve puzzles I label as "Medium
# implements the methods unique candidates and soul candidates
def intermediate_AI(game_board):
    B = board(game_board)
    B.Display()
    print
    last = []

    while (not B.isComplete()) and last != B.store:
        last = B.copy()

        # Soul Candiate Method
        for i in range(9):
            for j in range(9):
                if Soul_Candidate(B,[i,j]):
                    B.Display()
                    print
        if B.isComplete():
            break

        # Unique Candidate Method
        Unique_Candidate(B)
        B.Display()
        print
        if B.isComplete():
            break
    return B.store



""" Expert AI """

def isContradiction(B):
    for i in range(8):
        for j in range(8):
            if B.store[i][j] == 0 and getCandidates(B.store, [i,j]) == []:
                return True
    return False

class Sudoku_search_tree(general_search_tree):

    def __init__(self, val):
        general_search_tree.__init__(self, val)

        # You can run it without this line, which means it's a pure search tree with no logical deductions
        # It takes about a minute, but it will find the solution
        # Basically, if you want the AI to find the solution faster, you need to improve this line
        self.val.store = intermediate_AI(self.val.store)

    def isSolution(self):
        return self.val.isComplete()

    def prune(self):
        # There might be more cases that I could prune, which would make the AI faster
        if isContradiction(self.val):
            return True
        if not isValidSudokuBoard(self.val.store):
            return True
        return False

    def getEdges(self):
        return [[getCandidates(self.val.store, [i,j]), [i, j]] for i in range(9) for j in range(9) if self.val.store[i][j] == 0]

    def heuristic(self, L):
        # needed to make a special function for the sorting
        def length(C):
            return len(C[0])
        # getting a list of candidate moves from all empty cells
        # unfortunately I have to do something ugly to keep track of the indeces
        #   all_candidate = [ [...candidate moves...], i, j], ... ]
        # Then sorting the list based on the number of candidate moves
        L_sorted = sorted(L, key=length)

        # I only need the first set of candiadte moves bc we know that one of them has to be a correct answer
        first = L_sorted[0]

        # Now I need to make L_sorted match the format the general_search_tree is expecting
        # out = [ [num, [i,j]], ...]
        return [[first[0][i], first[1]] for i in range(len(first[0]))]

    def copy_node(self):
        return Sudoku_search_tree( self.val.new() )

    def evolve(self, E):
        self.val.move_search(E)
        return self

    def Display(self):
        return self.val.Display()

# Should be able to solve any sudoku puzzle
def expert_AI(game_board):
    B = board(game_board)
    B.Display()

    leaf = Sudoku_search_tree(B).search()
    if leaf == False:
        print "Could not find solution"
    else:
        leaf.Display()

    return leaf.val.store
