import math
from random import randint

import pygame
from pygame.locals import *

from body import Body
from vector import Vec2
from shape import Circle
from manifold import Manifold 
from impulse_math import DT, GRAVITY

WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0,0,0)
PI = math.pi



class Game:
    screen = None
    done = None
    clock = None
    screen_size = (800, 600)
    
    counter = 0
    

    

    #accumulator = 0
    iterations = 2
    bodies = []
    need_to_remove = []
        
    contacts = []

def init():

    pygame.init()
    Game.screen = pygame.display.set_mode(Game.screen_size)
    pygame.display.set_caption("physics engine 2d")
    Game.done = False
    Game.clock = pygame.time.Clock()
    
    #b = Body( Circle(20), 140, 50)
    b = Body( Circle(20), 100, 400)
    #b.force = Vec2(5000000,0)
    #b.angularVelocity = -3
    #b.setStatic()
    Game.bodies.append(b)
    #Game.target = b
    
    #b2 = Body( Circle(70), 100, 300)
    b2 = Body( Circle(90), 50, 150)
    b2.setStatic()
    Game.bodies.append(b2) 

    #b3 = Body( Circle(70), 200, 400)
    b3 = Body( Circle(100), 220, 50)
    b3.setStatic()
    Game.bodies.append(b3)  

    #b4 = Body( Circle(70), 350, 400)
    b4 = Body( Circle(150), 600, 0)
    b4.setStatic()
    Game.bodies.append(b4)        
    

def handle_event():    
    for event in pygame.event.get():
        if event.type == QUIT:
            Game.done = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                Game.done = True
        #elif event.type == MOUSEBUTTONDOWN:
           
    
    b1, _, _ = pygame.mouse.get_pressed()
    if b1 :
        Game.counter += 1
        if Game.counter % 7 == 0:    
            mouseX, mouseY = pygame.mouse.get_pos()
            size =  randint(10,40)
            b = Body(Circle(size), mouseX, Game.screen_size[1]-mouseY)
            Game.bodies.append(b)
    
def step():

    Game.contacts = []
    #collision detect
    for index, A in enumerate(Game.bodies):
        for B in Game.bodies[index+1:]:
            if A.invMass == 0 and B.invMass == 0 :
                continue
            m = Manifold(A, B)
            m.solve()
            
            if m.contactCount > 0:
                Game.contacts.append(m)
    
    print (len(Game.bodies))
    #collision resolution    
    for m in Game.contacts:
        m.initialize() 
    
    for i in range(Game.iterations):
        for m in Game.contacts:
            m.applyImpulse()
        
        
    for m in Game.contacts:   
        m.correctPosition()
    
    # integrate
    for b in Game.bodies:
        integrateForcesHalf(b)
        integrateVelocity(b)
        integrateForcesHalf(b)
        #clear force
        
        b.force = Vec2(0,0)
        b.torque = 0
        #check body that needs being remove
        #if b.pos.y  >  Game.screen_size[1]:
        if b.pos.y  <  0:
            Game.need_to_remove.append(b)

    
    
            
    # remove objects
    for b in Game.need_to_remove:
        Game.bodies.remove(b)
    Game.need_to_remove = []
    
        
def integrateForcesHalf(body, dt=DT):
    if body.invMass == 0 :
        return

    body.velocity += (body.force * body.invMass + GRAVITY) * 0.5 * dt
    body.angularVelocity += body.torque * body.invInertia * 0.5 * dt
    
def integrateVelocity(body, dt=DT):
    if body.invMass == 0 :
        return
    body.pos += body.velocity * dt
    body.orient += body.angularVelocity * dt
    
    
        
def draw():
    #erase
    Game.screen.fill(BLACK)

    #draw objects
    for b in Game.bodies:
        if isinstance(b.shape, Circle):
            radius = b.shape.radius
            rx = math.cos(b.orient) * radius
            ry = math.sin(b.orient) * radius
            
            #pos = (int(b.pos.x),  int(b.pos.y))
            pos = (int(b.pos.x), Game.screen_size[1] - int(b.pos.y))
            pygame.draw.circle(Game.screen, WHITE, pos, radius, 1)
            
            #orientPos = (int(b.pos.x + rx), int(b.pos.y + ry))
            orientPos = (int(b.pos.x + rx), Game.screen_size[1] - int(b.pos.y + ry))
            pygame.draw.line(Game.screen, WHITE, pos, orientPos)
            
             
            #print(pos, radius)

    
    #flip
    pygame.display.flip()
    
def main_loop():    
    while not Game.done:
        handle_event()
        
        #calculate
        step()

        #print(Game.target.angularVelocity, Game.target.orient)
        #draw
        draw()


        #fps
        Game.clock.tick(50)

    pygame.quit()    
    
if __name__ == '__main__' : 
    init()
    main_loop()