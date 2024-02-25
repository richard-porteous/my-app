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
SCALEDTILESIZE = (STANDARD_IMAGE_SIZE[0] * SCALESIZE, STANDARD_IMAGE_SIZE[1] * SCALESIZE)


#### global style variables
start_speed = 0.4 * SCALESIZE
# set window size
SCREENSIZE = width, height = (STANDARD_IMAGE_SIZE[0] * ASPECT[0], STANDARD_IMAGE_SIZE[0] * ASPECT[1]) # 800,560 if 80x80
screen = pygame.display.set_mode(SCREENSIZE)

#build background

#grid centers - get while drawing grid lines on the background
x_tile_pos = []
y_tile_pos = []

background = pygame.Surface.copy(screen)
background.fill(WHITE)
# draw grid on background
screen_width = SCREENSIZE[0]
screen_length = SCREENSIZE[1]

## get grid centers and draw grid on background
#draw vertical lines on background
for x in range(0, SCREENSIZE[0], int(SCALEDTILESIZE[1])):
    x_tile_pos.append(x + int(SCALEDTILESIZE[1])/2)
    pygame.draw.line(background, BLACK, (x,0), (x,screen_length))
#draw horizontal lines on background
for y in range(0, SCREENSIZE[1], int(SCALEDTILESIZE[0])):
    y_tile_pos.append(y + int(SCALEDTILESIZE[0])/2)
    pygame.draw.line(background, BLACK, (0,y), (screen_width,y))
#### end build background ####

grid_objects = []

class GridObject(pygame.sprite.Sprite):
    go_counter = 0

    def __init__(self, img_file, scale = 1, gridpos = (0,0)):
        # Call the parent class (Sprite) constructor
        #pygame.sprite.Sprite.__init__(self)
        super().__init__()
        GridObject.go_counter += 1
        grid_objects.append(self)

        self.image = self.get_loaded_and_scaled_image(img_file, scale )
        self.rect = self.image.get_rect()
        self.rect.center = self.get_px_center_from_gridpos(gridpos)
    
    def get_loaded_and_scaled_image(self, img_file, scale) -> pygame.surface:
        image = pygame.image.load(img_file)
        image = pygame.transform.scale_by(image, scale )
        return image

    def get_px_center_from_gridpos(self, gridpos):
        #x,y = (SCALEDTILESIZE[0] * gridpos[0] + SCALEDTILESIZE[0]/2) , (SCALEDTILESIZE[1] * gridpos[1] + SCALEDTILESIZE[1]/2)
        x,y = x_tile_pos[gridpos[0]], y_tile_pos[gridpos[1]]
        return (x,y)

    def get_tile_center_positions(self):
        return (x_tile_pos,y_tile_pos)
    
    def place_obj_on_grid_unique() -> bool:
        return True


class GameObject(GridObject):
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
    
    def __init__(self, speed, tilesize, img_file):
        super().__init__(img_file, SCALESIZE)
        self.tilesize = tilesize
        self.name = "obj"
        self.start_move_pos = self.rect.center
        self.speed = speed
        self.max = SCREENSIZE
        self.collide_rect = Rect(
            self.rect[0] + self.rect[2]/2 - 1, 
            self.rect[1] + self.rect[3]/2 - 1, 
            self.rect[2] - self.rect[2]/2 + 1, 
            self.rect[3] - self.rect[3]/2 + 1)
        #print("==============")
        #print(self.rect)
        #print(self.collide_rect)
        #print("==============")
        self.just_created = True


    def is_end_of_move(self, dt_distance):
        return abs(math.dist(self.rect.center, self.end_move_pos)) <= abs(dt_distance)
    
    def setup_next_move(self, direction, end_move_pos):
        self.last_end_move_pos = self.end_move_pos
        self.last_start_move_pos = self.start_move_pos
        self.last_direction = self.direction
        self.last_boundary_check = self.boundary_check

        self.direction = self.fix_direction(direction)
        self.rect.center = end_move_pos
        self.start_move_pos = end_move_pos
        self.end_move_pos = self.get_destination(self.start_move_pos, self.direction)



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


    def get_destination(self, from_pos, direction, num_tiles = 1):
        return (from_pos[0] + direction[0] * self.tilesize[0], from_pos[1] + direction[1] * self.tilesize[1])


