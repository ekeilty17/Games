from random import choice

class general_alphabeta_tree(object):

    def __init__(self, val, isMaximizingPlayer=True):
        self.val = val
        self.children = []
        self.alpha = float('inf')
        self.beta = float('-inf')
        self.isMaximizingPlayer = isMaximizingPlayer

    def AddSuccessor(self, T):
        T.isMaximizingPlayer = not self.isMaximizingPlayer
        self.children += [T]
        return True

    def evaluation(self):
        # Parameter:        void
        # Return Type:      float
        #   A higher is a more prefered state
        # Implementation:   REQUIRED
        raise NotImplementedError("The method 'evaluation(self)' was not implemented")

    def isLeaf(self):
        # Parameter:        void
        # Return Type:      boolean
        #   True = Node is a leaf node, i.e. no more Edges exist
        #   False = Node is not a lead node
        # Implementation:   REQUIRED
        raise NotImplementedError("The method 'isLeaf(self)' was not implemented")

    def getEdges(self):
        # Parameter:        void
        # Return Type:      A list of Edges
        #   See comments in self.search() for my definition of an Edge
        # Implementation:   REQUIRED
        raise NotImplementedError("The method 'getEdges(self)' was not implemented")

    def copy_node(self):
        # Parameter:        void
        # Return Type:      Child class that implements the general_search_tree class
        # Implementation:   REQUIRED
        raise NotImplementedError("The method 'copy_node(self)' was not implemented")

    def evolve(self, E):
        # Parameter:        An Edge
        # Return Type:      Child class that implements the general_search_tree class
        # Implementation:   REQUIRED
        raise NotImplementedError("The method 'evolve(self, E)' was not implemented")

    def search(self, depth):
        # Bad input
        if self.val == None:
            return False

        # Reached a terminating node (e.g. checkmate in chess)
        if self.isLeaf():
            return self.evaluation()
        # Reached end of depth
        if depth == 0:
            return self.evaluation()

        # Getting Edges
        #   Edges take the parent node to the child node
        #   For example if the game was chess, an edge would be moving a pawn to a2 to a4
        #   and the evolve function is responsible for handling that logic
        Edges = self.getEdges()

        # Another possible way to handle a terminating node
        # TODO I don't think this ever gets called
        if Edges == []:
            return self.val.evaluation()

        # The core of the algorithm
        if self.isMaximizingPlayer:
            # initialize v
            v = float("-inf")
            for E in Edges:
                # create child
                self.AddSuccessor( self.copy_node().evolve(E) )
                # searching
                v = max(v, self.children[-1].search(depth-1))
                # back propogating
                self.alpha = max(self.alpha, v)
                # pruning
                if self.beta >= self.alpha:
                    break
            return v
        else:
            # initialize v
            v = float("inf")
            for E in Edges:
                # create child
                self.AddSuccessor( self.copy_node().evolve(E) )
                # searching
                v = min(v, self.children[-1].search(depth-1))
                # back propogating
                self.beta = min(self.beta, v)
                # pruning
                if self.beta >= self.alpha:
                    break
            return v

    def getBestChild(self, depth):
        # .search just returns the evaluation of a node, so we can't call it on the root
        # Instead we call it on every child and then return the child with the maximum evaluation

        # Getting Edges
        Edges = self.getEdges()
        # check if current state is already complete
        if Edges == []:
            return False

        # creating children
        for E in Edges:
            self.AddSuccessor( self.copy_node().evolve(E) )

        # Getting values of children
        children_alphabeta = []
        for C in self.children:
            children_alphabeta += [C.search(depth-1)]

        # returning the appropriate child
        #   just for variety, if there are multiple children with the same evaluation,
        #   then it will return one of them at random
        if self.isMaximizingPlayer:
            max_child = max(children_alphabeta)
            return choice([self.children[i] for i in range(len(self.children)) if children_alphabeta[i] == max_child])
        else:
            min_child = min(children_alphabeta)
            return choice([self.children[i] for i in range(len(self.children)) if children_alphabeta[i] == min_child])
