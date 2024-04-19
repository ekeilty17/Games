from backend import ChessBackend
from board import StandardChessBoard
#from square import ChessSquare
from pieces import Pawn, Knight, Bishop, Rook, Queen, King
from colors import *
import pygame

"""
Notation:
    - pos=(pix_x, pix_y) = pixel value of screen
    - (x, y) = coordinate value of grid, which is the same regardless of board orientation
    - (i, j) = indices of self.B.board
    - (letter, num) = chess notation of the square
"""


class ChessEngine(object):

    # dimension (in pixels) of the squares of the chess board
    SQUARE_WIDTH = 80
    SQUARE_HEIGHT = 80

    # Game Speed: frames per second
    #FPS = 30

    HIGHLIGHT = (255, 255, 153,  20)     # actually an opaque yellow
    CANDIDATE = ( 58, 198,  30, 0.3)         # actually a grey

    """ Stage 1: Initialize Game """
    def __init__(self, orientation='W', color_scheme="lichess", verbose=True):
        # initialize parameters
        self.orientation = orientation
        self.color_scheme = str(color_scheme).lower()
        self.verbose = verbose

        # Initializing Chess Board backend
        Board = StandardChessBoard()
        self.backend = ChessBackend(Board, verbose=verbose)

        # Initializing pygame front-end
        pygame.init()
        pygame.display.set_caption("Chess")

        # The game layout will look as follows
        #   +-----------------------------+
        #   | +-------------+ +---------+ |
        #   | |             | | P1 info | |
        #   | | chess board | +---------+ |
        #   | |             | | P2 info | |
        #   | +-------------+ +---------+ |
        #   +-----------------------------+
        #
        # P1 and P2 info will include the time remaining, a draw offer button, forfiet button, and captured pieces

        # initializes the asthetics of the game display and various screens
        self.set_up_color_scheme_and_game_design()

        # calculates the size and location of the various screens
        self.initialize_screen_dimensions_and_locations()

        # Creating and drawing the screens that we need
        self.full_screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.p1_info_screen = pygame.Surface((self.INFO_WIDTH, self.INFO_HEIGHT))
        self.p2_info_screen = pygame.Surface((self.INFO_WIDTH, self.INFO_HEIGHT))
        self.board_screen = pygame.Surface((self.BOARD_WIDTH, self.BOARD_HEIGHT))

        self.full_screen.blit(self.p1_info_screen, self.p1_info_screen_topleft_position)
        self.full_screen.blit(self.p2_info_screen, self.p2_info_screen_topleft_position)
        self.full_screen.blit(self.board_screen, self.board_screen_topleft_position)

        # Drawing the static elements in the `full_screen` which will not change
        self.draw_game_container()

        # Pushing the drawn elements to the screen
        pygame.display.flip()

        # loading the piece images is very expensive, so we only want to do this once
        # the processed images are stored in self.piece_images indexed by color and piece character
        self.initialize_piece_images()

        # Initializing game clock
        clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

        # keeping track of what square/piece is currently selected by the user
        self.selected_square = None
        self.previous_selected_square = None
        self.selected_piece = None

        # display legal moves
        self.selected_legal_moves = []
    
    def initialize_screen_dimensions_and_locations(self):
        board_width = self.backend.get_board_width()
        board_height = self.backend.get_board_height()

        # screen dimensions
        self.BOARD_WIDTH = board_width * self.SQUARE_WIDTH + self.BORDER + self.SQUARE_GAP * (board_width - 1) + self.BORDER
        self.BOARD_HEIGHT = board_height * self.SQUARE_HEIGHT + self.BORDER + self.SQUARE_GAP * (board_height - 1) + self.BORDER

        self.BUFFER = 15
        self.INFO_WIDTH = 2*self.BOARD_WIDTH//3
        self.INFO_HEIGHT = self.BOARD_HEIGHT//2 - 2*self.BUFFER

        self.WIDTH = self.BUFFER + self.BOARD_WIDTH + self.BUFFER + self.INFO_WIDTH + self.BUFFER
        self.HEIGHT = self.BUFFER + self.BOARD_HEIGHT + self.BUFFER

        # screen positions
        self.full_screen_topleft_position = (0, 0)
        self.board_screen_topleft_position = (self.BUFFER, self.BUFFER)
        self.p1_info_screen_topleft_position = (self.BUFFER + self.BOARD_WIDTH + self.BUFFER, self.BUFFER + self.BUFFER)
        self.p2_info_screen_topleft_position = (self.BUFFER + self.BOARD_WIDTH + self.BUFFER, self.HEIGHT - self.BUFFER - self.BUFFER - self.INFO_HEIGHT)

    def set_up_color_scheme_and_game_design(self):
        self.SQUARE_GAP = 0             # this is the space between squares, think bathroom tiles
        self.BORDER = 0                 # an outline around the board

        # initializing color scheme
        if self.color_scheme == "black and white":
            self.LIGHT, self.DARK, self.BACKGROUND, self.SECONDARY_BACKGROUND = BLACK_AND_WHITE
            self.BORDER = 2
        elif self.color_scheme == "lichess":
            self.LIGHT, self.DARK, self.BACKGROUND, self.SECONDARY_BACKGROUND = LICHESS
        elif self.color_scheme == "chess.com":
            self.LIGHT, self.DARK, self.BACKGROUND, self.SECONDARY_BACKGROUND = CHESS_DOT_COM
        else:
            raise ValueError(f"We do not support the color scheme '{self.color_scheme}'")

    def draw_game_container(self):
        self.full_screen.fill(self.BACKGROUND)

        # drawing background to the info screen and game screen
        self.p1_info_screen.fill(self.SECONDARY_BACKGROUND)
        self.p2_info_screen.fill(self.SECONDARY_BACKGROUND)
        self.board_screen.fill(BLACK)        # why the "SQUARE_GAP"s and "BORDER" appears black

        if self.BORDER != 0:
            self.p1_info_screen.fill(self.BACKGROUND, self.p1_info_screen.get_rect().inflate(-2*self.BORDER, -2*self.BORDER))
            self.p2_info_screen.fill(self.BACKGROUND, self.p2_info_screen.get_rect().inflate(-2*self.BORDER, -2*self.BORDER))
        
        self.full_screen.blit(self.p1_info_screen, self.p1_info_screen_topleft_position)
        self.full_screen.blit(self.p2_info_screen, self.p2_info_screen_topleft_position)
        self.full_screen.blit(self.board_screen, self.board_screen_topleft_position)

    def initialize_piece_images(self):
        self.piece_images = {"W": {}, "B": {}}
        for color in ["W", "B"]:
            for piece_class in [Pawn, Knight, Bishop, Rook, Queen, King]:
                img = pygame.image.load(f"assets2/{color}-{piece_class.name.lower()}.png")
                buffer = 5
                img = pygame.transform.scale(img, (self.SQUARE_WIDTH-self.SQUARE_GAP-buffer, self.SQUARE_HEIGHT-self.SQUARE_GAP-buffer))
                img.convert()       # optimizes image file to make drawing faster
                self.piece_images[color][piece_class.char] = img

    # functions that translate between pixels, grid coordinates, and chess notation
    def pixel2coordinate(self, pos):
        # This gets a bit confusing because there is a fundamental mis-match between the way the board is stored and the spacial representation of the board
        # when we index the self.B.board, we index by row first and column second, which means (0, 1) is actually the coordinate (1, 0) in the x-y plane
        # so it's going to seem stupid because we have to swap x and y for the intermediate index, and then swap them back for the chess index
        # but it makes things easier to work with on the backend and as long as these functions work correctly, it doesn't really matter
        pix_x, pix_y = pos

        x = pix_x // (self.SQUARE_WIDTH + self.SQUARE_GAP)
        y = pix_y // (self.SQUARE_HEIGHT + self.SQUARE_GAP)

        if self.verbose:
            print(f"Click: {pos}\tGrid coordinates: {(x, y)}", end="\t")
        return x, y  
    def coordinate2index(self, x, y):
        i, j = y, x             # notice we just swap x and y to get the index

        if self.orientation == 'W':
            i = (self.backend.get_board_height()-1) - i
        else:
            j = (self.backend.get_board_width()-1) - j

        if self.verbose:
            print(f"Matrix index: {(i, j)}\tChess: {''.join(self.index2chess(i, j))}", end="\t")
        return i, j 
    def index2coordinate(self, i, j):
        if self.orientation == 'W':
            i = (self.backend.get_board_height()-1) - i
        else:
            j = (self.backend.get_board_width()-1) - j
        
        x, y = j, i             # notice we just swap i and j to get the coordiate
        return x, y
    def index2chess(self, i, j):
        board = self.backend.get_current_board()
        return board.index2chess(i, j)
    def chess2index(self, letter, num):
        board = self.backend.get_current_board()
        return board.chess2index(letter, num)

    # gets the pygame representation of a rectangle 
    def get_square(self, x, y):
        return (    self.BORDER + (self.SQUARE_WIDTH + self.SQUARE_GAP) * x , 
                    self.BORDER + (self.SQUARE_HEIGHT + self.SQUARE_GAP) * y, 
                    self.SQUARE_WIDTH,
                    self.SQUARE_HEIGHT
        )
    
    def update_info_screen(self):
        pass

    def update_board_screen(self):
        
        # drawing the background and the piece in each square of the board
        color = self.DARK
        for i in range(self.backend.get_board_height()):
            for j in range(self.backend.get_board_width()):
                # getting square and it's corresponding coordinate on the board
                board = self.backend.get_current_board()
                square = board[i, j]
                color = self.LIGHT if square.color == "LIGHT" else self.DARK
                x, y = self.index2coordinate(i, j)
                square_pos = self.get_square(x, y)
                
                # drawing square
                pygame.draw.rect(self.board_screen, color, square_pos)

                # drawing piece
                if square.contains_piece():
                    piece = square.piece
                    
                    # highlight square if selected
                    if square == self.selected_square:
                        pygame.draw.rect(self.board_screen, self.HIGHLIGHT, square_pos)
                    
                    if piece == self.selected_piece:
                        continue
                    piece_img = self.piece_images[piece.color][piece.char]
                    square_center = (square_pos[0] + self.SQUARE_WIDTH//2, square_pos[1] + self.SQUARE_HEIGHT//2)
                    piece_rect = piece_img.get_rect()
                    piece_rect.center = square_center
                    self.board_screen.blit(piece_img, piece_rect)

        # draw selected piece last
        if self.selected_piece is not None:
            piece = self.selected_piece
            piece_img = self.piece_images[piece.color][piece.char]
            square_center = (square_pos[0] + self.SQUARE_WIDTH//2, square_pos[1] + self.SQUARE_HEIGHT//2)
            piece_rect = piece_img.get_rect()
            piece_rect.center = pygame.mouse.get_pos()
            self.board_screen.blit(piece_img, piece_rect)
        
        for i, j in self.selected_legal_moves:
            board = self.backend.get_current_board()
            square = board[i, j]
            x, y = self.index2coordinate(i, j)
            square_pos = self.get_square(x, y)
            square_center = (square_pos[0] + self.SQUARE_WIDTH//2, square_pos[1] + self.SQUARE_HEIGHT//2)
            radius = min(self.SQUARE_WIDTH, self.SQUARE_HEIGHT) // 8
            pygame.draw.circle(self.board_screen, self.HIGHLIGHT, square_center, radius)

        """
        # Adding pieces based on board state
        pieces = []
        for i in range(self.B.HEIGHT):
            for j in range(self.B.WIDTH):
                # needed for various things
                x, y = self.index2coordinate(i, j)
                square_pos = self.get_square(x, y)
                square_center = (square_pos[0] + self.SQUARE_WIDTH//2, square_pos[1] + self.SQUARE_HEIGHT//2)

                # get square from ChessBoard
                square = self.B.get_square(i, j)

                # if user has selected the square, then we highlight the square
                if square.selected:
                    pygame.draw.rect(self.screen, self.HIGHLIGHT, square_pos)

                # if user selected a piece, we display it's possible moves
                if square.legal_move:
                    radius = min(self.SQUARE_WIDTH, self.SQUARE_HEIGHT) // 8
                    pygame.draw.circle(self.screen, self.CANDIDATE, square_center, radius)

                # if square contains no pieces, then we are done
                if square.is_empty():
                    continue

                # if the square contains a piece, then we get the piece
                piece = square.piece
                
                # load image of piece
                piece.img = pygame.image.load(f"assets2/{piece.color}-{piece.name.lower()}.png")
                piece.img = pygame.transform.scale(piece.img, (self.SQUARE_WIDTH-self.SQUARE_GAP-5, self.SQUARE_HEIGHT-self.SQUARE_GAP-5))
                piece.img.convert()    # optimizes image file to make drawing faster

                # get rectangle the image occupies
                piece.rect = piece.img.get_rect()

                # set the piece's location to where the ChessBoard says it should go
                piece.rect.center = square_center
                
                # draw piece
                self.screen.blit(piece.img, piece.rect)
                
                # add image and rectangle to list so we can access them later
                pieces.append( piece )
        """

        self.full_screen.blit(self.board_screen, self.board_screen_topleft_position)

        # Updating board
        pygame.display.flip()

        # TODO: Check if keeping track of the pieces is necessary
        pieces = []
        return pieces

    def run(self):
        
        # Initializing board display
        self.update_info_screen()
        self.update_board_screen()
       
        # TODO: implement dragging

        running = True
        selected_piece = None
        while running:
            
            for event in pygame.event.get():
                # So code stops when you click the red x to quit the game
                if event.type == pygame.QUIT:
                    running = False

                # getting square that was clicked on
                pos = pygame.mouse.get_pos()
                x, y = self.pixel2coordinate(pos)
                i, j = self.coordinate2index(x, y)
                board = self.backend.get_current_board()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                       # we are in the game screen
                        if board.in_range(i, j):
                            square = board[i, j]

                            if (i, j) in self.selected_legal_moves:
                                self.selected_piece = square.piece
                                self.previous_selected_square = self.selected_square

                            elif square.contains_piece():
                                self.selected_piece = square.piece
                                self.previous_selected_square = self.selected_square
                                self.selected_square = square
                                self.selected_legal_moves = self.backend.get_legal_moves(i, j) + self.backend.get_legal_captures(i, j)
                            else:
                                self.selected_piece = None
                                self.previous_selected_square = self.selected_square
                                self.selected_square = None
                                self.selected_legal_moves = []
                            
                        # we are in the info screen
                        else:
                            pass
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    # if we click on the same piece twice, we need to unselect the square
                    self.selected_piece = None
                    if self.previous_selected_square == self.selected_square:
                        self.selected_square = None

                    if event.button == 1:
                        # we are in the game screen
                        if board.in_range(i, j):
                            square = board[i, j]
                            
                            #if self.previous_selected_square.contains_piece() and self.selected_square is not None:
                                #self.B.make_move(self.selected_square.index, (i, j))

                        # we are in the info screen
                        else:
                            pass
                
                elif event.type == pygame.MOUSEMOTION:
                    # we are in the game screen
                    if board.in_range(i, j):
                        square = board[i, j]
                    
                    # we are in the info screen
                    else:
                        pass

            self.update_info_screen()
            self.update_board_screen()

        pygame.quit()
        quit()

    """
    def clear_selected(self):
        self.B.clear_selected()
        self.selected_square = None

    def handle_click(self, pos):
        x, y = self.pixel2coordinate(pos)
        i, j = self.coordinate2index(x, y)
        
        # get piece from ChessBoard
        square = self.B.get_square(i, j)
        if self.verbose:
            print(f"Square: {square}")

        # if a piece is already selected
        if not self.selected_square is None:

            try:
                self.B.make_move(self.selected_square.index, square.index)
                if self.verbose:
                    print(f"move {self.selected_square} at {self.selected_square.index} to {square.index}")
                    is_in_check, no_legal_moves = self.B.get_king_state()
                    print(f"\t{self.B.to_move} in check? {is_in_check}")
                    print(f"\t{self.B.to_move} in stalemate? {no_legal_moves and (not is_in_check)}")
                    print(f"\t{self.B.to_move} in checkmate? {no_legal_moves and is_in_check}")
            except Exception as e:
                if self.verbose:
                    print(e)
            
            # in both cases (if the move succeeds or fails) we clear all previously selected pieces
            # This also handles the case where the person selected the same piece twice
            self.clear_selected()

        else:
            if square.is_empty():
                self.clear_selected()
            
            # TODO: add logic to check if the piece is the right color
            else:
                self.selected_square = square
                square.selected = True

                if square.piece.color == self.B.to_move:
                    for move in square.piece.legal_moves:
                        self.B.get_square(*move).legal_move = True
                            
                    if self.verbose:
                        print(f"\tLegal moves: {square.piece.legal_moves}")
        
        # redraw board to make move
        self.update_board()
    """

if __name__ == "__main__":

    import sys

    orientation = 'W'

    args = sys.argv[1:]
    if args != []:
        orientation = args[0]

    engine = ChessEngine(orientation, "lichess", verbose=False)
    engine.run()