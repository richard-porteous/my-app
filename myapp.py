import math
import random
import pygame
from pygame.locals import *
from mygame_library import *


#### HARD CODED VALUES
BLACK = (0,0,0)
WHITE = (255,255,255)
STANDARD_IMAGE_SIZE = (80,80)
ASPECT = (10,7)
SCALESIZE = 0.5
TILESIZE = (STANDARD_IMAGE_SIZE[0] * SCALESIZE, STANDARD_IMAGE_SIZE[1] * SCALESIZE)
# Max frame rate
FPS = 60

#### global style variables
start_speed = 0.4 * SCALESIZE
# set window size
screen_size = width, height = (STANDARD_IMAGE_SIZE[0] * ASPECT[0], STANDARD_IMAGE_SIZE[0] * ASPECT[1]) # 800,560 if 80x80
screen = pygame.display.set_mode(screen_size)

class SpriteObject(pygame.sprite.Sprite):
    def __init__(self, img_file, scale = 1):
        # Call the parent class (Sprite) constructor
        #pygame.sprite.Sprite.__init__(self)
        super().__init__()

        self.image = pygame.image.load(img_file)
        self.image = pygame.transform.scale_by(self.image, scale )
        self.rect = self.image.get_rect()
    

class GameObject(SpriteObject):
    start_move_pos = (0,0)
    end_move_pos = (0,0)
    direction = (0,0)
    min = (0,0)
    max = (0,0)
    boundary_check = "none"
    last_end_move_pos = (0,0)
    last_start_move_pos = (0,0)
    last_direction = (0,0)
    last_boundary_check = "none"
    
    def __init__(self, speed, tilesize, img_file, screen_size):
        super().__init__(img_file, SCALESIZE)
        self.tilesize = tilesize
        
        self.start_move_pos = self.rect.center
        self.speed = speed
        self.max = screen_size
        self.collide_rect = Rect(self.rect[0] + self.rect[2]/2, self.rect[1] + self.rect[3]/2, self.rect[2]/2, self.rect[3]/2) #left,top,width,height
        self.just_created = True

    

    def is_end_of_move(self, dt_distance):
        return abs(math.dist(self.rect.center, self.end_move_pos)) <= abs(dt_distance)
    
    def keep_moving(self, dt_distance):
        velocity = (self.direction[0] * dt_distance, self.direction[1] * dt_distance)
        self.rect = self.rect.move(velocity)

    # normalize direction
    def fix_direction(self, end, start=(0,0)):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        if dx > 0: dx = 1
        if dx < 0: dx = -1
        if dy > 0: dy = 1
        if dy < 0: dy = -1

        return (dx, dy)
    
    def get_tile_center_positions(self):
        return (x_tile_pos,y_tile_pos) 

    #currently only works with 4 directions
    def check_boundaries(self):
        x_pos,y_pos = self.get_tile_center_positions()
        
        if self.boundary_check != "none":
            return
        
        end_move_pos = self.end_move_pos

        if self.rect.left <= 0 and self.direction[0] < 0:
            self.set_boundary_check("left")
            end_move_pos = (x_pos[len(x_pos) -1] + self.tilesize[0], self.rect.center[1])
            
        if self.rect.right >= self.max[0] and self.direction[0] > 0:
            self.set_boundary_check("right")
            end_move_pos = (x_pos[0] - self.tilesize[0], self.rect.center[1])

        if self.rect.top <= 0 and self.direction[1] < 0:
            self.set_boundary_check("top")
            end_move_pos = (self.rect.center[0], y_pos[len(y_pos) -1] + self.tilesize[1])

        if self.rect.bottom >= self.max[1] and self.direction[1] > 0:
            self.set_boundary_check("bottom")
            end_move_pos = (self.rect.center[0], y_pos[0] - self.tilesize[1])

        if self.boundary_check in ["left","right","top","bottom"]:
            self.setup_next_move(self.direction, end_move_pos)

    def set_boundary_check(self, side):
        self.boundary_check = side

    def draw_wrap_image(self,rect,image,screen):

        # Draw echo/ghost/disapearing-character  Rect(left, top, width, height)
        if (self.boundary_check == "left"):
            shifted_rect = pygame.Rect(rect[0] - self.max[0], rect[1], rect[2], rect[3])
        elif (self.boundary_check == "right"):
            shifted_rect = pygame.Rect(rect[0] + self.max[0], rect[1], rect[2], rect[3])
        elif (self.boundary_check == "top"):
            shifted_rect = pygame.Rect(rect[0], rect[1] - self.max[1], rect[2], rect[3])
        elif (self.boundary_check == "bottom"):
            shifted_rect = pygame.Rect(rect[0], rect[1] + self.max[1], rect[2], rect[3])

        if (self.boundary_check in ["left", "right", "bottom", "top"]):
            screen.blit(image, shifted_rect)


    def draw(self, screen):
        screen.blit(self.image,self.rect)


