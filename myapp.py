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

speed = 10
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
        self.leftkey = False
        self.rightkey = False
        self.upkey = False
        self.downkey = False
        self.key_queue = []

    def getEvents(self):
       
        for event in pygame.event.get():
            if event.type == QUIT:
                self.key_queue.clear()
                return False
           
            if event.type==pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                if event.key in [K_s, K_DOWN]:
                    self.downkey = True
                    self.key_queue.append("D")
                if event.key in [K_w, K_UP]:
                    self.upkey = True
                    self.key_queue.append("U")
                if event.key in [K_d, K_RIGHT]:
                    self.rightkey = True
                    self.key_queue.append("R")
                if event.key in [K_a, K_LEFT]:
                    self.leftkey = True
                    self.key_queue.append("L")
               
            if event.type==pygame.KEYUP:
                if event.key in [K_s, K_DOWN]:
                    self.downkey = False
                    self.key_queue.remove("D")
                if event.key in [K_w, K_UP]:
                    self.upkey = False
                    self.key_queue.remove("U")
                if event.key in [K_d, K_RIGHT]:
                    self.rightkey = False
                    self.key_queue.remove("R")
                if event.key in [K_a, K_LEFT]:
                    self.leftkey = False
                    self.key_queue.remove("L")
        #if(self.upkey or self.rightkey or self.downkey or self.leftkey):
        #    print("up",self.upkey, "right", self.rightkey, "down", self.downkey, "left", self.leftkey)
        return True
    
    def get_first_of_remaining_pressed(self):
        while(len(self.key_queue) > 0):
            match (self.key_queue[0]): 
                case "U":
                    if self.upkey:
                        return (0,-speed)
                case "D":
                    if self.downkey:
                        return (0,speed)
                case "L":
                    if self.leftkey:
                        return (-speed,0)
                case "R":
                    if self.rightkey:
                        return (speed,0)
            
            #should be removed if invalid or no longer valid
            self.key_queue.pop(0)

        return(0,0)

    def clean_queue(self):
        self.key_queue = []
        

#initialize the classes
held_keys = keyisdown()
delta_time = deltatime()

#game loop
while game_running:
    clock.tick(FPS)

    # indicating the number of miliseconds since the last time that piece of code was run
    dt = delta_time.loop_time()
    speed = 0.7 * dt

    game_running = held_keys.getEvents()
    velocity = (x,y) = held_keys.get_first_of_remaining_pressed()
    player_loc = player_loc.move(velocity)

    #clear the display
    screen.fill(white)

    # place image on the screen
    screen.blit(player, player_loc)
    # apply changes
    pygame.display.update()


# quit the pygame window
pygame.quit()
#the app exits
