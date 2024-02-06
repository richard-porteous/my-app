import pygame
from pygame.locals import *


# time based movement requires delta time
class DeltaTime():
    """
    could use 'dt = clock.get_time()' instead. 
    It must be used with clock.tick(fps)
    i.e.

        clock.tick(fps)

        dt = clock.get_time()
    """

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
        

