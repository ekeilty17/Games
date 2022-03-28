class MinesweeperCell(object):

    colors = [
        '\033[94m',     # 1
        '\033[32m',     # 2
        '\033[91m',     # 3
        '\033[34m',     # 4
        '\033[31m',     # 5
        '\033[36m',     # 6
        '\033[30m',     # 7
        '\033[90m',     # 8
        '\033[43m'      # 9     (even though this would never be displayed)
    ]
    background_color = '\033[47m'   # light grey background
    flag_color = '\033[41m'         # red background
    mine_color = '\033[30m'         # black text
    
    bold = '\033[01m'
    reset = '\033[0m'
    
    def __init__(self, mine=False, count=0, visible=False, flagged=False):
        self.mine = mine            # whether the cell itself contains a mine
        self.count = count          # number of mines in the boarding cells (including itself)
        self.visible = visible      # whether the contents of the cell are visible
        self.flagged = flagged      # whether the user has flagged the cell
    
    def __repr__(self):
        if self.visible:
            if self.mine:
                return f"{self.flag_color}{self.mine_color}{self.bold}*{self.reset}"
            else:
                if self.count == 0:
                    return f"{self.background_color} {self.reset}"
                else:
                    return f"{self.background_color}{self.bold}{self.colors[self.count-1]}{self.count}{self.reset}"
        else:
            if self.flagged:
                return f"{self.flag_color}#{self.reset}"
            else:
                return "#"

    def contains_mine(self):
        return self.mine
    
    def is_visible(self):
        return self.visible
    
    def is_flagged(self):
        return self.flagged

if __name__ == "__main__":

    cell = Cell()
    print(cell)
    print()

    cell = Cell(flagged=True)
    print(cell)
    print()

    for i in range(9):
        cell = Cell(count=i, visible=True)
        print(cell)
    
    print()

    cell = Cell(mine=True, visible=True)
    print(cell)
    print()