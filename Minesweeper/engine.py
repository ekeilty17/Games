from cell import MinesweeperCell
from grid import MinesweeperGrid
from colors import *
from game_tiles import *
from clock_numbers import *
from faces import *

import pygame

"""
Notation:
    - absolute_pos = absolute position on the PyGame screen
    - relative_pos = the position relative to some subsurface in PyGame
    - (pix_x, pix_y) = PyGame pixel value of screen
    - (x, y) =  MineSweeper pixel value (which are represented by PyGame rectangles)
    - (i, j) = indices of self.G.grid
"""

class MinesweeperEngine(object):

    # dimension (in pixels) of the cell of the Minesweeper grid
    PIXEL_WIDTH = PIXEL_HEIGHT = 2      # This can be adjusted to preference, it will just scale up the game
    CELL_WIDTH = CELL_HEIGHT = 16       # This cannot be adjusted because all of the bitmap assets assume this

    cell_bitmap = {
        "empty" : EMPTY,
        "hidden" : HIDDEN,
        "flagged": HIDDEN_WITH_FLAG,
        "question mark": HIDDEN_WITH_QUESTION_MARK,
        "number" : TILE_NUMBERS,
        "mine": MINE,
        "red mine": MINE_RED_BACKGROUND,
        "crossed out mine": MINE_CROSSED_OUT
    }


    """ Stage 1: Initialize Game """
    # initializes my Minesweeper backend and the PyGame front end
    def __init__(self, height, width, number_of_mines, verbose=True):
        self.verbose = verbose

        # Initializing Minesweeper backend
        self.G = MinesweeperGrid(height=height, width=width, number_of_mines=number_of_mines, verbose=self.verbose)

        # Initializing pygame front-end
        pygame.init()
        pygame.display.set_caption("Minesweeper")

        # The game will have 2 screens
        #                       +-----------------------------------+
        #     screen 1   -->    | <mines left>      :)      <timer> |
        #                       +-----------------------------------+
        #                       | +---+---+---+---+---+---+---+---+ |
        #                       | | * | * | 1 | 1 | * | * | 2 |   | |
        #     screen 2   -->    | +---+---+---+---+---+---+---+---+ |
        #                       | | 2 | 2 | 1 |   | 3 | * | 2 |   | |
        #                       | +---+---+---+---+---+---+---+---+ |
        #                       +-----------------------------------+
        # screen 1 is the information about the game, i.e. the timer and the number of mines left
        # screen 2 is the actual game
        
        self.initialize_screen_dimensions_and_locations()

        # Creating and drawing the screens that we need
        self.full_screen = pygame.display.set_mode((self.BUFFER + self.WIDTH + self.BUFFER, self.BUFFER + self.HEIGHT + self.BUFFER))
        self.info_screen = pygame.Surface((self.INFO_WIDTH, self.INFO_HEIGHT))
        self.game_screen = pygame.Surface((self.GAME_WIDTH, self.GAME_HEIGHT))
        
        # I have to store the position of the screens
        self.info_screen_topleft_position = (self.BUFFER + self.BORDER, self.BUFFER + self.BORDER)
        self.game_screen_topleft_position = (self.BUFFER + self.BORDER, self.BUFFER + self.BORDER + self.INFO_HEIGHT + self.BORDER)

        # Drawing the static elements in the `full_screen` which will not change
        self.draw_game_container()
        
        # drawing background to the info screen and game screen
        self.info_screen.fill(LIGHT_GREY)
        self.game_screen.fill(LIGHT_GREY)
        self.full_screen.blit(self.info_screen, self.info_screen_topleft_position)
        self.full_screen.blit(self.game_screen, self.game_screen_topleft_position)
        
        # Pushing the drawn elements to the screen
        pygame.display.flip()

        # Initializing game clock
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

        # a global state to keep track of what state of the game we are at
        self.game_state = "beginning"

    # Basically, this does a bunch of calculations to determine the dimensions of the various screens and locations of where things need to go
    # for example, where the face, timer, and mine counter need to go
    def initialize_screen_dimensions_and_locations(self):
        # screen dimensions
        self.INFO_WIDTH = self.G.WIDTH * self.CELL_WIDTH * self.PIXEL_WIDTH
        self.INFO_HEIGHT = 2 * self.CELL_HEIGHT * self.PIXEL_HEIGHT

        self.GAME_WIDTH = self.G.WIDTH * self.CELL_WIDTH * self.PIXEL_WIDTH
        self.GAME_HEIGHT = self.G.HEIGHT * self.CELL_HEIGHT * self.PIXEL_HEIGHT

        self.BUFFER = self.PIXEL_WIDTH
        self.BORDER = 10 * self.PIXEL_WIDTH

        self.WIDTH = self.BORDER + self.GAME_WIDTH + self.BORDER
        self.HEIGHT = self.BORDER + self.INFO_HEIGHT + self.BORDER + self.GAME_HEIGHT + self.BORDER

        # face rectangle location
        # Note: This is very dependent on the fact that self.CELL_WIDTH = self.CELL_HEIGHT = 16
        #       And that the info_screen is 2 pixels in height
        self.face_index = (8/32, (self.G.WIDTH-1)/2 - 6/24)
        self.mine_counter_index = (9/32, 9/32)
        self.timer_index = (9/32, self.G.WIDTH - (13*3)/16 - 9/32)
    
    # The purpose of this function is to be called once and then we never have to redraw these parts again
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
        top_bevel1 = pygame.draw.rect(self.full_screen, GREY, (self.BUFFER+self.BORDER-2*self.PIXEL_WIDTH, self.BUFFER+self.BORDER-2*self.PIXEL_HEIGHT, self.INFO_WIDTH+3*self.PIXEL_WIDTH, self.PIXEL_HEIGHT))
        top_bevel2 = pygame.draw.rect(self.full_screen, GREY, (self.BUFFER+self.BORDER-2*self.PIXEL_WIDTH, self.BUFFER+self.BORDER-self.PIXEL_HEIGHT, self.INFO_WIDTH+2*self.PIXEL_WIDTH, self.PIXEL_HEIGHT))

        left_bevel1 = pygame.draw.rect(self.full_screen, GREY, (self.BUFFER+self.BORDER-2*self.PIXEL_WIDTH, self.BUFFER+self.BORDER-2*self.PIXEL_HEIGHT, self.PIXEL_WIDTH, self.INFO_HEIGHT+3*self.PIXEL_HEIGHT))
        left_bevel2 = pygame.draw.rect(self.full_screen, GREY, (self.BUFFER+self.BORDER-self.PIXEL_WIDTH, self.BUFFER+self.BORDER-2*self.PIXEL_HEIGHT, self.PIXEL_WIDTH, self.INFO_HEIGHT+2*self.PIXEL_HEIGHT))

        bottom_bevel1 = pygame.draw.rect(self.full_screen, WHITE, (self.BUFFER+self.BORDER, self.BUFFER+self.BORDER+self.INFO_HEIGHT, self.INFO_WIDTH+2*self.PIXEL_WIDTH, self.PIXEL_HEIGHT))
        bottom_bevel2 = pygame.draw.rect(self.full_screen, WHITE, (self.BUFFER+self.BORDER-self.PIXEL_WIDTH, self.BUFFER+self.BORDER+self.INFO_HEIGHT+self.PIXEL_HEIGHT, self.INFO_WIDTH+3*self.PIXEL_WIDTH, self.PIXEL_HEIGHT))

        right_bevel1 = pygame.draw.rect(self.full_screen, WHITE, (self.BUFFER+self.BORDER+self.INFO_WIDTH, self.BUFFER+self.BORDER, self.PIXEL_WIDTH, self.INFO_HEIGHT+2*self.PIXEL_HEIGHT))
        right_bevel2 = pygame.draw.rect(self.full_screen, WHITE, (self.BUFFER+self.BORDER+self.INFO_WIDTH+self.PIXEL_WIDTH, self.BUFFER+self.BORDER-self.PIXEL_HEIGHT, self.PIXEL_WIDTH, self.INFO_HEIGHT+3*self.PIXEL_HEIGHT))

        # Adding beveled edges to game screen (screen 2)
        top_bevel1 = pygame.draw.rect(self.full_screen, GREY, (self.BUFFER+self.BORDER-2*self.PIXEL_WIDTH, self.BUFFER+2*self.BORDER+self.INFO_HEIGHT-2*self.PIXEL_HEIGHT, self.GAME_WIDTH+3*self.PIXEL_WIDTH, self.PIXEL_HEIGHT))
        top_bevel2 = pygame.draw.rect(self.full_screen, GREY, (self.BUFFER+self.BORDER-2*self.PIXEL_WIDTH, self.BUFFER+2*self.BORDER+self.INFO_HEIGHT-self.PIXEL_HEIGHT, self.GAME_WIDTH+2*self.PIXEL_WIDTH, self.PIXEL_HEIGHT))

        left_bevel1 = pygame.draw.rect(self.full_screen, GREY, (self.BUFFER+self.BORDER-2*self.PIXEL_WIDTH, self.BUFFER+2*self.BORDER+self.INFO_HEIGHT-2*self.PIXEL_HEIGHT, self.PIXEL_WIDTH, self.GAME_HEIGHT+3*self.PIXEL_HEIGHT))
        left_bevel2 = pygame.draw.rect(self.full_screen, GREY, (self.BUFFER+self.BORDER-self.PIXEL_WIDTH, self.BUFFER+2*self.BORDER+self.INFO_HEIGHT-2*self.PIXEL_HEIGHT, self.PIXEL_WIDTH, self.GAME_HEIGHT+2*self.PIXEL_HEIGHT))

        bottom_bevel1 = pygame.draw.rect(self.full_screen, WHITE, (self.BUFFER+self.BORDER, self.BUFFER+2*self.BORDER+self.INFO_HEIGHT+self.GAME_HEIGHT, self.GAME_WIDTH+2*self.PIXEL_WIDTH, self.PIXEL_HEIGHT))
        bottom_bevel2 = pygame.draw.rect(self.full_screen, WHITE, (self.BUFFER+self.BORDER-self.PIXEL_WIDTH, self.BUFFER+2*self.BORDER+self.INFO_HEIGHT+self.GAME_HEIGHT+self.PIXEL_HEIGHT, self.GAME_WIDTH+3*self.PIXEL_WIDTH, self.PIXEL_HEIGHT))

        right_bevel1 = pygame.draw.rect(self.full_screen, WHITE, (self.BUFFER+self.BORDER+self.GAME_WIDTH, self.BUFFER+2*self.BORDER+self.INFO_HEIGHT, self.PIXEL_WIDTH, self.GAME_HEIGHT+2*self.PIXEL_HEIGHT))
        right_bevel2 = pygame.draw.rect(self.full_screen, WHITE, (self.BUFFER+self.BORDER+self.GAME_WIDTH+self.PIXEL_WIDTH, self.BUFFER+2*self.BORDER+self.INFO_HEIGHT-self.PIXEL_HEIGHT, self.PIXEL_WIDTH, self.GAME_HEIGHT+3*self.PIXEL_HEIGHT))

        # drawing to screen
        pygame.display.flip()

    # for starting or restarting the game
    def initialize_game(self, first_click_index=None):
        
        # resetting grid
        self.G.initialize_grid(first_click_index=first_click_index)
        self.face_pixels = HAPPY_FACE

        # In PyGame, event.button == 2 is supposed to mean a middle click (both left and right click at the same time)
        # but it doesn't actually work, so we have to implement middle clicks manually
        self.left_mouse_down = self.right_mouse_down = False

        # these variables just help preformance in the `self.update_info_screen()` function
        self.previous_mine_count = 0
        self.previous_time = -1
        self.start_time = pygame.time.get_ticks()

        # allows us to highlight cells when a user clicks down on them
        self.previous_selected_cell_indices = set()
        self.selected_cell_indices = set()

        # Initializing board display
        self.update_info_screen()
        self.update_game_screen()
        pygame.display.flip()


    """ State 2: Get input from user and preform the correct action """
    # The possible actions are "nothing", "left down", "middle down", "rigth down", "left click", "middle click", and "right click" 
    def get_user_action_from_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:               # 1 = left click
                self.left_mouse_down = True
            if event.button == 3:               # 3 = right click
                self.right_mouse_down = True

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            # Middle Click Down while moving: changes the cells you are highlighting
            if self.left_mouse_down and self.right_mouse_down:
                return "middle down"
            # Left Click Down while moving: changes the cells you are highlighting
            if self.left_mouse_down:
                return "left down"
            # Right Click Down while moving: still does nothing
            if self.right_mouse_down:
                return "right down"

        if event.type == pygame.MOUSEBUTTONUP:
            # If either button is released, it is a Middle Click
            if self.left_mouse_down and self.right_mouse_down:
                if event.button == 1:               # 1 = left click
                    self.left_mouse_down = False
                if event.button == 3:               # 3 = right click
                    self.right_mouse_down = False
                return "middle click"
            
            # Left and Right Clicks are straight forward
            if self.left_mouse_down:
                if event.button == 1:               # 1 = left click
                    self.left_mouse_down = False
                    return "left click"
            
            if self.right_mouse_down:
                if event.button == 3:               # 3 = right click
                    self.right_mouse_down = False
                    return "right click"
        
        return "nothing"

    # bunch of functions to calculate where exactly the user clicked
    def absolute2relative(self, absolute_pos, topleft_position):
        absolute_pix_x, absolute_pix_y = absolute_pos
        dx, dy = topleft_position
        return absolute_pix_x - dx, absolute_pix_y - dy
    def pixel2index(self, pos):
        pix_x, pix_y = pos
        i = pix_y // (self.PIXEL_HEIGHT * self.CELL_HEIGHT)
        j = pix_x // (self.PIXEL_WIDTH * self.CELL_WIDTH)
        return i, j
    def is_click_on_face(self, pos):
        pix_x, pix_y = pos
        face_width = 24 * self.PIXEL_WIDTH      # TODO: the fact the face is 24x24 is hardcoded, could make it more general
        face_height = 24 * self.PIXEL_HEIGHT
        return abs(pix_x - self.INFO_WIDTH/2) < face_width/2 and abs(pix_y - self.INFO_HEIGHT/2) < face_height/2
    def get_idle_face(self):
        if self.game_state == "win":
            return COOL_FACE
        elif self.game_state == "lose":
            return SAD_FACE
        else:
            return HAPPY_FACE
    def is_game_over(self):
        return self.game_state in ["win", "lose"]

    def handle_user_action_on_info_screen(self, absolute_pos, user_action):
        info_pos = self.absolute2relative(absolute_pos, self.info_screen_topleft_position)
        if self.is_click_on_face(info_pos):
            if user_action == "left down":
                self.face_pixels = SELECTED_FACE
            elif user_action == "left click":
                self.initialize_game()
                self.game_state = "beginning"
                self.face_pixels = self.get_idle_face()

    def handle_user_action_on_game_screen(self, absolute_pos, user_action):
        game_pos = self.absolute2relative(absolute_pos, self.game_screen_topleft_position)
        i, j = self.pixel2index(game_pos)

        if user_action == "left down":
            self.selected_cell_indices = [(i, j)]
            self.face_pixels = WOW_FACE
        elif user_action == "middle down":
            self.selected_cell_indices = self.G.get_neighbor_indices(i, j, include_self=True)
            self.face_pixels = WOW_FACE
        elif user_action == "right down":
            self.face_pixels = WOW_FACE
        
        elif user_action == "left click":
            # make sure the first click is on a square with a mine-count of 0
            if self.game_state == "beginning":
                self.initialize_game(first_click_index=(i, j))
                self.game_state = "playing"
            self.G.left_click(i, j)
            self.face_pixels = self.get_idle_face()
        elif user_action == "middle click":
            self.G.middle_click(i, j)
            self.face_pixels = self.get_idle_face()
        elif user_action == "right click":
            self.G.right_click(i, j)
            self.face_pixels = self.get_idle_face()
    
    def handle_end_of_game_check(self):
        # check if user lost
        if len(self.G.get_exposed_mines()) > 0:
            self.game_state = "lose"
            self.face_pixels = SAD_FACE
            if self.verbose:
                print("Kaboom!")

        # check if the user won
        if len(self.G.visible_cell_indices) == len(self.G.no_mine_indices):
            self.game_state = "win"
            self.face_pixels = COOL_FACE
            if self.verbose:
                print("You Win!")

        # update all cells to win or lose state
        if self.is_game_over():
            for i in range(self.G.HEIGHT):
                for j in range(self.G.WIDTH):
                    cell = self.G.get_cell(i, j)
                    cell.action(self.game_state)

                    # TODO: I would rather self.G handle this internally, but I'm too lazy to figure out the best way to do that rn
                    # I need to do this so the flag count display changes
                    self.G.number_of_flags += (cell.current_state == "flagged") - (cell.previous_state == "flagged")
        
            # If the game is over, we need to update again since the cells have changed state
            self.update_info_screen()
            self.update_game_screen()
            pygame.display.flip()


    """ State 3: Draw the updated state to the screen as effeiciently as possible """
    # some helper functions for `self.update_info_screen()`
    @staticmethod
    def concatenate_bitmaps(*digits):
        if len(digits) == 0:
            return []
        
        bitmap = [[] for _ in range(len(digits[0]))]
        for next_bitmap in digits:
            for i in range(len(next_bitmap)):
                bitmap[i].extend(list(next_bitmap[i]))
        return bitmap
    @staticmethod
    def number_to_bitmap(n, d=3):
        # this just makes sure we can display the number with 3 digits
        n = max(1-10**(d-1), n)
        n = min(n, 10**(d)-1)
        
        digits = []
        for c in str(n).zfill(3).rjust(3, " "):
            if c == " ":
                digits.append(CLOCK_EMPTY)
            elif c == "-":
                digits.append(CLOCK_NEGATIVE)
            else:
                digits.append( CLOCK_NUMBERS[int(c)] )
        return MinesweeperEngine.concatenate_bitmaps(*digits)

    # some helper functions for `self.update_game_screen()`
    def get_cell_pixels(self, cell):
        cell_pixels = self.cell_bitmap[cell.current_state] 
        if cell.current_state == "number":
            cell_pixels = cell_pixels[cell.count]
        return cell_pixels
    def draw_cell_pixels(self, i, j, cell_pixels):
        # drawing the updated state change
        for x in range(self.CELL_HEIGHT):
            for y in range(self.CELL_WIDTH):
                pygame.draw.rect(self.game_screen, COLORS[cell_pixels[x][y]], self.get_pixel_rectangle(x, y, i, j))

    # The true pixels in PyGame are smaller than the "pixels" used by my MineSweeper game
    # This gets the PyGame rectangle that represents a "pixel" in my game
    def get_pixel_rectangle(self, x, y, i, j):
        x_absolute = self.CELL_WIDTH * i + x
        y_absolute = self.CELL_HEIGHT * j + y
        return (self.PIXEL_WIDTH * y_absolute, self.PIXEL_HEIGHT * x_absolute, self.PIXEL_WIDTH, self.PIXEL_HEIGHT)

    # This is what is redrawn to the info screen every frame
    def update_info_screen(self):

        # Adding smiley face
        for x in range(len(self.face_pixels)):
            for y in range(len(self.face_pixels[x])):
                pygame.draw.rect(self.info_screen, COLORS[self.face_pixels[x][y]], self.get_pixel_rectangle(x, y, *self.face_index))


        # getting mine count
        mines_remaining = self.G.NUMBER_OF_MINES - self.G.number_of_flags
        
        if self.previous_mine_count != mines_remaining:
            mine_counter_pixels = self.number_to_bitmap(mines_remaining)
            for x in range(len(mine_counter_pixels)):
                for y in range(len(mine_counter_pixels[x])):
                    pygame.draw.rect(self.info_screen, COLORS[mine_counter_pixels[x][y]], self.get_pixel_rectangle(x, y, *self.mine_counter_index))
            
            self.previous_mine_count = mines_remaining

        # getting time
        time_elapsed_in_milliseconds = pygame.time.get_ticks() - self.start_time
        time_elapsed_in_seconds = time_elapsed_in_milliseconds // 1000
        
        # if the game is at the beginning, the time is frozen at 0
        if self.game_state == "beginning":
            time_elapsed_in_seconds = 0

        # if the game is over, we want to freeze the timer
        if not self.is_game_over():
            if self.previous_time != time_elapsed_in_seconds:
                time_pixels = self.number_to_bitmap(time_elapsed_in_seconds)
                for x in range(len(time_pixels)):
                    for y in range(len(time_pixels[x])):
                        pygame.draw.rect(self.info_screen, COLORS[time_pixels[x][y]], self.get_pixel_rectangle(x, y, *self.timer_index))
                
                self.previous_time = time_elapsed_in_seconds

        self.full_screen.blit(self.info_screen, self.info_screen_topleft_position)

    # This is what is redrawn to the game screen every frame
    def update_game_screen(self):
        for i in range(self.G.HEIGHT):
            for j in range(self.G.WIDTH):
                cell = self.G.get_cell(i, j)

                # get display of cell given its state
                cell_pixels = self.get_cell_pixels(cell)
                
                # this solves an edge case at the beginning of the game where we need the engine to draw every cell once and then not redraw it again
                # note that if this elif block is True, then the next elif block does not get executed
                if cell.previous_state == None:
                    cell.previous_state = "hidden"
                # otherwise, we check if the state hasn't changed, and if not we continue because we don't wnat to redraw it
                elif not cell.state_changed():
                    continue
                
                # drawing cell
                self.draw_cell_pixels(i, j, cell_pixels)

        # unselect any cells in self.previous_selected_cell_indices
        for i, j in self.previous_selected_cell_indices:
            cell = self.G.get_cell(i, j)
            cell_pixels = self.get_cell_pixels(cell)
            self.draw_cell_pixels(i, j, cell_pixels)

        self.previous_selected_cell_indices = set()

        # any select any selected cells
        for i, j in self.selected_cell_indices:
            cell = self.G.get_cell(i, j)
            cell_pixels = self.cell_bitmap["empty"] if cell.current_state == "hidden" else self.get_cell_pixels(cell)
            self.draw_cell_pixels(i, j, cell_pixels)

        # Updating board
        self.full_screen.blit(self.game_screen, self.game_screen_topleft_position)

    
    """ Stage 4: String all previous stages together """
    def run(self):
        
        # start game
        self.initialize_game()
        self.game_state = "beginning"

        # Main game loop
        running = True
        while running:

            for event in pygame.event.get():
                # So code stops when you click the red x to quit the game
                if event.type == pygame.QUIT:
                    running = False

                # make sure all selections get cleared by defaut
                self.previous_selected_cell_indices = self.previous_selected_cell_indices.union( self.selected_cell_indices )
                self.selected_cell_indices = set()

                # obtaining the input fron the user
                # if there is no input then we just continue to avoid needless computation
                user_action = self.get_user_action_from_event(event)
                if user_action == "nothing":
                    # Adding the idle face face expression
                    self.face_pixels = self.get_idle_face()
                    continue

                # Since we are here, the user clicked somewhere, we need to figure out where
                # get the cell that was clicked on
                absolute_pos = pygame.mouse.get_pos()
                info_screen_rect = self.info_screen.get_rect(topleft=self.info_screen_topleft_position)
                game_screen_rect = self.game_screen.get_rect(topleft=self.game_screen_topleft_position)

                # user clicked on info screen
                if info_screen_rect.collidepoint(absolute_pos):
                    self.handle_user_action_on_info_screen(absolute_pos, user_action)
                
                # user clicked on game screen
                elif game_screen_rect.collidepoint(absolute_pos):
                    if not self.is_game_over():
                        self.handle_user_action_on_game_screen(absolute_pos, user_action)
                
            # update game with changes
            self.update_info_screen()
            self.update_game_screen()
            pygame.display.flip()

            # If the game is already over, we don't need to check if the user won
            # It's important we do this after we first update the bored with the user's action
            if not self.is_game_over():
                self.handle_end_of_game_check()

        pygame.quit()
        quit()


if __name__ == "__main__":
    beginner = {"height": 9, "width": 9, "number_of_mines": 10}
    intermediate = {"height": 16, "width": 16, "number_of_mines": 40}
    expert = {"height": 16, "width": 30, "number_of_mines": 99}

    engine = MinesweeperEngine(verbose=True, **expert)
    engine.run()