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
        self.verbose = verbose

        # instantiates self.mine_indices and self.grid
        self.initialize_grid()

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
    def get_random_mine_indices(self, avoid_indicies=None):
        if avoid_indicies is None:
            avoid_indicies = []
        possible_indices = [(i, j) for j in range(self.WIDTH) for i in range(self.HEIGHT) if (i, j) not in avoid_indicies]
        mine_indices = random.sample(possible_indices, self.NUMBER_OF_MINES)
        return set(mine_indices)

    def initialize_grid(self, first_click_index=None):
        # To make the game more fun, we always ensure the first click is a cell with no mines 
        # in the cell itself and in the neighboring cells
        avoid_indicies = []
        if first_click_index is not None:
            i, j = first_click_index
            avoid_indicies = self.get_neighbor_indices(i, j, include_self=True)
        
        # randomly placing mines everywhere else
        self.mine_indices = self.get_random_mine_indices(avoid_indicies=avoid_indicies)

        # blank grid
        self.grid = [[None for j in range(self.WIDTH)] for i in range(self.HEIGHT)]
        
        # count mines in empty cells
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                neighbor_indices = self.get_neighbor_indices(i, j, include_self=True)
                mine_count = len(neighbor_indices.intersection(self.mine_indices))
                contains_mine = (i, j) in self.mine_indices
                self.grid[i][j] = MinesweeperCell(mine=contains_mine, count=mine_count)
        
        # we need to keep track of these things to know when the game is over
        self.number_of_flags = 0
        self.no_mine_indices = set([(i, j) for j in range(self.WIDTH) for i in range(self.HEIGHT)]) - self.mine_indices
        self.visible_cell_indices = set()


    def left_click(self, i, j):
        cell = self.grid[i][j]

        # Prevents cyclic calls to neighboring cells
        if cell.is_visible():
            return

        # preform the left click
        cell.action("left click")

        # if the left click resulted in the cell becoming visible, then we need to check some stuff
        if cell.is_visible():
            self.visible_cell_indices.add( (i, j) )

            # if the cell has no neighboring mines
            if cell.count == 0:
                # then we recursively make its neighbors visible
                neighbor_indices = self.get_neighbor_indices(i, j, include_self=False)
                for i, j in neighbor_indices:
                    self.left_click(i, j)
        # If we've toggle between "flagged" and "question mark" then we need to update the flag count
        else:
            self.number_of_flags += (cell.current_state == "flagged") - (cell.previous_state == "flagged")
    
    # This implements chordings, which will resolve the neighboring cells based on the flags the user has put down
    # It is assumed that this function is only called on cells that are already visible
    def middle_click(self, i, j):
        cell = self.grid[i][j]

        if cell.is_hidden():
            return
        
        neighbor_indices = self.get_neighbor_indices(i, j, include_self=False)
        flagged_neighbor_indices = set(filter(lambda t: self.grid[t[0]][t[1]].is_flagged(), neighbor_indices))
        unflagged_neighbor_indices = (neighbor_indices - flagged_neighbor_indices)
        
        # we only chord if the number of flags matches the number mine count
        if len(flagged_neighbor_indices) == cell.count:
            for x, y in unflagged_neighbor_indices:
                self.left_click(x, y)

    def right_click(self, i, j):
        cell = self.grid[i][j]
        cell.action("right click")
        self.number_of_flags += (cell.current_state == "flagged") - (cell.previous_state == "flagged")
    
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