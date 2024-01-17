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

class keyisdown():
   
    def __init__(self) -> None:
        self.leftkey = False
        self.rightkey = False
        self.upkey = False
        self.downkey = False
    def getEvents(self):
       
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
           
            if event.type==pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                if event.key in [K_s, K_DOWN]:
                    self.downkey = True
                if event.key in [K_w, K_UP]:
                    self.upkey = True
                if event.key in [K_d, K_RIGHT]:
                    self.rightkey = True
                if event.key in [K_a, K_LEFT]:
                    self.leftkey = True
               
            elif event.type==pygame.KEYUP:
                if event.key in [K_s, K_DOWN]:
                    self.downkey = False
                if event.key in [K_w, K_UP]:
                    self.upkey = False
                if event.key in [K_d, K_RIGHT]:
                    self.rightkey = False
                if event.key in [K_a, K_LEFT]:
                    self.leftkey = False
        return True

held_keys = keyisdown()
speed = 10
# control variable
game_running = True


#game loop
while game_running:
    clock.tick(FPS)

    game_running = held_keys.getEvents()
    x=0
    y=0
    if held_keys.leftkey:
        x += -speed
    if held_keys.rightkey:
        x += speed
    if held_keys.upkey:
        y += -speed
    if held_keys.downkey:
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
