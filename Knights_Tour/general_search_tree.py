class general_search_tree(object):
    def __init__(self,x):
        self.val = x
        self.children = []
        self.parent = None
        
    def AddSuccessor(self,T):
        self.children += [T]
        T.parent = self
        return True
    
    def isSolution(self):
        raise NotImplementedError("The method not implemented")

    def prune(self):
        return False

    def getEdges(self):
        raise NotImplementedError("The method not implemented")

    def heuristic(self, L):
        return L
    
    def copy_node(self):
        raise NotImplementedError("The method not implemented")

    def evolve(self, E):
        raise NotImplementedError("The method not implemented")

    def Display(self):
        pass

    def search(self):
        if self == None:
            return False
        if self.val == None:
            return False

        self.Display()

        if self.isSolution():
            return self

        if self.prune():
            return False

        Edges = self.getEdges()
        Edges = self.heuristic(Edges)

        for E in Edges:
            self.AddSuccessor( self.copy_node().evolve(E) )
            
            r = self.children[-1].search()
            if r != False:
                return r
        return False

    def back_track(self, L=[]):
        if self == None:
            return L
        if self.parent == None:
            return L
        return self.parent.back_track([self.val] + L)
