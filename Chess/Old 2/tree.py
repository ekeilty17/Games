class tree:
    def __init__(self,x):
        self.val = x
        self.move = []
        self.children = []
        self.material = 0
        self.position = 0

    def AddSuccessor(self,T):
        self.children += [T]
        return True

    #for debugging purposes, not actually used in the code
    def Print_DepthFirst(self):
        def rec(x,indent):
            print indent + displayNode(x)
            indent += "\t"
            for i in range(0,len(x.children)):
                rec(x.children[i],indent)
            return True

        return rec(self,"")


#For debugging purposes
def displayNode(root):
    if root == None:
        return False

    #Display Function
    pieces = {  0: 'p',
                1: 'N',
                2: 'B',
                3: 'R',
                4: 'Q',
                5: 'K'
            }
    blank_board = [ ['_', '#', '_', '#', '_', '#', '_', '#'],
                    ['#', '_', '#', '_', '#', '_', '#', '_'],
                    ['_', '#', '_', '#', '_', '#', '_', '#'],
                    ['#', '_', '#', '_', '#', '_', '#', '_'],
                    ['_', '#', '_', '#', '_', '#', '_', '#'],
                    ['#', '_', '#', '_', '#', '_', '#', '_'],
                    ['_', '#', '_', '#', '_', '#', '_', '#'],
                    ['#', '_', '#', '_', '#', '_', '#', '_']
                  ]
    out = []
    out = "\x1b[90m" + "   1  2  3  4  5  6  7  8" + "\x1b[0m" + "\n"
    alpha = ['a','b','c','d','e','f','g','h']
    for i in range(7,-1,-1):
        s_temp =  "\x1b[90m" + alpha[i] + " " + "\x1b[0m"
        for j in range(0,8):
            if root.val[i][j] == 0:
                if blank_board[i][j] == '_':
                    s_temp += " \x1b[30m" + blank_board[i][j] + "\x1b[0m "
                else:
                    s_temp += " \x1b[90m" + blank_board[i][j] + "\x1b[0m "
            elif 10 <= root.val[i][j] and root.val[i][j] < 20:
                s_temp += " \x1b[97m" + pieces[root.val[i][j]-10] + "\x1b[0m "
            elif 20 <= root.val[i][j]:
                s_temp += " \x1b[34m" + pieces[root.val[i][j]-20] + "\x1b[0m "
        out += s_temp
        if i != 0:
            out += "\n"
    print out
    print
    print
    return out
