import pygame
from evolve import *

# Colors (rgb)
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
yellow = (255,255,0)
blue = (0,0,255)

# Initializing display window
size = width, height = 800, 600
window = pygame.display.set_mode(size)
pygame.display.set_caption("Gravity")
window.fill(black)

# Initializing game clock
clock = pygame.time.Clock()

# Initialize game variables
length_scale = 500*10**5        # one pixel is 1,000,000 meters 
r_E = 10
s0 = [350, 200]
v0 = [-1,2]

s0 = [x * length_scale for x in s0]
v0 = [x * length_scale for x in v0]

# Drawing the Sun
pygame.draw.circle(window, yellow, (width//2, height//2), 20)
# Draw Earth
pygame.draw.circle(window, blue, (int(s0[0]/length_scale), int(s0[1]/length_scale)), r_E)
pygame.display.flip()

s = s0
v = v0
dt = 1
gameLoop = True
while gameLoop:
    
    for event in pygame.event.get():
        # So code stops when you click the red x to quit the game
        if event.type == pygame.QUIT:
            gameLoop = False
    
    [s, v] = evolve(s, v, [(width/2)*length_scale, (height/2)*length_scale], dt)

    window.fill(black)
    pygame.draw.circle(window, yellow, (width//2, height//2), 20)
    pygame.draw.circle(window, blue, (int(s[0]/length_scale), int(s[1]/length_scale)), r_E)
    pygame.display.flip()
    clock.tick(50)
