import math
import random
import pygame
from pygame.locals import *


SCALESIZE = 0.5
TILE_SIZE = (80,80)
TILESIZE = (TILE_SIZE[0] * SCALESIZE, TILE_SIZE[1] * SCALESIZE)


PLAYERNORMALSPEED = 0.4 * SCALESIZE

# set window size
size = width, height = (800, 560)
screen = pygame.display.set_mode(size)

black = (0,0,0)
white = (255,255,255)
#screen.fill(white)

#background
background = pygame.Surface.copy(screen)
background.fill(white)

for y in range(0, height, int(TILESIZE[0])):
    pygame.draw.line(background, black, (0,y), (width,y))
for x in range(0, width, int(TILESIZE[1])):
    pygame.draw.line(background, black, (x,0), (x,height))

#player
player = pygame.image.load("assets/player/blue_body_squircle.png")
player = pygame.transform.scale_by(player, 0.5 )
player_loc = player.get_rect()
player_loc.center = TILESIZE[0]/2, TILESIZE[1]/2

#food
eaten = False
food = pygame.image.load("assets/food/tile_coin.png")
food = pygame.transform.scale_by(food, 0.5 )
food_loc = food.get_rect()
food_loc.center = (TILESIZE[0] * 9 + TILESIZE[0]/2) , (TILESIZE[1] * 9 + TILESIZE[1]/2)

screen.blit(background,(0,0))

# update the display to see what we set
pygame.display.update()

# Initialize the pygame code
pygame.init()
# Max frame rate
clock = pygame.time.Clock()
FPS = 60

#speed = 10
# control variable
game_running = True

# time based movement requires delta time
class deltatime():
    def __init__(self):
        self.last_loop = pygame.time.get_ticks()
        self.dt = 0


    def loop_time(self) -> int:
        time_now_ms = pygame.time.get_ticks()
        dt = time_now_ms - self.last_loop
        self.last_loop = time_now_ms
        return dt
    

class keyisdown():
    
    def __init__(self) -> None:
        self.key_queue = []

    def getEvents(self):
       
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==pygame.KEYDOWN and event.key in [K_ESCAPE]):
                self.key_queue.clear()
                return False
            
            # KEEP KEY PRESS ORDER
            if event.type==pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                if event.key in [K_s, K_DOWN]:
                    self.key_queue.append("D")
                if event.key in [K_w, K_UP]:
                    self.key_queue.append("U")
                if event.key in [K_d, K_RIGHT]:
                    self.key_queue.append("R")
                if event.key in [K_a, K_LEFT]:
                    self.key_queue.append("L")

            # KEEP KEY PRESS ORDER (remove released from middle too)
            if event.type==pygame.KEYUP:
                if event.key in [K_s, K_DOWN]:
                    self.key_queue.remove("D")
                if event.key in [K_w, K_UP]:
                    self.key_queue.remove("U")
                if event.key in [K_d, K_RIGHT]:
                    self.key_queue.remove("R")
                if event.key in [K_a, K_LEFT]:
                    self.key_queue.remove("L")
        #if(self.upkey or self.rightkey or self.downkey or self.leftkey):
        #    print("up",self.upkey, "right", self.rightkey, "down", self.downkey, "left", self.leftkey)
        return True
    
    def get_first_of_remaining_pressed(self):
        keys = pygame.key.get_pressed()

        while(len(self.key_queue) > 0):
            match (self.key_queue[0]): 
                case "U":
                    if keys[pygame.K_UP] or keys[pygame.K_w]:
                        return (0,-1)
                case "D":
                    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                        return (0,1)
                case "L":
                    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                        return (-1,0)
                case "R":
                    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                        return (1,0)
            
            #in-valid front of queue items are removed
            self.key_queue.pop(0)

        return(0,0)

    def clean_queue(self):
        self.key_queue = []
        

#initialize the classes
held_keys = keyisdown()
delta_time = deltatime()
direction = (0,0)
from_tile = player_loc.center
player_current_speed = PLAYERNORMALSPEED

#game loop
while game_running:
    clock.tick(FPS)

    # indicating the number of miliseconds since the last time that piece of code was run
    dt = delta_time.loop_time()
    dt_distance = player_current_speed * dt

    game_running = held_keys.getEvents()

    new_direction = held_keys.get_first_of_remaining_pressed()
    to_tile = (from_tile[0] + direction[0] * TILESIZE[0], from_tile[1] + direction[1] * TILESIZE[1])

    # we have a direction
    if direction != (0,0) or new_direction != (0,0):
        #print("movement")
        # are we there yet?
        dist_to_dest = abs(math.dist(player_loc.center, to_tile))
        if (dist_to_dest <= abs(dt_distance)):
            player_loc.center = to_tile
            from_tile = to_tile
            #print("end of contineous movement")
            direction = new_direction
        else:
            velocity = (direction[0] * dt_distance, direction[1] * dt_distance)
            player_loc = player_loc.move(velocity)


    if (player_loc.center == food_loc.center):
        x = random.randrange(0, 20)
        y = random.randrange(0, 14)
        food_loc.center = (TILESIZE[0] * x + TILESIZE[0]/2) , (TILESIZE[1] * y + TILESIZE[1]/2)
        

    #clear the display
    screen.blit(background,(0,0))

    # place image on the screen
    screen.blit(food, food_loc)
    screen.blit(player, player_loc)

    # apply changes
    pygame.display.update()


# quit the pygame window
pygame.quit()
#the app exits
