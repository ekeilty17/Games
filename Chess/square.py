from pieces import ChessPiece

class ChessSquare(object):

    # these are to display the square in the terminal
    LIGHT = "\x1b[90m"      # actually grey
    DARK = "\x1b[30m"       # actually black
    RESET = "\x1b[0m"

    def __init__(self, color, index, piece=None):
        if not color in ["LIGHT", "DARK"]:
            raise ValueError(f"Argument 'color' must be either 'LIGHT' or 'DARK'. Got value {color}")

        if type(index) != tuple or len(index) != 2:
            raise TypeError(f"Argument 'index' should be a 2-tuple. Got {index} with length {len(index)}")

        self.color = color      # "LIGHT" or "DARK"
        self.index = index
        self.piece = piece
        #self.selected = False
        #self.legal_move = False
    
    def __repr__(self):
        if self.is_empty():
            if self.color == "LIGHT":
                return f" {self.LIGHT}#{self.RESET} "
            else:
                return f" {self.DARK}_{self.RESET} "
        else:
            return f" {self.piece.__repr__()} "

    def copy(self):
        new_square = ChessSquare(color=self.color, index=self.index, piece=None if self.piece is None else self.piece.copy())
        return new_square

    def is_empty(self):
        return self.piece is None
    
    def contains_piece(self):
        return not self.is_empty()
