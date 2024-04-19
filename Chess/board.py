from abc import ABC, abstractmethod
from square import ChessSquare
from pieces import ChessPiece, Pawn, Knight, Bishop, Rook, Queen, King

class ChessBoard(ABC):
    
    # used for chess notation
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    BORDER_COLOR = "\x1b[90m"      # actually grey
    RESET = "\x1b[0m"

    def __init__(self, height, width, orientation='W', verbose=False):
        if height < 1:
            raise ValueError(f"Argument `height` must be greater than 0. Got value {height} instead.")
        if width < 1:
            raise ValueError(f"Argument `width` must be greater than 0. Got value {width} instead.")
        if orientation not in ['W', 'B']:
            raise ValueError(f"Argument 'orientation' needs to be either 'W' or 'B'. Got value {orientation} instead.")
        
        if width > len(self.alphabet):
            raise ValueError("A width of this length is currently not supported.")

        self.height = height
        self.width = width
        self.orientation = orientation
        self.verbose = verbose

        self.board = [ [ChessSquare(color="DARK" if (i+j)%2 == 0 else "LIGHT", index=(i, j)) for j in range(self.width)] for i in range(self.height) ]
        self.setup_pieces()

    def __repr__(self):
        display_board = []
        alpha_labels = [f"{self.BORDER_COLOR} {letter} {self.RESET}" for letter in self.alphabet[:self.width]]
        if self.orientation == 'W':
            for i, row in enumerate(reversed(self.board), 1):
                row_str = ' '.join([str(square) for square in row])
                display_board.append(f"{self.BORDER_COLOR} {str(self.height - i + 1):3s}{self.RESET} {row_str}")
            alpha_labels = ['    '] + alpha_labels
        else:
            for i, row in enumerate(self.board, 1):
                row_str = ' '.join([str(square) for square in reversed(row)])
                display_board.append(f"{self.BORDER_COLOR} {str(i):3s}{self.RESET} {row_str}")
            alpha_labels = ['    '] + list(reversed(alpha_labels))

        return '\n'.join(display_board) + '\n' + ' '.join(alpha_labels)

    # All of this is to make ChessBoard act like a 2D matrix and make it able to use without calling self.board
    def __getitem__(self, key):
        if type(key) == int:
            return self.board[key]
        elif type(key) == tuple:
            if len(key) == 1:
                return self.board[key[0]]
            elif len(key) == 2:
                return self.board[key[0]][key[1]]
            else:
                raise ValueError(f"Expected a tuple of length 1 or 2. Got value {key} instead.")
        else:
            raise TypeError(f"Expected a tuple or an integer. Got type {type(key)} instead.")

    def __setitem__(self, key, value):
        if type(key) == tuple and len(key) == 2:
            i, j = key
            if isinstance(value, ChessSquare):
                self.board[i][j] = value
            else:
                raise TypeError(f"Expected argument `value` to be of type `ChessSquare`. Got type {type(value)} instead.")
        else:
            raise TypeError(f"Expected argument `key` to be a 2-tuple. Got value {key} instead.")

    def __iter__(self):
        return self.board.__iter__()

    def __len__(self):
        return self.board.__len__()

    @abstractmethod
    def copy(self):
        new_board = ChessBoard(height=self.height, width=self.width, orientation=self.orientation, verbose=self.verbose)
        new_board.board = [[square.copy() for square in row] for row in self.board]
        return new_board

    # Some type checking helper functions
    def in_range(self, i, j):
        return ( (i in range(self.height)) and (j in range(self.width)) )
    def check_board_position(self, pos):
        if type(pos) != tuple:
            raise TypeError(f"Expecting argument `pos` to be a tuple. Got type {type(pos)} instead.")
        if len(pos) != 2:
            raise TypeError(f"Expecting argument `pos` to be a 2-tuple. Got length {len(pos)} instead.")
        
        i, j = pos
        if type(i) != int:
            raise TypeError(f"Expecting argument `i` to be an integer. Got type {type(i)} instead.")
        if type(j) != int:
            raise TypeError(f"Expecting argument `j` to be an integer. Got type {type(j)} instead.")
        if not self.in_range(i, j):
            raise IndexError(f"Arguments `i` and `j` are out of range of the board. Got values i={i} and j={j}. Must be integers between [0, {self.height}) and [0, {self.width}), respectively.")

    # Some miscellaneous helper functions
    def flip_board(self):
        self.orientation = 'B' if self.orientation == 'W' else 'W'
    def get_rank(self, i):
        # a rank is chess is a row
        if not i in range(self.height):
            raise ValueError(f"Index out of range, can only be in [0, {self.height}), got {i} instead.")
        return self.board[i-1]
    def get_file(board, j):
        # a file is chess is a column
        if not j in range(self.width):
            raise ValueError(f"Index out of range, can only be in [0, {self.width}), got {j} instead.")
        return [self.board[i][j] for i in range(self.width)]
    def index2chess(self, i, j):
        letter = self.alphabet[j]
        num = i + 1
        return letter, str(num)
    def chess2index(self, letter, num):
        j = self.alphabet.index(letter)
        i = int(num) - 1
        return i, j

    # The only class that needs to be implemented
    # defines the starting position of all the pieces
    @abstractmethod
    def setup_pieces(self):
        raise NotImplementedError()

    # adding piece to the board
    def add_piece_to_board(self, piece, pos):
        if not issubclass(piece.__class__, ChessPiece):
            raise TypeError(f"Expecting argument `piece` to be of type <ChessPiece>. Got type {type(piece)} instead.")
        self.check_board_position(pos)
        
        i, j = pos
        square = self.board[i][j]

        # place piece on board
        square.piece = piece

        # instantiate pointers to piece object back to it's squares
        piece.starting_square = square
        piece.current_square = square

    # moving peices from one square to another
    def move_piece(self, from_pos, to_pos):
        self.check_board_position(from_pos)
        self.check_board_position(to_pos)

        from_square = self[from_pos]
        to_square = self[to_pos]

        if from_square.is_empty():
            raise Exception("The square does not contain a piece to move.")
        
        from_piece = from_square.piece
        to_piece = to_square.piece

        # exchanging pieces
        from_square.piece = None
        to_square.piece = from_piece
        
        # maintaining peice pointers
        from_piece.current_square = to_square
        if to_piece is not None:
            to_piece.current_square = None
        
        return to_piece


class StandardChessBoard(ChessBoard):

    def __init__(self, orientation='W', verbose=False):
        super(StandardChessBoard, self).__init__(height=8, width=8, orientation=orientation, verbose=verbose)

    def copy(self):
        new_board = StandardChessBoard(orientation=self.orientation, verbose=self.verbose)
        new_board.board = [[square.copy() for square in row] for row in self.board]
        return new_board

    def setup_pieces(self):
        # This function assumes that the board is 8x8
        piece_classes = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for j in range(self.width):
            piece_class = piece_classes[j]
            self.add_piece_to_board(piece_class('W'), (0, j))
            self.add_piece_to_board(Pawn('W'), (1, j))
            self.add_piece_to_board(Pawn('B'), (self.height-2, j))
            self.add_piece_to_board(piece_class('B'), (self.height-1, j))

if __name__ == "__main__":
    B = StandardChessBoard(orientation='W', verbose=True)
    
    for row in reversed(B):
        print(" ".join([''.join(B.index2chess(*square.index)) for square in row]))
    print()
    
    print()
    print(B)
    print()
    B.flip_board()
    print(B)
    print()

    B.move_piece((1, 0), (3, 0))
    B.move_piece((6, 0), (3, 0))
    print(B)
    print()
    