class Head(GameObject):
    

    def __init__(self, speed, tilesize):
        super().__init__(speed, tilesize, "assets/player/blue_body_squircle.png")
        self.name = "head"

        self.face_image = self.get_loaded_and_scaled_image("assets/player/face_a.png",SCALESIZE)
        
        ## draw 2nd image onto first
        self.face_rect = self.face_image.get_rect()
        self.face_rect.center = self.rect.center
        self.image.blit(self.face_image, self.face_rect)

        self.end_move_pos = self.get_destination(self.start_move_pos, self.direction)


    def eat_food(self, food):
        # the actual placing of the food should be done by food
        if (self.rect.center == food.rect.center):
            
            try_again = True
            counter = 5
            while try_again:
                try_again = False
                x = random.randrange(0, 20)
                y = random.randrange(0, 14)
                food.rect.center = food.get_px_center_from_gridpos((x,y))
                for go in grid_objects:
                    if go.name == "tail" or go.name == "head":
                        if go.rect.center == food.rect.center:
                            print(try_again, go.rect.center, food.rect.center)
                            counter -= 1
                            try_again = counter > 0
            if counter == 0 :
                pygame.quit() # another win condition
            return True
        return False
    
    def collide(self, tails):
        for t in tails:
            if pygame.Rect.colliderect(self.collide_rect, t.collide_rect) and t.just_created == False:
                return True
        return False



    def update(self, dt_distance, new_direction, def_direction, continuous):
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

        self.draw_wrap_image(self.rect,self.image,screen)
        self.draw_wrap_image(self.face_rect,self.face_image,screen)


class Tail(GameObject):
    def __init__(self, speed, tilesize):
        super().__init__(speed, tilesize, "assets/player/blue_body_circle.png")
        self.name = "tail"

    
    def add_object_to_follow(self, obj):
        self.object_to_follow = obj
        self.rect.center = obj.rect.center
        self.end_move_pos = obj.rect.center
        self.start_move_pos = obj.rect.center


    def complete_move(self):
        self.last_end_move_pos = self.end_move_pos
        self.last_start_move_pos = self.start_move_pos
        self.last_direction = self.direction
        self.last_boundary_check = self.boundary_check

        
        self.rect.center = self.object_to_follow.last_start_move_pos
        self.start_move_pos = self.object_to_follow.last_start_move_pos
        self.end_move_pos = self.object_to_follow.last_end_move_pos
        self.boundary_check = self.object_to_follow.last_boundary_check
           
        self.direction = self.object_to_follow.last_direction

    def follow(self, dt_distance):
        self.check_boundaries()
        self.keep_moving(dt_distance)

    def update(self, move_start, dt_distance):
        if move_start:
            self.collide_rect.center = self.rect.center
            self.just_created = False
            self.complete_move()
        else:
            self.collide_rect.center = self.rect.center
            self.follow(dt_distance)
        
    def draw(self,screen):
        super().draw(screen)
        self.draw_wrap_image(self.rect,self.image,screen)


class Player():
    tail_group = pygame.sprite.Group()
    tailpieces = []

    def __init__(self, speed, tilesize):
        self.head = Head(speed, tilesize)

    def grow_tail(self, screen_size, start_speed):
        t = Tail(start_speed, self.head.tilesize)
        self.tail_group.add(t)
        
        if (len(self.tailpieces) > 0):
            t.add_object_to_follow(self.tailpieces[len(self.tailpieces) - 1])
        else:
            t.add_object_to_follow(self.head)

        self.tailpieces.append(t)

    def update(self, dt, new_direction, def_direction):
        dt_distance = self.head.speed * dt
        move_start = self.head.update(dt_distance,new_direction,def_direction,True)
        self.tail_group.update(move_start, dt_distance)

        if self.head.eat_food(food):
            self.grow_tail(self.head.max, self.head.speed)
        if GridObject.go_counter > 20:
            pygame.quit() # win condition

        if self.head.collide(self.tailpieces):
            return True
        return False


    def draw(self, screen):
        self.head.draw(screen)
        self.tail_group.draw(screen)


# GAME CODE

screen.blit(background,(0,0))
pygame.display.update()

player = Player(start_speed, SCALEDTILESIZE)
food = GridObject("assets/food/tile_coin.png",SCALESIZE, (9,9))
food.name = "food"

# we use a group for food as the game can have more that one piece of food
food_group = pygame.sprite.Group()
food_group.add(food)

# Initialize the pygame code
pygame.init()
clock = pygame.time.Clock()
# Max frame rate
FPS = 60
# movement
held_keys = KeyInput()
continuous = True
#keypress_for_partialtime = False
game_running = True

#game loop
while game_running:
    clock.tick(FPS)
    dt = clock.get_time()

    game_running = held_keys.getEvents()
    new_direction = held_keys.get_first_of_remaining_pressed()
    def_direction = held_keys.get_last_direction_chosen()
 
    player_collide = player.update(dt, new_direction, def_direction)
    if player_collide:
        game_running = False

    #clear the display
    screen.blit(background,(0,0))
    # place images on the screen
    food_group.draw(screen)
    player.draw(screen)
    # apply screen changes
    pygame.display.update()


# quit the pygame window
pygame.quit()
