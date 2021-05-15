class tree:
    def __init__(self,x):
        self.val = x
        self.children = []
        self.heuristic = 0

    def AddSuccessor(self,T):
        self.children += [T]
        return True

    #for debugging purposes, not actually used in the code
    def Print_DepthFirst(self):
        def rec(x,indent):
            print indent + str(x.val)
            indent += "\t"
            for i in range(0,len(x.children)):
                rec(x.children[i],indent)
            return True

        return rec(self,"")
