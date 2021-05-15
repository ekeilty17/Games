import pygame
from snake import *
from random import randint

import time

pygame.init()

# Creating display window
size = width, height = 800, 600
window = pygame.display.set_mode(size)
pygame.display.set_caption("Snake")

# Colors (rgb)
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)

cell_size = 20

# Initializing display window
window.fill(black)
pygame.draw.rect(window, red, (0, 0, cell_size, cell_size))
pygame.display.flip()

# Initializing game clock
clock = pygame.time.Clock()

# Initialize Snake
S = snake([0, 0], cell_size, width, height)

# Initialize game variables
direction = [1, 0]
food = [randint(0, (width/cell_size)-1) * cell_size, randint(0,(height/cell_size)-1) * cell_size]
gameLoop = True

while gameLoop:
    for event in pygame.event.get():
        # So code stops when you click the red x to quit the game
        if event.type == pygame.QUIT:
            gameLoop = False
        
        # Getting keyboard input and updating position
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = [-1, 0]

            if event.key == pygame.K_RIGHT:
                direction = [1, 0]

            if event.key == pygame.K_DOWN:
                direction = [0, 1]

            if event.key == pygame.K_UP:
                direction = [0, -1]
    
    # updating move
    removed = S.evolve(direction)

    # Re-drawing diplay
    window.fill(black) 
    #   Food
    pygame.draw.rect(window, white, (food[0], food[1], cell_size, cell_size))
    #   Snake
    for i in range(len(S.body.store)):
        if i == len(S.body.store)-1:
            pygame.draw.rect(window, green, (S.body.store[i][0], S.body.store[i][1], cell_size, cell_size))
        else:
            pygame.draw.rect(window, red, (S.body.store[i][0], S.body.store[i][1], cell_size, cell_size))
        
    # Updating board
    pygame.display.flip()

    # Refresh speed
    clock.tick(10)

    # handling is snake crashes into itself
    if S.body.getHead() in S.body.store[:-1]:
        gameLoop = False

    # handling when snake eats food
    if S.body.store[-1] == food:
        S.eat(food)
        food = [randint(0, (width/cell_size)-1) * cell_size, randint(0,(height/cell_size)-1) * cell_size]

