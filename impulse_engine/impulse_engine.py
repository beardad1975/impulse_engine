import pygame
import math

pygame.init()

WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0,0,0)
PI = math.pi
SCREEN_SIZE = (500, 500)


class Circle:
    def __init__(self,size):
        self.radius = size
        
    def computeMass(self, density, body):
        body.mass = PI * (self.radius**2) * density
        body.invMass = 1.0/body.mass if body.mass >= 0 else 0
        body.inertia = body.mass * (self.radius**2)
        body.invInertia = 1.0/body.inertia if body.inertia >=0 else 0 

class Body:
    def __init__(self, shape, x, y):
        self.shape = shape
        self.posX = 0
        self.posY = 0
        self.velX = 0
        self.velY = 0
        self.forceX = 0
        self.forceY = 0
        self.angularVelocity = 0
        self.torque = 0
        self.orient = 0
        self.mass = 0
        self.invMass = 0
        self.inertia = 0
        self.invInertia = 0
        self.staticFriction = 0.5
        self.dynamicFriction = 0.3
        self.restitution = 0.2
        
        self.computeMass(1.0, self)




screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("physics engine 2d")
done = False
clock = pygame.time.Clock()



while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    #calculate

    #draw
    screen.fill(BLACK)

    
    
    #flip 
    pygame.display.flip()
    
    #fps
    clock.tick(60)

pygame.quit()    