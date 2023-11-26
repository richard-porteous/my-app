import pygame
from pygame.locals import *



# set window size
size = width, height = (800, 600)
screen = pygame.display.set_mode(size)
black = (0,0,0)
white = (255,255,255)
screen.fill(white)
# update the display to see what we set
pygame.display.update()




# Initialize the pygame code
pygame.init()
# Max frame rate
clock = pygame.time.Clock()
FPS = 60

# control variable
game_running = True


#game loop
while game_running:
    clock.tick(FPS)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            game_running = False




# quit the pygame window
pygame.quit()
#the app exits