class Head(GameObject):
    

    def __init__(self, speed, tilesize, screen_size):
        super().__init__(speed, tilesize, "assets/player/blue_body_squircle.png", screen_size)
        self.face_image = pygame.image.load("assets/player/face_a.png")
        self.face_image = pygame.transform.scale_by(self.face_image, 0.5 )
        self.face_rect = self.face_image.get_rect()
        self.face_rect.center = self.rect.center
        self.end_move_pos = (self.start_move_pos[0] + self.direction[0] * self.tilesize[0], self.start_move_pos[1] + self.direction[1] * self.tilesize[1])


    def eat_food(self, food):
        if (self.rect.center == food.rect.center):
            x = random.randrange(0, 20)
            y = random.randrange(0, 14)
            food.rect.center = (self.tilesize[0] * x + self.tilesize[0] * SCALESIZE) , (self.tilesize[1] * y + self.tilesize[1] * SCALESIZE)
            return True
        return False
    
    def collide(self, tails):
        for t in tails:
            if pygame.Rect.colliderect(self.collide_rect, t.collide_rect) and t.just_created == False:
                return True
        return False


    def setup_next_move(self, direction, end_move_pos):
        self.last_end_move_pos = self.end_move_pos
        self.last_start_move_pos = self.start_move_pos
        self.last_direction = self.direction
        self.last_boundary_check = self.boundary_check

        self.direction = self.fix_direction(direction)
        self.rect.center = end_move_pos
        self.start_move_pos = end_move_pos
        self.end_move_pos = (self.start_move_pos[0] + self.direction[0] * self.tilesize[0], self.start_move_pos[1] + self.direction[1] * self.tilesize[1])


    def move(self, dt_distance, new_direction, def_direction, continuous):
        direction = self.direction
        if direction != (0,0) or new_direction != (0,0):

            if (self.is_end_of_move(dt_distance)):
                self.collide_rect.center = self.rect.center
                if (continuous and new_direction == (0,0)):
                    direction = def_direction
                else:
                    direction = new_direction
                self.setup_next_move(direction, self.end_move_pos)
                self.set_boundary_check("none")
                return True

            else:
                self.collide_rect.center = self.rect.center
                #keep moving we are not there yet
                self.check_boundaries()
                self.keep_moving(dt_distance)

        return False

    def draw(self,screen):
        super().draw(screen)
        self.face_rect.center = self.rect.center
        screen.blit(self.face_image, self.face_rect)

        self.draw_wrap_image(self.rect,self.image,screen)
        self.draw_wrap_image(self.face_rect,self.face_image,screen)
        


