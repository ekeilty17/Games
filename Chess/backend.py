from board import ChessBoard, StandardChessBoard

class ChessState(object):

    def __init__(self, board, to_move, captured_pieces, verbose=True):
        if not issubclass(board.__class__, ChessBoard):
            raise TypeError(f"Expecting argument `board` to be of type <ChessBoard>. Got type {type(board)} instead.")

        self.board = board
        self.to_move = to_move
        self.captured_pieces = captured_pieces
        self.verbose = verbose

        # A variable to keep track of if the player has the right to castle
        # (they may not be able to castle in the moment due to piece being in the way
        # but they have the potential to castle in the future)
        self.short_castling_rights = {'W': True, 'B': True}
        self.long_castling_rights = {'W': True, 'B': True}
        
        self.WIDTH = 8
        self.HEIGHT = 8

    def __repr__(self):
        out  = f"{'White' if self.to_move == 'W' else 'Black'} to move" + '\n'
        out += self.board.__repr__()
        out += "\n\n"
        out += "White Pieces Captured: " + ', '.join([str(piece) for piece in self.captured_pieces['W']]) + '\n'
        out += "Black Pieces Captured: " + ', '.join([str(piece) for piece in self.captured_pieces['B']]) + '\n'
        out += "\n"
        return out
    
    def copy(self):
        new_board = self.board.copy()
        new_captured_pieces = {'W': list(self.captured_pieces['W']), 'B':list(self.captured_pieces['B'])}
        return ChessState(board=new_board, to_move=self.to_move, captured_pieces=new_captured_pieces, verbose=self.verbose)

    def get_king_state(self):
        opponent_color = 'B' if self.to_move == 'W' else 'W'

        square_indeces_opponent_sees = set([])
        for piece in self.players[opponent_color]["active_pieces"]:
            square_indeces_opponent_sees = square_indeces_opponent_sees.union( piece.legal_moves )

        king_square = self.players[self.to_move]["king_square"]
        is_in_check = ( king_square.index in square_indeces_opponent_sees )

        print(king_square.piece.legal_moves)
        no_legal_moves = ( square_indeces_opponent_sees.intersection( king_square.piece.legal_moves ) == set() )

        return is_in_check, no_legal_moves
                

class ChessBackend(object):

    def __init__(self, starting_position, first_move='W', orientation='W', verbose=True):
        if orientation not in ['W', 'B']:
            raise ValueError(f"Argument 'orgientation' needs to be either 'W' or 'B'. Got value {orientation}")

        self.orientation = orientation
        self.verbose = verbose

        # TODO: do a check that starting position is correctly configured
        captured_pieces = {'W': [], 'B':[]}

        # initialize the first state
        self.starting_state = ChessState(board=starting_position, to_move=first_move, captured_pieces=captured_pieces, verbose=verbose)

        # keeps track of history of the game
        self.history = [self.starting_state]

        """
        # keeping a pointer to the rooks makes it easier to code castling
        self.rooks = {
            "W": {'a': rank1[0],  'h': rank1[-1]},
            "B": {'a': rank8[-1], 'h': rank8[0] }
        }

        # Some extra data structures to help with later functionality
        """

    """
    def copy(self):
        new_board = [[square.copy() for square in row] for row in self.board]
        new_captured_pieces = {'W': list(captured_pieces['W']), 'B': list(captured_pieces['B'])}
    """

    def __repr__(self):
        return self.get_current_state().__repr__()

    def get_current_state(self):
        return self.history[-1]
    
    def get_current_board(self):
        return self.get_current_state().board
    
    def get_board_height(self):
        return self.get_current_board().height
    
    def get_board_width(self):
        return self.get_current_board().width

    @staticmethod
    def toggle_to_move(to_move):
        return 'W' if to_move == 'B' else 'B'

    def get_legal_moves(self, i, j):
        board = self.get_current_board()
        square = board[i, j]

        # if square has no piece, then there are no possible moves
        if square.is_empty():
            return []
        
        piece = square.piece
        legal_moves = piece.get_legal_moves(board)

        # We have to do special logic to determine if the king can castle
        if piece.name == "king":
            #TODO: check for castling
            pass
        
        return legal_moves

    def get_legal_captures(self, i, j):
        board = self.get_current_board()
        square = board[i, j]

        # if square has no piece, then there are no possible moves
        if square.is_empty():
            return []
        
        piece = square.piece
        legal_moves = piece.get_legal_captures(board)

        # We have to do special logic to determine if the pawn can en passant 
        if piece.name == "pawn":
            #TODO: check for en passant capture
            pass
        
        return legal_moves

    def make_move(self, from_pos, to_pos):
        new_state = self.get_current_state().copy()

        from_square = new_state.board[from_pos]
        to_square = new_state.board[to_pos]

        # Checking the selected square has a piece
        if from_square.is_empty():
            raise Exception("Square does not contain a piece to make a move.")
        
        # getting the piece that's being moved
        moving_piece = from_square.piece

        # Checking the selected piece is the correct color
        if moving_piece.color != self.get_current_state().to_move:
            raise Exception(f"""It is not {"White's" if moving_piece.color == 'W' else "Black's"} turn""")

        # making sure the move is legal
        legal_moves = self.get_legal_moves(*from_pos) + self.get_legal_captures(*from_pos)
        print(legal_moves)
        # TODO: check if the king is in check and add that logic
        if to_pos not in legal_moves:
            raise Exception("Not a legal move")

        # making move on the board and keeping track of the captured pieces
        new_state.board.move_piece(from_pos, to_pos)
        
        # if the to_square contains a piece, then we capture it
        # we don't need to check whether it's the right color because that's taken care of by the valid_move function
        if to_square.contains_piece():
            new_state.captured_pieces[moving_piece.color].append( to_square.piece )
        
        # toggling next move for the next state
        new_state.to_move = self.toggle_to_move(new_state.to_move)
        
        # TODO
        # updating castling state
        # if new_state.short_castling_rights['W']:
        #     if from_square.piece.name == "king" or (from_square.piece == "rook")

        # updating board history
        self.history.append(new_state)

if __name__ == "__main__":
    Board = StandardChessBoard()
    Backend = ChessBackend(Board)
    print(Backend)

    Backend.make_move((1, 0), (3, 0))
    print(Backend)

    Backend.make_move((6, 1), (5, 1))
    print(Backend)

    Backend.make_move((3, 0), (4, 0))
    print(Backend)

    Backend.make_move((5, 1), (4, 0))
    print(Backend)