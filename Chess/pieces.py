from abc import ABC, abstractmethod

class ChessPiece(ABC):
    
    WHITE = "\x1b[97m"      # actually white
    BLACK = "\x1b[34m"      # actually blue

    RESET = "\x1b[0m"

    def __init__(self, color):
        if not color.upper() in ["W", "B"]:
            raise ValueError(f"Argument 'color' must be either 'W' or 'B'. Got value {color}")
        self.color = color.upper()      # 'W' or 'B'
        
        # These are instantiated and maintained by the ChessBoard class
        self.starting_square = None
        self.current_square = None

    def copy(self):
        new_piece = self.__class__(color=self.color)
        new_piece.starting_square = self.starting_square
        new_piece.current_square = self.current_square
        return new_piece
    
    def __repr__(self):
        return f"{self.WHITE if self.color == 'W' else self.BLACK}{self.char}{self.RESET}"

    """
    I define `path` a path as an ordered sequence of `moves`
    For example, a rook that can travel along the a-file would have path [a1, a2, a3, ..., a8]

    These functions contain `relative paths`, which means the moves are offsets of the position of the current piece
    In the rook example, [(1, 0), (2, 0), (3, 0), ...] would define its ability to move up ranks
    
    The output is a list of paths
    """
    @abstractmethod
    def get_all_relative_move_paths(self, height, width):
        raise NotImplementedError()
    
    def get_all_relative_capture_paths(self, height, width):
        return self.get_all_relative_move_paths(height=height, width=width)

    """
    I separate chess moves into 2 types
        1) single state moves: these moves depend only on the current board state to determine
        2) multi-state moves: these moves depend on previous states to determine, such as en passant and castling
    
    Type 1) moves will be handled by the pieces themselves
    Type 2) moves will be handled by the chess backend

    The Piece class handles all the Type 1) moves given a board state.
    It does through the following steps
        1) Converts the relative paths to absolute paths given the position of the piece
        2) Removes any move that is out of range of the board
        3) Truncates the path sequence if it is blocked by another piece
    """
    def relative_to_absolute_paths(self, relative_paths, board):
        if self.current_square is None:
            raise TypeError("This piece is not yet placed on a square.")
        i, j = self.current_square.index

        # convert the relative offsets into the actual squares indices on the board
        absolute_paths = []
        if self.color == 'W':
            absolute_paths = [ list(map(lambda offset: (i + offset[0], j + offset[1]), seq)) for seq in relative_paths ]
        else: # piece.color == 'B'
            absolute_paths = [ list(map(lambda offset: (i - offset[0], j - offset[1]), seq)) for seq in relative_paths ]

        # filter put moves that are out of range of the board
        absolute_paths_in_range = []
        for seq in absolute_paths:
            new_seq = []
            for move in seq:
                if board.in_range(*move):
                    new_seq.append(move)
            if new_seq != []:
                absolute_paths_in_range.append(new_seq)
        
        return absolute_paths_in_range

    def get_legal_moves(self, board):
        relative_paths = self.get_all_relative_move_paths(height=board.height, width=board.width)
        absolute_paths = self.relative_to_absolute_paths(relative_paths, board)
        
        # now we remove sqaures that are blocked by other pieces
        legal_moves = []
        for seq in absolute_paths:
            for move in seq:
                dest_square = board[move]          # destination square
                
                # if the square contains a piece, we stop the sequence
                if dest_square.contains_piece():
                    break
                # otherwise the square is empty and we can move to that square and continue on the sequence
                else:
                    legal_moves.append(move)

        return legal_moves

    def get_legal_captures(self, board):
        relative_paths = self.get_all_relative_capture_paths(height=board.height, width=board.width)
        absolute_paths = self.relative_to_absolute_paths(relative_paths, board)
        
        # now we remove sqaures that are blocked by other pieces
        legal_captures = []
        for seq in absolute_paths:
            for move in seq:
                dest_square = board[move]          # destination square
                
                # if the square contains a piece, we check if it's the opposite color, and capture it
                if dest_square.contains_piece():
                    if self.color != dest_square.piece.color:
                        legal_captures.append(move)
                    # since we captured a piece, we can't continue
                    break
                # otherwise the square is empty, so there's nothing to capture, and we continue on the path
                else:
                    continue
        
        return legal_captures




class Pawn(ChessPiece):

    name = "pawn"
    char = 'p'
    
    def get_all_relative_move_paths(self, height, width):
        # since pawns can't move backwards, this is sufficient
        print(self.starting_square.index, self.current_square.index)
        if self.current_square == self.starting_square:
            return [ [(1, 0), (2, 0)] ]
        else:
            return [ [(1, 0)] ]
    
    def get_all_relative_capture_paths(self, height, width):
        return [ [(1, -1)], [(1, 1)] ]

class Knight(ChessPiece):

    name = "knight"
    char = 'N'

    def get_all_relative_move_paths(self, height, width):
        return [            
                            [(-1, 2)],      [(1, 2)],
                    [(-2, 1)],                      [(2, 1)], 

                    [(-2, -1)],                     [(2, -1)],
                            [(-1, -2)],     [(1, -2)]
                ]

class Bishop(ChessPiece):

    name = "bishop"
    char = 'B'
    
    def get_all_relative_move_paths(self, height, width):
        return [
            [( i,  i) for i in range(1, max(width, height))],
            [( i, -i) for i in range(1, max(width, height))],
            [(-i,  i) for i in range(1, max(width, height))],
            [(-i, -i) for i in range(1, max(width, height))]
        ]

class Rook(ChessPiece):

    name = "rook"
    char = 'R'
    
    def get_all_relative_move_paths(self, height, width):
        return [
            [( i,  0) for i in range(1, height)],
            [(-i,  0) for i in range(1, height)],
            [( 0,  i) for i in range(1, width )],
            [( 0, -i) for i in range(1, width )]
        ]

class Queen(ChessPiece):

    name = "queen"
    char = 'Q'
    
    def get_all_relative_move_paths(self, width, height):
        return [
            [( i,  i) for i in range(1, max(width, height))],
            [( i, -i) for i in range(1, max(width, height))],
            [(-i,  i) for i in range(1, max(width, height))],
            [(-i, -i) for i in range(1, max(width, height))],
            [( i,  0) for i in range(1, height)],
            [(-i,  0) for i in range(1, height)],
            [( 0,  i) for i in range(1, width )],
            [( 0, -i) for i in range(1, width )]
        ]

class King(ChessPiece):

    name = "king"
    char = 'K'

    def get_all_relative_move_paths(self, width, height):
        return [
            [( 1, -1)], [( 1, 0)], [( 1, 1)],
            [( 0, -1)],            [( 0, 1)],
            [(-1, -1)], [(-1, 0)], [(-1, 1)]
        ]


if __name__ == "__main__":
    
    piece_classes = [Pawn, Bishop, Knight, Rook, Queen, King]
    pieces = [Pawn('W'), Bishop('W'), Knight('W'), Rook('W'), Queen('W'), King('W')]
    
    for piece in pieces:
        print(piece.name.title())
        print(piece.get_all_relative_move_paths(8, 8))
        print(piece.get_all_relative_capture_paths(8, 8))
        print()