import pygame
from pygame.locals import *

# set window size
size = width, height = (800, 600)
screen = pygame.display.set_mode(size)
black = (0,0,0)
white = (255,255,255)
screen.fill(white)


#load images
player = pygame.image.load("assets/player/blue_body_squircle.png")
player_loc = player.get_rect()
player_loc.center = width/2, height/2


# update the display to see what we set
pygame.display.update()


# Initialize the pygame code
pygame.init()
# Max frame rate
clock = pygame.time.Clock()
FPS = 60

leftkey = False
rightkey = False
upkey = False
downkey = False

speed = 10
# control variable
game_running = True


#game loop
while game_running:
    clock.tick(FPS)

    
    for event in pygame.event.get():
        if event.type == QUIT:
            game_running = False
            break
        
        if event.type==pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                game_running = False
                break
            if event.key in [K_s, K_DOWN]:
                downkey = True
            if event.key in [K_w, K_UP]:
                upkey = True
            if event.key in [K_d, K_RIGHT]:
                rightkey = True
            if event.key in [K_a, K_LEFT]:
                leftkey = True
            
        elif event.type==pygame.KEYUP:
            if event.key in [K_s, K_DOWN]:
                downkey = False
            if event.key in [K_w, K_UP]:
                upkey = False
            if event.key in [K_d, K_RIGHT]:
                rightkey = False
            if event.key in [K_a, K_LEFT]:
                leftkey = False




    x=0
    y=0
    if leftkey:
        x += -speed
    if rightkey:
        x += speed
    if upkey:
        y += -speed
    if downkey:
        y += speed

    player_loc = player_loc.move([x, y])

    #clear the display
    screen.fill(white)

    # place image on the screen
    screen.blit(player, player_loc)
    # apply changes
    pygame.display.update()



# quit the pygame window
pygame.quit()
#the app exits
