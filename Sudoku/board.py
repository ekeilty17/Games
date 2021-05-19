import numpy as np

class SudokuBoard(object):

    def __init__(self, board, check_consistent=True):
        
        # some error checking
        self.board_correct_structure(board)
        self.board = np.array(board)    # will be a 9x9 numpy array

        if check_consistent:
            if not self.is_consistent():
                raise ValueError("This board contains inconsistencies")


    @staticmethod
    def board_correct_structure(board):
        if not type(board) in [list, np.ndarray]:
            raise TypeError("Input is not a list")
        
        if len(board) != 9:
            raise TypeError("Number of rows in input does not equal 9")

        for i in range(9):
            if len(board[i]) != 9:
                raise TypeError("Number of columns in input does not equal 9")
            for j in range(9):
                if board[i][j] not in range(10):
                    raise ValueError("Input list does not contain integers between 0 and 9 (inclusive)")

    #def __getitem__(self, index):
    #    return self.board[index]

    def __repr__(self):
        out = "\t \033[90m  -----------------------\033[0m\n"
        for i in range(9):
            temp = '\t\033[90m' + str(i+1) + ' |\033[0m '
            for j in range(9):
                if self.board[i][j] == 0:
                    temp += '  '
                else:
                    temp += str(self.board[i][j]) + ' '
                if j == 2 or j == 5:
                    temp += '\033[90m|\033[0m '
                elif j == 8:
                    temp += '\033[90m|\033[0m\n'
            out += temp
            if i == 2 or i == 5:
                out += "\t\033[90m  |-------+-------+-------|\033[0m\n"
            if i == 8:
                out += "\t\033[90m   -----------------------\033[0m\n"
        out +=  "\t \033[90m   1 2 3   4 5 6   7 8 9\033[0m\n"
        return out

    def copy(self):
        return SudokuBoard( self.board.copy(), check_consistent=False )

    def check_bounds(i):
        return i in range(1, 10)
    


    """ basic functionality to use the Sudoku Board """

    def move(self, r, c, val):
        self.board[r-1, c-1] = val

    # Due to Sudoku convensions, when calling these functions 
    # we will index from 1 to 9 instead of 0 to 8
    def get_cell(self, r, c):
        return self.board[r-1, c-1]

    def get_row(self, r, include_self=True):
        return self.board[r-1, :]

    def get_col(self, c, include_self=True):
        return self.board[:, c-1]

    # because these will mostly be used for iterating I thought this would be simpler to label
    # the cells in each 3x3 square as follows
    #       1   2   3
    #       4   5   6
    #       7   8   9
    
    @staticmethod
    def coord2flat(r, c):
        x = (r-1) // 3
        y = (c-1) // 3
        s = 3*x + y
        return s+1
    
    @staticmethod
    def flat2coord(s):
        x = (s-1) // 3
        y = (s-1) % 3
        r = 2 + 3*x
        c = 2 + 3*y
        return r, c
    
    # again we index from 1 to 9
    def get_neighbor_indices(self, r, c, include_self=True):
        neighbor_idx = [
            (r-1, c-1), (r-1, c), (r-1, c+1),
            (r,   c-1), (r, c),   (r, c+1),
            (r+1, c-1), (r+1, c), (r+1, c+1)
        ]
        neighbor_idx = filter(lambda t: t[0] in range(1, 10) and t[1] in range(1, 10), neighbor_idx)
        if not include_self:
            neighbor_idx = filter(lambda t: t != (r, c), neighbor_idx)
        return list(neighbor_idx)

    def get_neighbor_values(self, r, c, include_self=True):
        neighbor_idx = self.get_neighbor_indices(r, c, include_self=include_self)
        return [self.get_cell(r, c) for r, c in neighbor_idx]

    # I've created this intermediate function because it will provide useful functionality later
    def get_square_indexes(self, *args, include_self=True):
        
        if len(args) == 1:
            s = args[0]
        elif len(args) == 2:
            r, c = args
            s = self.coord2flat(r, c)
        else:
            raise ValueError(f"Too many arguments. Expected 1 or 2, got {len(args)}")
        
        
        r_center, c_center = self.flat2coord(s)
        square_idx = self.get_neighbor_indices(r_center, c_center)
        if not include_self:
            square_idx = filter(lambda t: t != (r, c), square_idx)

        return square_idx
    
    # there are 2 ways to identify a square, either using index s or using the coordinate (r, c)
    # I've included both functionaity to make things easier
    def get_square(self, *args):

        if len(args) == 1:
            s = args[0]
        elif len(args) == 2:
            r, c = args
            s = self.coord2flat(r, c)
        else:
            raise ValueError(f"Too many arguments. Expected 1 or 2, got {len(args)}")

        r_center, c_center = self.flat2coord(s)
        square_idx = self.get_neighbor_indices(r_center, c_center, include_self=True)
        return [self.get_cell(r, c) for r, c in square_idx]


    # returns values from top left to bottom right
    def get_diagonal(self, k=0):
        return np.diag(self.board, k)
    
    # returns values from bottom left to top right
    def get_skew_diagonal(self, k=0):
        return np.flip(np.diag(np.flip(self.board, axis=1), k))


    """ Verfication of solution """

    def is_complete(self):
        return not np.any(self.board == 0)
    
    @staticmethod
    def has_repeats(L):
        return list(sorted(L)) != list(sorted(set(L)))

    # This might not be super efficient, but it's only a 9x9 board
    def is_consistent(self, diagonals=False):
        # check if any row, col, or square has a repeated value
        for i in range(1, 10):
            row = list(filter(lambda x: x != 0, self.get_row(i)))
            col = list(filter(lambda x: x != 0, self.get_col(i)))
            square = list(filter(lambda x: x != 0, self.get_square(i)))
            if self.has_repeats(row) or self.has_repeats(col) or self.has_repeats(square):
                return False
        
        # sometimes sudokus also do the diagonals, so check if those have any repeats
        if diagonals:
            diagonal = list(filter(lambda x: x != 0, self.get_diagonal()))
            skew_diagonal = list(filter(lambda x: x != 0, self.get_skew_diagonal()))
            if self.has_repeats(diagonal) or self.has_repeats(skew_diagonal):
                return False
        
        # if all checks successed return true
        return True

    def is_solution(self):
        return self.is_complete() and self.is_consistent()