import numpy as np
from general_search_tree import GeneralSearchTree


class SudokuLogicManager(object):

    def __init__(self, B):
        self.B = B
        self.candidates = self.set_candidates()
    
    def __repr__(self):
        return self.B.__repr__()

    def copy(self):
        return SudokuLogicManager(self.B.copy())

    """ functionality related to solving the Sudoku """
    def get_possible_cell_values(self, r, c):
        if self.B.get_cell(r, c) != 0:
            return set([self.B.get_cell(r, c)])

        row = self.B.get_row(r)
        col = self.B.get_col(c)
        square = self.B.get_square(r, c)
        not_possible_values = set(np.concatenate((row, col, square)))
        
        return set(range(1, 10)) - not_possible_values

    def get_most_restructed_cells(self):
        flat = [ (x+1, y+1, self.candidates[x][y]) for y in range(9) for x in range(9) if self.B.board[x][y] == 0]
        sorted_flat = list(sorted(flat, key=lambda t: len(t[2])))

        return sorted_flat

    def set_candidates(self):
        return [ [self.get_possible_cell_values(r, c) for c in range(1, 10)] for r in range(1, 10) ]

    def update_candidates(self, r, c, val):
        x, y = r-1, c-1
        self.candidates[x][y] = set([val])

        # remove candidate from rows
        for i in range(1, 10):
            if i == r:
                continue
            self.candidates[i-1][y] = self.candidates[i-1][y] - self.candidates[x][y]

        # remove candidate from cols
        for j in range(1, 10):
            if j == c:
                continue
            self.candidates[x][j-1] = self.candidates[x][j-1] - self.candidates[x][y]

        # remove candidate from square
        for i, j in self.B.get_square_indexes(r, c, include_self=True):
            if i == r and j == c:
                continue
            self.candidates[i-1][j-1] = self.candidates[i-1][j-1] - self.candidates[x][y]
    
    # also sometimes called "Soul Candidate"
    def naked_singles(self):
        '''cell only has 1 candidate''' 
        naked_singles = [(r, c, candidates) for r, c, candidates in self.get_most_restructed_cells() if len(candidates) == 1]
        for r, c, candidates in naked_singles:
            val = candidates.pop()
            self.B.move(r, c, val)
            self.update_candidates(r, c, val)
        
        return naked_singles != []

    def unique_candidate(self):
        '''cell only has 1 candidate within a row, col, or box''' 
        changed = False

        # squares
        for s in range(1, 10):
            
            inverted_index = [set([]) for _ in range(1, 10)]
            for r, c in self.B.get_square_indexes(s, include_self=True):
                for val in self.candidates[r-1][c-1]:
                    inverted_index[val-1].add((r, c))
            
            for val in range(1, 10):
                if len(inverted_index[val-1]) == 1:
                    r, c = inverted_index[val-1].pop()
                    if self.B.get_cell(r, c) != 0:
                        continue
                    self.B.move(r, c, val)
                    self.update_candidates(r, c, val)
                    changed = True
        
        # rows
        for r in range(1, 10):
            inverted_index = [set([]) for _ in range(1, 10)]
            for j in range(1, 10):
                for val in self.candidates[r-1][j-1]:
                    inverted_index[val-1].add((r, j))
            
            for val in range(1, 10):
                if len(inverted_index[val-1]) == 1:
                    r, c = inverted_index[val-1].pop()
                    if self.B.get_cell(r, c) != 0:
                        continue
                    self.B.move(r, c, val)
                    self.update_candidates(r, c, val)
                    changed = True

        # cols
        for c in range(1, 10):
            inverted_index = [set([]) for _ in range(1, 10)]
            for i in range(1, 10):
                for val in self.candidates[i-1][c-1]:
                    inverted_index[val-1].add((i, c))
            
            for val in range(1, 10):
                if len(inverted_index[val-1]) == 1:
                    r, c = inverted_index[val-1].pop()
                    if self.B.get_cell(r, c) != 0:
                        continue
                    self.B.move(r, c, val)
                    self.update_candidates(r, c, val)
                    changed = True

        return changed

    def logical_step(self):
        changing1 = self.naked_singles()
        changing2 = self.unique_candidate()
        return changing1 or changing2


class SudokuSearchTree(GeneralSearchTree):

    def __init__(self, val):
        super(SudokuSearchTree, self).__init__(val)

        # It will continue solve the Sudoku logically until it does not know what to do
        # Then, it will bifercate using the search tree
        changing = True
        while changing:
            changing = self.val.logical_step()

    def isSolution(self):
        return self.val.B.is_solution()

    def prune(self):
        # There might be more cases that I could prune, which would make the AI faster
        if not self.val.B.is_consistent():
            return True
        
        for row in self.val.candidates:
            if set() in row:
                return True
            if set.union(*row) != set(range(1, 10)):
                return True

        for c in range(1, 10):
            col = [self.val.candidates[i][c-1] for i in range(9)]
            if set.union(*col) != set(range(1, 10)):
                return True

        for s in range(1, 10):
            square = [self.val.candidates[r-1][c-1] for r, c in self.val.B.get_square_indexes(s, include_self=True)]
            if set.union(*square) != set(range(1, 10)):
                return True

        return False

    def getEdges(self):
        cells = self.val.get_most_restructed_cells()

        # I actually only need to look at the most restricted cell, because we know one of them has to be correct
        r, c, candidates = cells[0]
        return [ (r, c, val) for val in candidates ]

    def heuristic(self, L):
        # edges are already sorted by least number of candidates
        return L

    def copy_node(self):
        return SudokuSearchTree( self.val.copy() )

    def evolve(self, E):
        r, c, val = E
        self.val.B.move(r, c, val)
        self.val.update_candidates(r, c, val)
        return self


if __name__ == "__main__":

    from board import SudokuBoard
    from puzzles import *

    B = SudokuBoard(Extreme_3)
    print(B)

    L = SudokuLogicManager(B)
    print(L)

    T = SudokuSearchTree(L)
    leaf = T.search()
    if leaf == False:
        print("Could not find solution")
        raise Exception("could not solve board at index", i)
    else:
        print(leaf.val)
        print("Solution Found!")

    """
    changing = True
    while changing:
        changing = L.logical_step()
        print(L)
    """
