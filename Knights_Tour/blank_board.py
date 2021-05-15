
class blank_board:

    def __init__(self, rows, cols):
        
        #Error checks
        if type(rows) != int or type(cols) != int:
            raise TypeError("Rows and columns of board must be integers.")
        if rows < 1  or cols < 1:
            raise TypeError("Rows and columns of board must be positive integers.")
        if rows > 26 or cols > 26:
            raise TypeError("Bro...a little too big.")
        
        #variables
        self.rows = rows
        self.cols = cols

        #getting the black board
        self.store = []
        for i in range(self.rows):
            temp = []
            for j in range(self.cols):
                if (i+j)%2 == 0:
                    temp += ['_']
                else:
                    temp += ['#']
            self.store += [temp]

    def Display(self):
        alpha = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                  'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z' ]
        #print " ".join(alpha)
        out = "  ".join(alpha[:self.cols])
        out = "\x1b[90m" + "   " + out + "\x1b[0m" + "\n"
        for i in range(self.rows-1,-1,-1):
            s_temp =  "\x1b[90m" + str(i+1)
            if i+1 < 10:
                s_temp += " "
            s_temp += "\x1b[0m"
            for j in range(self.cols):
                if self.store[i][j] == '_':
                    s_temp += " \x1b[30m" + self.store[i][j] + " \x1b[0m"
                else:
                    s_temp += " \x1b[0m" + self.store[i][j] + " \x1b[0m"
            out += s_temp
            if i != 0:
                out += "\n"
        print out
        return out
