from cell import MinesweeperCell
import random
import string

class MinesweeperGrid(object):

    def __init__(self, height, width, number_of_mines, verbose=True):
        self.isPositiveInteger(height)
        self.isPositiveInteger(width)
        self.isPositiveInteger(number_of_mines)
        if number_of_mines > height * width:
            raise ValueError("The number of mines cannot exceed the squares in the grid")
        
        self.HEIGHT = height
        self.WIDTH = width
        self.NUMBER_OF_MINES = number_of_mines

        self.construct_grid()

    def __repr__(self):
        output = ""
        for i in reversed(range(self.HEIGHT)):
            for j in range(self.WIDTH):
                output += self.grid[i][j].__repr__() + ' '
            output += "\n"
        return output[:-1]

    @staticmethod
    def isPositiveInteger(n):
        if type(n) != int:
            raise TypeError(f"Expected an integer and got type {type(n)}")
        if n <= 0:
            raise ValueError(f"Expected a positive integer and got value {n}")

    def get_cell(self, i, j):
        return self.grid[i][j]

    def coord_in_range(self, i, j):
        return (0 <= i < self.HEIGHT) and (0 <= j < self.WIDTH)

    def get_neighbor_indices(self, i, j, include_self=False):
        neighbor_indices = [
            (i-1, j-1), (i-1, j), (i-1, j+1),
            (i,   j-1),           (i,   j+1),
            (i+1, j-1), (i+1, j), (i+1, j+1)
        ]
        if include_self:
            neighbor_indices.append( (i, j) )
        neighbor_indices_in_range = set(filter(lambda t: self.coord_in_range(*t), neighbor_indices))
        return neighbor_indices_in_range

    # `no_mines` is a list of indices that cannot contain a mine
    def get_random_mine_indices(self, no_mines=None):
        if no_mines is None:
            no_mines = []
        possible_indices = [(i, j) for j in range(self.WIDTH) for i in range(self.HEIGHT) if (i, j) not in no_mines]
        mine_indices = random.sample(possible_indices, self.NUMBER_OF_MINES)
        return set(mine_indices)

    def construct_grid(self, no_mines=None):
        if no_mines is None:
            no_mines = []
        self.mine_indices = self.get_random_mine_indices(no_mines)

        # blank grid
        self.grid = [[None for j in range(self.WIDTH)] for i in range(self.HEIGHT)]
        
        # count mines in empty cells
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                neighbor_indices = self.get_neighbor_indices(i, j, include_self=True)
                mine_count = len(neighbor_indices.intersection(self.mine_indices))
                contains_mine = (i, j) in self.mine_indices
                self.grid[i][j] = MinesweeperCell(mine=contains_mine, count=mine_count, visible=False, flagged=False)

    def toggle_flag(self, i, j):
        cell = self.grid[i][j]
        cell.flag = (not cell.is_flagged())
    
    def make_visible(self, i, j):
        cell = self.grid[i][j]
        
        # is a cell is not visible
        if not cell.is_visible():
            # make it visible
            cell.visible = True
            # if the cell has no neighboring mines
            if cell.count == 0:
                # then we recursively make its neighbors visible
                neighbor_indices = self.get_neighbor_indices(i, j, include_self=False)
                for i, j in neighbor_indices:
                    self.make_visible(i, j)
    
    # This will resolve the neighboring cells based on the flags the user has put down
    def chord(self, i, j):
        cell = self.grid[i][j]

        if not cell.is_visible():
            self.make_visible(i, j)
            return
        
        neighbor_indices = self.get_neighbor_indices(i, j, include_self=False)
        flagged_neighbor_indices = set(filter(lambda n_cell: n_cell.is_flagged(), neighbor_indices))
        unflagged_neighbor_indices = (neighbor_indices - flagged_neighbor_indices)
        
        # we only chord if the number of flags matches the number mine count
        if len(flagged_neighbors) == cell.count:
            for n_cell in unflagged_neighbors:
                n_cell.make_visible()

    def get_exposed_mines(self):
        exposed_mine_indices = set()
        for i, j in self.mine_indices:
            cell = self.grid[i][j]
            if cell.is_visible():
                exposed_mine_indices.add( (i, j) )
        return exposed_mine_indices

        

if __name__ == "__main__":
    beginner = {"height": 9, "width": 9, "number_of_mines": 10}
    intermediate = {"height": 16, "width": 16, "number_of_mines": 40}
    expert = {"height": 16, "width": 30, "number_of_mines": 99}

    G = MinesweeperGrid(**expert)
    print(G)
    
    """
    while True:
        G = MinesweeperGrid(**expert)
        counts = [G.grid[i][j].count for i in range(G.HEIGHT) for j in range(G.WIDTH) if not G.grid[i][j].contains_mine()]
        if 6 in counts:
            print(G)
            break
    """