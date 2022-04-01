
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
    x_color = '\033[91m'            # red text
    
    bold = '\033[01m'
    reset = '\033[0m'

    def __init__(self, mine=False, count=0, initial_state="hidden"):
        self.mine = mine            # whether the cell itself contains a mine
        self.count = count          # number of mines in the boarding cells (including itself)
        self.initial_state = initial_state

        self.initialize_fsm()

    def __repr__(self):
        return self.states[self.current_state]

    def contains_mine(self):
        return self.mine

    def initialize_fsm(self):
        self.transitions = ["left click", "right click", "win", "lose"]
        self.states = {
            "hidden" : "#",
            "flagged": f"{self.flag_color}#{self.reset}",
            "question mark": f"{self.bold}?{self.reset}",
            "number" : f"{self.background_color} {self.reset}" if self.count == 0 else f"{self.background_color}{self.bold}{self.colors[self.count-1]}{self.count}{self.reset}",
            "mine": f"{self.mine_color}{self.bold}*{self.reset}",
            "red mine": f"{self.mine_color}{self.bold}*{self.reset}",
            "crossed out mine": f"{self.x_color}{self.bold}X{self.reset}"
        }

        # by default the FSM is the identity FSM, meaning all transitions do nothing
        self.FSM = {}
        for state in self.states:
            for transition in self.transitions:
                self.FSM[state, transition] = state

        # the cell has a different FSM depending on if it contains a mine or not
        if self.contains_mine():
            self.initialize_mine_fsm()
        else:
            self.initialize_no_mine_fsm()
        
        # all cells begin as hidden
        self.previous_state = None
        self.current_state = self.initial_state

    def initialize_mine_fsm(self):
        self.FSM["hidden", "left click"] = "red mine"
        self.FSM["hidden", "right click"] = "flagged"
        self.FSM["hidden", "win"] = "flagged"
        self.FSM["hidden", "lose"] = "mine"

        self.FSM["flagged", "left click"] = "question mark"
        self.FSM["flagged", "right click"] = "hidden"

        self.FSM["question mark", "left click"] = "flagged"
        self.FSM["question mark", "right click"] = "hidden"
        self.FSM["question mark", "lose"] = "mine"
    
    def initialize_no_mine_fsm(self):
        self.FSM["hidden", "left click"] = "number"
        self.FSM["hidden", "right click"] = "flagged"
        
        self.FSM["flagged", "left click"] = "question mark"
        self.FSM["flagged", "right click"] = "hidden"
        self.FSM["flagged", "lose"] = "crossed out mine"

        self.FSM["question mark", "left click"] = "flagged"
        self.FSM["question mark", "right click"] = "hidden"
    
    def action(self, transition):
        self.previous_state = self.current_state
        self.current_state = self.FSM[self.previous_state, transition]
    
    def state_changed(self):
        return self.previous_state != self.current_state

    def is_hidden(self):
        return self.current_state in ["hidden", "flagged", "question mark"]
    
    def is_visible(self):
        return not self.is_hidden()
    
    def is_flagged(self):
        return self.current_state == "flagged"

if __name__ == "__main__":
    cell = MinesweeperCell()