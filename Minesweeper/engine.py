from cell import MinesweeperCell
from grid import MinesweeperGrid
from pixel_art import *
import pygame

"""
Notation:
    - pos = (pix_x, pix_y) = pixel value of screen
    - (x, y) = game pixels
    - index = (i, j) = indices of self.G.grid
"""

class MinesweeperEngine(object):

    # dimension (in pixels) of the cell of the Minesweeper grid
    PIXEL_WIDTH = PIXEL_HEIGHT = 5
    CELL_WIDTH = CELL_HEIGHT = 4
    MARGIN = 0

    # Game Speed: frames per second
    FPS = 30

    def __init__(self, height, width, number_of_mines, verbose=True):
        self.verbose = verbose

        # Initializing Minesweeper backend
        self.G = MinesweeperGrid(height=height, width=width, number_of_mines=number_of_mines, verbose=self.verbose)

        # Initializing pygame front-end
        pygame.init()
        pygame.display.set_caption("Minesweeper")

        # The game will have 2 screens
        #       +-------------------------+
        #       |        screen 1         |
        #       +-------------------------+
        #       |                         |
        #       |        screen 2         |
        #       |                         |
        #       +-------------------------+
        #
        # screen 1 is the information about the game, i.e. the timer and the number of mines left
        # screen 2 is the actual game

        # Calculating the screen dimensions (in pixels)
        self.INFO_WIDTH = self.G.WIDTH * self.CELL_WIDTH * self.PIXEL_WIDTH
        self.INFO_HEIGHT = 2 * self.CELL_HEIGHT * self.PIXEL_HEIGHT

        self.GAME_WIDTH = self.G.WIDTH * self.CELL_WIDTH * self.PIXEL_WIDTH
        self.GAME_HEIGHT = self.G.HEIGHT * self.CELL_HEIGHT * self.PIXEL_HEIGHT

        self.BUFFER = self.PIXEL_WIDTH
        self.BORDER = 10 * self.PIXEL_WIDTH

        self.WIDTH = self.BORDER + self.GAME_WIDTH + self.BORDER
        self.HEIGHT = self.BORDER + self.INFO_HEIGHT + self.BORDER + self.GAME_HEIGHT + self.BORDER
        
        # Creating and drawing the screens that we need
        self.full_screen = pygame.display.set_mode((self.BUFFER + self.WIDTH + self.BUFFER, self.BUFFER + self.HEIGHT + self.BUFFER))
        self.info_screen = pygame.Surface((self.INFO_WIDTH, self.INFO_HEIGHT))
        self.game_screen = pygame.Surface((self.GAME_WIDTH, self.GAME_HEIGHT))

        # Drawing the static elements in the `full_screen` which will not change
        self.draw_game_container()
        
        self.info_screen.fill(RED)
        self.game_screen.fill(GREEN)
        self.full_screen.blit(self.info_screen, (self.BUFFER + self.BORDER, self.BUFFER + self.BORDER))
        self.full_screen.blit(self.game_screen, (self.BUFFER + self.BORDER, self.BUFFER + self.BORDER + self.INFO_HEIGHT + self.BORDER))
        
        # Pushing the drawn elements to the screen
        pygame.display.flip()

        # Initializing game clock
        clock = pygame.time.Clock()

    def run(self):
        
        # Initializing board display
        self.update_grid()

        running = True
        selected_piece = None
        while running:
            for event in pygame.event.get():
                # So code stops when you click the red x to quit the game
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    """
                    pos = pygame.mouse.get_pos()
                    i, j = self.pixel2index(pos)

                    if event.button == 1:               # 1 = left click
                        self.handle_left_click(i, j)
                    elif event.button == 2:             # 2 = middle click
                        self.handle_middle_click(i, j)
                    elif event.button == 3:             # 3 = right click
                        self.handle_right_click(i, j)
                    else:
                        pass
                        # 4 = scroll up
                        # 5 = scroll down
                    """
                    pass
                
                elif event.type == pygame.KEYDOWN:
                    pass
                

        pygame.quit()
        quit()

    def draw_game_container(self):
        
        # Makes the buffer zone black
        self.full_screen.fill(BLACK)

        # Makes the full screen LIGHT_GREY
        pygame.draw.rect(self.full_screen, LIGHT_GREY, (self.BUFFER, self.BUFFER, self.WIDTH, self.HEIGHT))

        # Adding beveled edges to the full screen
        top_bevel1 = pygame.draw.rect(self.full_screen, WHITE, (self.BUFFER, self.BUFFER, self.WIDTH-self.PIXEL_WIDTH, self.PIXEL_HEIGHT))
        top_bevel2 = pygame.draw.rect(self.full_screen, WHITE, (self.BUFFER, self.BUFFER+self.PIXEL_HEIGHT, self.WIDTH-2*self.PIXEL_WIDTH, self.PIXEL_HEIGHT))

        left_bevel1 = pygame.draw.rect(self.full_screen, WHITE, (self.BUFFER, self.BUFFER, self.PIXEL_WIDTH, self.HEIGHT-self.PIXEL_HEIGHT))
        left_bevel2 = pygame.draw.rect(self.full_screen, WHITE, (self.BUFFER+self.PIXEL_WIDTH, self.BUFFER, self.PIXEL_WIDTH, self.HEIGHT-2*self.PIXEL_HEIGHT))

        bottom_bevel1 = pygame.draw.rect(self.full_screen, GREY, (self.BUFFER+self.PIXEL_WIDTH, self.BUFFER+self.HEIGHT-self.PIXEL_HEIGHT, self.WIDTH-self.PIXEL_WIDTH, self.PIXEL_HEIGHT))
        bottom_bevel2 = pygame.draw.rect(self.full_screen, GREY, (self.BUFFER+2*self.PIXEL_WIDTH, self.BUFFER+self.HEIGHT-2*self.PIXEL_HEIGHT, self.WIDTH-2*self.PIXEL_WIDTH, self.PIXEL_HEIGHT))

        right_bevel1 = pygame.draw.rect(self.full_screen, GREY, (self.BUFFER+self.WIDTH-self.PIXEL_WIDTH, self.BUFFER+self.PIXEL_HEIGHT, self.PIXEL_WIDTH, self.HEIGHT-self.PIXEL_HEIGHT))
        right_bevel2 = pygame.draw.rect(self.full_screen, GREY, (self.BUFFER+self.WIDTH-2*self.PIXEL_WIDTH, self.BUFFER+2*self.PIXEL_HEIGHT, self.PIXEL_WIDTH, self.HEIGHT-2*self.PIXEL_HEIGHT))


        # Adding beveled edges to info screen (screen 1)
        top_bevel1 = pygame.draw.rect(self.full_screen, GREY, (self.BUFFER+self.BORDER-2*self.PIXEL_HEIGHT, self.BUFFER, self.WIDTH-self.PIXEL_WIDTH, self.PIXEL_HEIGHT))

        pygame.display.flip()









    # complicated function to create a grid we can easily index
    def get_square(self, i, j):
        return (    (self.SQUARE_WIDTH + self.MARGIN) * i + self.MARGIN, 
                    (self.SQUARE_HEIGHT + self.MARGIN) * j + self.MARGIN, 
                    self.SQUARE_WIDTH,
                    self.SQUARE_HEIGHT
        )

    def update_grid(self):
        
        
        
        for i in range(self.G.HEIGHT):
            for j in range(self.G.WIDTH):
                cell = self.G.get_cell(i, j)

                #square_pos = self.get_square(i, j)
                #pygame.draw.rect(self.game_screen, LIGHT_GREY, square_pos)
                
                """
                if cell.is_visible():
                    # background of grid
                    square_pos = self.get_square(i, j)
                    pygame.draw.rect(self.screen, LIGHT_GREY, square_pos)

                    if cell.contains_mine():
                        # TODO: draw mine (probably as a circle for now)
                        pass
                    else:
                        # TODO: write number
                        pass
                else:
                    if cell.is_flagged():
                        # TODO: mark cell with flag (probably just make it red in color for now)
                        pass
                    else:
                        # TODO: draw default cell
                        pass
                """
                

        # Updating board
        pygame.display.flip()

        """
        # drawing light and dark squares
        # we start with that the a1 square is dark, and generate the rest of the grid from that
        color = self.DARK
        for i in range(self.G.HEIGHT):
            for j in range(self.G.WIDTH):
                x, y = self.index2coordinate(i, j)
                square_pos = self.get_square(x, y)
                pygame.draw.rect(self.screen, color, square_pos)
                color = self.DARK if color == self.LIGHT else self.LIGHT
            color = self.DARK if color == self.LIGHT else self.LIGHT

        # Adding pieces based on board state
        pieces = []
        for i in range(self.B.HEIGHT):
            for j in range(self.B.WIDTH):
                # needed for various things
                x, y = self.index2coordinate(i, j)
                square_pos = self.get_square(x, y)
                square_center = (square_pos[0] + self.SQUARE_WIDTH//2, square_pos[1] + self.SQUARE_HEIGHT//2)

                # get square from ChessBoard
                square = self.B[i, j]

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
                piece.img = pygame.image.load(f"assets2/{piece.color}-{piece.name.title()}.png")
                piece.img.convert()    # optimizes image file to make drawing faster
                piece.img = pygame.transform.scale(piece.img, (self.SQUARE_WIDTH-self.MARGIN-5, self.SQUARE_HEIGHT-self.MARGIN-5))
                
                # get rectangle the image occupies
                piece.rect = piece.img.get_rect()

                # set the piece's location to where the ChessBoard says it should go
                piece.rect.center = square_center
                
                # draw piece
                self.screen.blit(piece.img, piece.rect)
                
                # add image and rectangle to list so we can access them later
                pieces.append( piece )

        # Updating board
        pygame.display.flip()

        # TODO: Check if keeping track of the pieces is necessary
        pieces = []
        return pieces
        """

    def pixel2index(self, pos):
        pix_i, pix_j = pos

        i = pix_i // (self.SQUARE_WIDTH + self.MARGIN)
        j = pix_j // (self.SQUARE_HEIGHT + self.MARGIN)

        if self.verbose:
            print(f"Click: {pos}  \tGrid index: {(i, j)}")
        return i, j
    
    """
    def coordinate2index(self, x, y):
        i, j = y, x             # notice we just swap x and y to get the index

        if self.orientation == 'W':
            i = (self.B.HEIGHT-1) - i
        else:
            j = (self.B.WIDTH-1) - j

        if self.verbose:
            print(f"Matrix index: {(i, j)}\tChess: {''.join(self.index2chess(i, j))}", end="\t")
        return i, j
    
    def index2coordinate(self, i, j):
        if self.orientation == 'W':
            i = (self.B.HEIGHT-1) - i
        else:
            j = (self.B.WIDTH-1) - j
        
        x, y = j, i             # notice we just swap i and j to get the coordiate
        return x, y

    def index2chess(self, i, j):
        return self.B.index2chess(i, j)
    
    def chess2index(self, letter, num):
        return self.B.chess2index(letter, num)

    def clear_selected(self):
        self.B.clear_selected()
        self.selected_square = None
    """

    def handle_left_click(self, i, j):
        pass
    
    def handle_middle_click(self, i, j):
        pass
    
    def handle_right_click(self, i, j):
        pass
    
    """
    def handle_click(self, pos):
        x, y = self.pixel2coordinate(pos)
        i, j = self.coordinate2index(x, y)
        
        # get piece from ChessBoard
        square = self.B[i, j]
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
                        self.B[move].legal_move = True
                            
                    if self.verbose:
                        print(f"\tLegal moves: {square.piece.legal_moves}")
        
        # redraw board to make move
        self.draw_board()
    """

if __name__ == "__main__":
    beginner = {"height": 9, "width": 9, "number_of_mines": 10}
    intermediate = {"height": 16, "width": 16, "number_of_mines": 40}
    expert = {"height": 16, "width": 30, "number_of_mines": 99}

    engine = MinesweeperEngine(**beginner)
    engine.run()