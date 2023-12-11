import math
import random
import pygame
from pygame.locals import *


# HARD CODED VALUES
SCALESIZE = 0.5
TILE_SIZE = (80,80)
ASPECT = (10,7)
black = (0,0,0)
white = (255,255,255)
start_speed = 0.4

PLAYERNORMALSPEED = start_speed * SCALESIZE

# set window size
screen_size = width, height = (TILE_SIZE[0] * ASPECT[0], TILE_SIZE[0] * ASPECT[1]) # 800,560 if 80x80
screen = pygame.display.set_mode(screen_size)
TILESIZE = (TILE_SIZE[0] * SCALESIZE, TILE_SIZE[1] * SCALESIZE)


#background
background = pygame.Surface.copy(screen)
background.fill(white)

x_tile_pos = []
y_tile_pos = []
for y in range(0, height, int(TILESIZE[0])):
    y_tile_pos.append(y + int(TILESIZE[0])/2)
    pygame.draw.line(background, black, (0,y), (width,y))
for x in range(0, width, int(TILESIZE[1])):
    x_tile_pos.append(x + int(TILESIZE[1])/2)
    pygame.draw.line(background, black, (x,0), (x,height))

def get_tile_center_positions():
    return (x_tile_pos,y_tile_pos) 


class GameObject():
    start_move_pos = (0,0)
    end_move_pos = (0,0)
    direction = (0,0)
    min = (0,0)
    max = (0,0)
    boundary_check = "none"
    
    def __init__(self, speed, tilesize, img_file, screen_size):
        self.tilesize = tilesize
        self.image = pygame.image.load(img_file)
        self.image = pygame.transform.scale_by(self.image, 0.5 )
        self.rect = self.image.get_rect()
        self.rect.center = tilesize[0]/2, tilesize[1]/2
        self.start_move_pos = self.rect.center
        self.speed = speed
        self.max = screen_size


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
    
    #currently only works with 4 directions
    def check_boundaries(self):
        x_pos,y_pos = get_tile_center_positions()
        
        if self.boundary_check != "none":
            return
        if self.rect.left < 0:
            self.set_boundary_check("left")
            self.end_move_pos = (x_pos[len(x_pos) -1], self.rect.center[1])
            self.setup_next_move(self.direction)
        if self.rect.right > self.max[0]:
            self.set_boundary_check("right")
            self.end_move_pos = (x_pos[0], self.rect.center[1])
            self.setup_next_move(self.direction)
        if self.rect.top < 0:
            self.set_boundary_check("top")
            self.end_move_pos = (self.rect.center[0], y_pos[len(y_pos) -1])
            self.setup_next_move(self.direction)
        if self.rect.bottom > self.max[1]:
            self.set_boundary_check("bottom")
            self.end_move_pos = (self.rect.center[0], y_pos[0])
            self.setup_next_move(self.direction)


    def set_boundary_check(self, side):
        self.boundary_check = side

    def update(self, screen):
        screen.blit(self.image,self.rect)


class Player(GameObject):
    def __init__(self, speed, tilesize, screen_size):
        super().__init__(speed, tilesize, "assets/player/blue_body_squircle.png", screen_size)

        self.face_image = pygame.image.load("assets/player/face_a.png")
        self.face_image = pygame.transform.scale_by(self.face_image, 0.5 )
        self.face_rect = self.face_image.get_rect()
        self.face_rect.center = self.rect.center



    def move(self, dt_distance, new_direction, def_direction, continuous):
        direction = self.direction
        if direction != (0,0) or new_direction != (0,0):
            if (self.is_end_of_move(dt_distance)):
                self.set_boundary_check("none")
                if (continuous and new_direction == (0,0)):
                    direction = def_direction
                else:
                    direction = new_direction
                self.setup_next_move(direction)
                return True
            else:
                #keep moving we are not there yet
                self.keep_moving(dt_distance)
                self.check_boundaries()
        return False

    def update(self,screen):
        super().update(screen)
        self.face_rect.center = self.rect.center
        screen.blit(self.face_image, self.face_rect)

        if (self.boundary_check == "left"):
            shifted_rect = pygame.Rect(self.rect[0] - self.max[0], self.rect[1], self.rect[2], self.rect[3])
            shifted_face_rect = pygame.Rect(self.face_rect[0] - self.max[0], self.face_rect[1], self.face_rect[2], self.face_rect[3])
        elif (self.boundary_check == "right"):
            shifted_rect = pygame.Rect(self.rect[0], self.rect[1], self.rect[2] + self.max[0], self.rect[3])
            shifted_face_rect = pygame.Rect(self.face_rect[0], self.face_rect[1], self.face_rect[2] + self.max[0], self.face_rect[3])
        elif (self.boundary_check == "top"):
            shifted_rect = pygame.Rect(self.rect[0], self.rect[1] + self.max[1], self.rect[2], self.rect[3])
            shifted_face_rect = pygame.Rect(self.face_rect[0], self.face_rect[1] + self.max[1], self.face_rect[2], self.face_rect[3])
        elif (self.boundary_check == "bottom"):
            shifted_rect = pygame.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3] - self.max[1])
            shifted_face_rect = pygame.Rect(self.face_rect[0], self.face_rect[1], self.face_rect[2], self.face_rect[3] - self.max[1])

        if (self.boundary_check in ["left", "right", "bottom", "top"]):
            screen.blit(self.image, shifted_rect)
            screen.blit(self.face_image, shifted_face_rect)


#Rect(left, top, width, height)



class Tail(GameObject):
    def __init__(self, speed, tilesize, screen_size):
        super().__init__(speed, tilesize, "assets/player/blue_body_circle.png", screen_size)
    
    def set_obj_to_follow(self, obj):
        self.object_to_follow = obj

    def complete_move(self):
        self.start_move_pos = self.end_move_pos
        self.rect.center = self.end_move_pos
        self.end_move_pos = self.object_to_follow.start_move_pos           
        self.direction = self.get_direction_from_start_end(self.start_move_pos, self.end_move_pos)

    def follow(self, dt_distance):
        self.keep_moving(dt_distance)



player = Player(PLAYERNORMALSPEED, TILESIZE, screen_size)
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

def grow_tail(TILESIZE, screen_size, PLAYERNORMALSPEED, Tail, player, player_tail):
    t = Tail(PLAYERNORMALSPEED, TILESIZE, screen_size)
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
    move_start = player.move(dt_distance,new_direction,def_direction,continuous)
    for t in player_tail:
        if move_start:
            t.complete_move()
        else:
            t.follow(dt_distance)


    if eat_food(TILESIZE, player, food_rect):
        grow_tail(TILESIZE, screen_size, PLAYERNORMALSPEED, Tail, player, player_tail)
        

    #clear the display
    screen.blit(background,(0,0))

    # place image on the screen
    screen.blit(food, food_rect)
    
    for t in player_tail:
        t.update(screen)
    
    player.update(screen)

    player.face_rect.center = player.rect.center
    screen.blit(player.face_image, player.face_rect)

    # apply changes
    pygame.display.update()


# quit the pygame window
pygame.quit()
#the app exits