class Tail(GameObject):
    def __init__(self, speed, tilesize, screen_size):
        super().__init__(speed, tilesize, "assets/player/blue_body_circle.png", screen_size)
    
    def complete_move(self):
        self.last_end_move_pos = self.end_move_pos
        self.last_start_move_pos = self.start_move_pos
        self.last_direction = self.direction
        self.last_boundary_check = self.boundary_check

        
        self.rect.center = self.object_to_follow.last_start_move_pos
        self.start_move_pos = self.object_to_follow.last_start_move_pos
        self.end_move_pos = self.object_to_follow.last_end_move_pos
        self.boundary_check = self.object_to_follow.last_boundary_check
           
        self.direction = self.object_to_follow.last_direction #self.fix_direction(self.end_move_pos, self.start_move_pos)

    def follow(self, dt_distance):
        self.check_boundaries()
        self.keep_moving(dt_distance)

    def move(self, move_start, dt_distance):
        if move_start:
            self.collide_rect.center = self.rect.center
            self.just_created = False
            t.complete_move()
        else:
            self.collide_rect.center = self.rect.center
            t.follow(dt_distance)
        
    def draw(self,screen):
        super().draw(screen)
        self.draw_wrap_image(self.rect,self.image,screen)

class Player():
    tail_group = pygame.sprite.Group()
    tailpieces = []

    def __init__(self, speed, tilesize, screen_size):
        self.head = Head(speed, tilesize, screen_size)

    def grow_tail(self, screen_size, start_speed):
        t = Tail(start_speed, self.head.tilesize, screen_size)
        self.tail_group.add(t)
        if (len(self.tailpieces) > 0):
            f = self.tailpieces[len(self.tailpieces) - 1]
            t.rect.center = f.rect.center
            t.end_move_pos = f.rect.center
            t.start_move_pos = f.rect.center
            t.object_to_follow = f
        else:
            t.rect.center = self.head.rect.center
            t.end_move_pos = self.head.rect.center
            t.start_move_pos = self.head.rect.center
            t.object_to_follow = self.head
        self.tailpieces.append(t)

    def draw(self, screen):
        self.head.draw(screen)
        self.tail_group.draw(screen)


# START OF GAME CODE


#### build background - background is used to clear each frame ####
background = pygame.Surface.copy(screen)
background.fill(WHITE)

# draw grid on background
x_tile_pos = []
y_tile_pos = []
for y in range(0, height, int(TILESIZE[0])):
    y_tile_pos.append(y + int(TILESIZE[0])/2)
    pygame.draw.line(background, BLACK, (0,y), (width,y))
for x in range(0, width, int(TILESIZE[1])):
    x_tile_pos.append(x + int(TILESIZE[1])/2)
    pygame.draw.line(background, BLACK, (x,0), (x,height))

screen.blit(background,(0,0))
#### end background ####

# Early update the display for background
pygame.display.update()

food_group = pygame.sprite.Group()


player = Player(start_speed, TILESIZE, screen_size)


#food
food = SpriteObject("assets/food/tile_coin.png",SCALESIZE)
food.rect.center = (TILESIZE[0] * 9 + TILESIZE[0]/2) , (TILESIZE[1] * 9 + TILESIZE[1]/2)
food_group.add(food)

# Initialize the pygame code
pygame.init()
clock = pygame.time.Clock()
FPS = 60

#speed = 10
# control variable
game_running = True


#initialize the classes
held_keys = KeyInput()
delta_time = DeltaTime()

continuous = True
keypress_for_partialtime = False

# control variable
game_running = True

#game loop
while game_running:
    clock.tick(FPS)

    # indicating the number of miliseconds since the last time that piece of code was run
    dt = delta_time.loop_time()
    

    game_running = held_keys.getEvents()

    new_direction = held_keys.get_first_of_remaining_pressed()
    def_direction = held_keys.get_last_direction_chosen()
 
    # do we have a direction?
    dt_distance = player.head.speed * dt
    move_start = player.head.move(dt_distance,new_direction,def_direction,continuous)
    for t in player.tailpieces:
        t.move(move_start, dt_distance)

    if player.head.eat_food(food):
        player.grow_tail(screen_size, start_speed)
        

    #clear the display
    screen.blit(background,(0,0))

    # place image on the screen
    food_group.draw(screen)
    
    
    player.draw(screen)

    # apply changes
    pygame.display.update()

    if player.head.collide(player.tailpieces):
        game_running = False

# quit the pygame window
pygame.quit()
