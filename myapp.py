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






class GameObject():
    start_move_pos = (0,0)
    end_move_pos = (0,0)
    direction = (0,0)
    
    def __init__(self, speed, tilesize, img_file):
        self.tilesize = tilesize
        self.image = pygame.image.load(img_file)
        self.image = pygame.transform.scale_by(self.image, 0.5 )
        self.rect = self.image.get_rect()
        self.rect.center = tilesize[0]/2, tilesize[1]/2
        self.start_move_pos = self.rect.center
        self.speed = speed

    def setup_next_move(self, direction):
        self.direction = direction
        self.rect.center = self.end_move_pos
        self.start_move_pos = self.end_move_pos
        self.end_move_pos = (self.start_move_pos[0] + self.direction[0] * self.tilesize[0], self.start_move_pos[1] + self.direction[1] * self.tilesize[1])


    def is_end_of_move(self, dt_distance):
        return abs(math.dist(self.rect.center, self.end_move_pos)) <= abs(dt_distance)
    
    def keep_moving(self, dt_distance):
        velocity = (self.direction[0] * dt_distance, self.direction[1] * dt_distance)
        self.rect = self.rect.move(velocity)

    def get_direction_from_start_end(self, start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        if dx > 0: dx = 1
        if dx < 0: dx = -1
        if dy > 0: dy = 1
        if dy < 0: dy = -1

        return (dx, dy)



class Player(GameObject):
    def __init__(self, speed, tilesize):
        super().__init__(speed, tilesize, "assets/player/blue_body_squircle.png")

        self.face_image = pygame.image.load("assets/player/face_a.png")
        self.face_image = pygame.transform.scale_by(self.face_image, 0.5 )
        self.face_rect = self.face_image.get_rect()
        self.face_rect.center = self.rect.center



    def move(self, dt_distance, new_direction, def_direction, continuous):
        direction = self.direction
        if direction != (0,0) or new_direction != (0,0):
            if (self.is_end_of_move(dt_distance)):
                if (continuous and new_direction == (0,0)):
                    direction = def_direction
                else:
                    direction = new_direction
                self.setup_next_move(direction)
            else:
                #keep moving we are not there yet
                self.keep_moving(dt_distance)



class Tail(GameObject):
    def __init__(self, speed, tilesize):
        super().__init__(speed, tilesize, "assets/player/blue_body_circle.png")
    
    def set_obj_to_follow(self, obj):
        self.object_to_follow = obj

    def follow(self, dt_distance):
        if (self.is_end_of_move(dt_distance)):
            self.start_move_pos = self.end_move_pos
            self.end_move_pos = self.object_to_follow.start_move_pos           
            self.direction = self.get_direction_from_start_end(self.start_move_pos, self.end_move_pos)
        else:
            self.keep_moving(dt_distance)



player = Player(PLAYERNORMALSPEED, TILESIZE)
player_tail = []

#food
food = pygame.image.load("assets/food/tile_coin.png")
food = pygame.transform.scale_by(food, 0.5 )
food_rect = food.get_rect()
food_rect.center = (TILESIZE[0] * 9 + TILESIZE[0]/2) , (TILESIZE[1] * 9 + TILESIZE[1]/2)

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
class DeltaTime():
    def __init__(self):
        self.last_loop = pygame.time.get_ticks()
        self.dt = 0


    def loop_time(self) -> int:
        time_now_ms = pygame.time.get_ticks()
        dt = time_now_ms - self.last_loop
        self.last_loop = time_now_ms
        return dt
    

class KeyInput():

    def __init__(self) -> None:
        self.key_queue = []
        self.last_key_pressed = "none"

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
                    self.last_key_pressed = "D"
                    self.key_queue.append("D")
                if event.key in [K_w, K_UP]:
                    self.last_key_pressed = "U"
                    self.key_queue.append("U")
                if event.key in [K_d, K_RIGHT]:
                    self.last_key_pressed = "R"
                    self.key_queue.append("R")
                if event.key in [K_a, K_LEFT]:
                    self.last_key_pressed = "L"
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

    def get_last_direction_chosen(self):
        match (self.last_key_pressed):
            case "U":
                return (0,-1)
            case "D":
                return (0,1)
            case "L":
                return (-1,0)
            case "R":
                return (1,0)
        return (0,0)

    def clean_queue(self):
        self.key_queue = []
        

#initialize the classes
held_keys = KeyInput()
delta_time = DeltaTime()

continuous = True
keypress_for_partialtime = False


#player.setup_next_move((0,0))
player.end_move_pos = (player.start_move_pos[0] + player.direction[0] * TILESIZE[0], player.start_move_pos[1] + player.direction[1] * TILESIZE[1])

#game loop
def eat_food(TILESIZE, player, food_rect):
    if (player.rect.center == food_rect.center):
        x = random.randrange(0, 20)
        y = random.randrange(0, 14)
        food_rect.center = (TILESIZE[0] * x + TILESIZE[0]/2) , (TILESIZE[1] * y + TILESIZE[1]/2)
        return True
    return False

while game_running:
    clock.tick(FPS)

    # indicating the number of miliseconds since the last time that piece of code was run
    dt = delta_time.loop_time()
    
    dt_distance = player.speed * dt

    game_running = held_keys.getEvents()

    direction = player.direction
    new_direction = held_keys.get_first_of_remaining_pressed()
    def_direction = held_keys.get_last_direction_chosen()
 
    # do we have a direction?
    player.move(dt_distance,new_direction,def_direction,continuous)
    for t in player_tail:
        t.follow(dt_distance)

    # eat food and grow tail
    if eat_food(TILESIZE, player, food_rect):
        t = Tail(PLAYERNORMALSPEED, TILESIZE)
        if (len(player_tail) > 0):
            f = player_tail[len(player_tail) - 1]
            t.rect.center = f.rect.center
            t.end_move_pos = f.rect.center
            t.start_move_pos = f.rect.center
            t.object_to_follow = f
        else:
            t.rect.center = player.rect.center
            t.end_move_pos = player.rect.center
            t.start_move_pos = player.rect.center
            t.object_to_follow = player
        player_tail.append(t)
        

    #clear the display
    screen.blit(background,(0,0))

    # place image on the screen
    screen.blit(food, food_rect)
    
    for t in player_tail:
        screen.blit(t.image,t.rect)
    
    screen.blit(player.image, player.rect)
    player.face_rect.center = player.rect.center
    screen.blit(player.face_image, player.face_rect)

    # apply changes
    pygame.display.update()


# quit the pygame window
pygame.quit()
#the app exits
