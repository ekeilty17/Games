from board import *
from general_search_tree import *


""""""""""""""""""""""""""""""""""""
"""                              """
"""   Finding any Knight's Tour  """
"""                              """
""""""""""""""""""""""""""""""""""""
class Knights_Tour_search_tree(general_search_tree):

    def __init__(self, val):
        general_search_tree.__init__(self, val)

    def isSolution(self):
        return self.val.isComplete()

    def prune(self):
        # If there exists a square with 0 possible knight moves,
        #   then it's impossible to ever get to that sqare,
        #   thus that board state could never be a knights tour
        # If there exists two squares each with 1 possible knight move,
        #   then that board state can't be a knights tour either bc you could get to each square
        #   but after that you wouldn't be able to get out of it
        cnt = 0
        for i in range(self.val.rows):
            for j in range(self.val.cols):
                if self.val.visited[i][j] == 0:
                    if self.val.Num_Knight_Moves([i,j]) == 0:
                        return True
                    elif self.val.Num_Knight_Moves([i,j]) == 1:
                        cnt += 1
                        if cnt == 2:
                            return True
        return False

    def getEdges(self):
        return self.val.Possible_Knight_Moves()

    def heuristic(self, L):
        return sorted(L, key=self.val.Num_Knight_Moves)

    def copy_node(self):
        return Knights_Tour_search_tree( self.val.new() )
    
    def evolve(self, E):
        self.val.Move(E)
        return self

    def Display(self):
        return self.val.Display()

def Knights_Tour(B):
    
    leaf = Knights_Tour_search_tree(B).search()
    if leaf == False:
        print "Knight's tour is not possible from this square"
        return []
    return leaf.back_track()



""""""""""""""""""""""""""""""""""""""
"""                                """
""" Finding a Closed Knight's Tour """
"""                                """
""""""""""""""""""""""""""""""""""""""
class Closed_Knights_Tour_search_tree(general_search_tree):

    def __init__(self, val):
        general_search_tree.__init__(self, val)

    def isSolution(self):
        return self.val.isClosed()

    def prune(self):
        # If there are no knight moves that can get to back to the start
        # then it can't be a closed knights tour
        if self.val.Num_Knight_Moves(self.val.start) == 0:
            return True

        # Getting rid of impossible cases
        cnt = 0
        for i in range(self.val.rows):
            for j in range(self.val.cols):
                if self.val.visited[i][j] == 0:
                    if self.val.Num_Knight_Moves([i,j]) == 0:
                        return True
                    elif self.val.Num_Knight_Moves([i,j]) == 1:
                        cnt += 1
                        if cnt == 2:
                            return True
        return False

    def getEdges(self):
        return self.val.Possible_Knight_Moves()

    def heuristic(self, L):
        return sorted(L, key=self.val.Num_Knight_Moves)
    
    def copy_node(self):
        return Closed_Knights_Tour_search_tree( self.val.new() )

    def evolve(self, E):
        self.val.Move(E)
        return self

    def Display(self):
        return self.val.Display()

def Closed_Knights_Tour(B):
    
    #Use some mathematical theorems so I don't fall into an infinite search
    if B.rows%2 == 1 and B.cols%2 == 1:
        print "A complete Knight's Tour is impossible with these dimensions."
        return False
    elif min(B.rows,B.cols) in [1,2,4]:
        print "A complete Knight's Tour is impossible with these dimensions."
        return False
    elif min(B.rows,B.cols) == 3 and max(B.rows,B.cols) in [4,6,8]:
        print "A complete Knight's Tour is impossible with these dimensions."
        return False
    
    leaf = Closed_Knights_Tour_search_tree(B).search()
    if leaf == False:
        print "Knight's tour is not possible from this square"
        return []
    return leaf.back_track()
