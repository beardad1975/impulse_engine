import math
from random import randint,randrange

import pygame
from pygame.locals import *

from body import Body
from vector import Vec2
from matrix import Mat2


from shape import Circle, Polygon

from manifold import Manifold 
from impulse_math import DT, GRAVITY, FPS

WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)
YELLOW = (255,255,0)



class Game:
    screen = None
    done = None
    clock = None
    screen_size = (800, 600)
    
    counter = 0
    

    

    #accumulator = 0
    iterations = 8
    bodies = []
    need_to_remove = []
        
    contacts = []
    seasaw = None
    
def init():

    pygame.init()
    Game.screen = pygame.display.set_mode(Game.screen_size)
    pygame.display.set_caption("physics engine 2d")
    Game.done = False
    Game.clock = pygame.time.Clock()
    
    #b = Body( Circle(20), 140, 50)
    #b = Body( Circle(100), 300, 600)
    #b.setStatic()
    #Game.bodies.append(b)
    b = Body( Circle(100), 100, 600)
    b.setStatic()
    Game.bodies.append(b)
    
    b = Body( Circle(20), 200, 350)
    b.setStatic()
    Game.bodies.append(b)
    
    #Game.target = b
    
    #b2 = Body( Circle(70), 100, 300)
    #b2 = Body( Circle(90), 50, 150)
    #b2.setStatic()
    #Game.bodies.append(b2) 

    #b3 = Body( Circle(70), 200, 400)
    #b3 = Body( Circle(100), 220, 50)
    #b3.setStatic()
    #Game.bodies.append(b3)  

    #b4 = Body( Circle(70), 350, 400)
    #b4 = Body( Circle(200), 600, 0)
    #b4.setStatic()
    #Game.bodies.append(b4)        
    
    #verts = [Vec2(-17,10),Vec2(-33,-28),Vec2(-30,50),Vec2(10,20),Vec2(20,40),Vec2(17,-12), Vec2(-30,-10),Vec2(13,44)]
    
    #b5 = Body( Polygon(verts=verts), 300, 400, math.pi/3 )
    #b5 = Body( Polygon(boxHw=50, boxHh=100), 300, 400, math.pi/3 )
    #b5.shape.setBox(50, 100)
    #b5.setStatic()
    #Game.bodies.append(b5) 

    b6 = Body(Polygon(boxHw=260, boxHh=10), 500,300)
    b6.setOrient(0)
    b6.setStatic()
    Game.bodies.append(b6)
    Game.seasaw = b6
    
    
def handle_event():    
    for event in pygame.event.get():
        if event.type == QUIT:
            Game.done = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                Game.done = True
            elif event.key == K_LEFT:
                o = Game.seasaw.orient - 0.1
                Game.seasaw.setOrient(o)
            elif event.key == K_RIGHT:
                o = Game.seasaw.orient + 0.1
                Game.seasaw.setOrient(o)    
        #elif event.type == MOUSEBUTTONDOWN:
           
    
    b1, b2, b3 = pygame.mouse.get_pressed()
    if b1 :
        Game.counter += 1
        if Game.counter % 7 == 0:    
            mouseX, mouseY = pygame.mouse.get_pos()
            #size =  randint(10,40)
            #b = Body(Circle(size), mouseX, Game.screen_size[1]-mouseY)
            #verts = []
            #vertCount = randint(3, Polygon.MAX_POLY_VERTEX_COUNT)
            #for i in range(vertCount):
            #    verts.append(Vec2(randrange(-40,40), randrange(-40,40)))
            hw = randrange(10,40)
            hh = randrange(10,40)
            
            #b = Body(Polygon(verts=verts), mouseX, Game.screen_size[1]-mouseY)
            b = Body(Polygon(boxHw=hw, boxHh=hh), mouseX, mouseY)
            #b.setOrient(1.5)
            
            
            Game.bodies.append(b)
            #print("vertices:",b.shape.vertices)
            #print("normals:", b.shape.normals)
    elif b2:
        Game.counter += 1
        if Game.counter % 7 == 0:    
            mouseX, mouseY = pygame.mouse.get_pos()
            
            verts = []
            vertCount = randint(3, Polygon.MAX_POLY_VERTEX_COUNT)
            for i in range(vertCount):
                verts.append(Vec2(randrange(-40,40), randrange(-40,40)))
            
            
            b = Body(Polygon(verts=verts), mouseX, mouseY)
            
            
            
            
            Game.bodies.append(b)
            #print("vertices:",b.shape.vertices)
            #print("normals:", b.shape.normals)    
            
            
    elif b3 :
        Game.counter += 1
        if Game.counter % 7 == 0 :
            mouseX, mouseY = pygame.mouse.get_pos()
            size =  randint(10,40)
            b = Body(Circle(size), mouseX, mouseY)
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

    for m in Game.contacts:
        m.initialize() 
    
    for i in range(Game.iterations):
        for m in Game.contacts:
            m.applyImpulse()
                
    
    
    # integrate
    for b in Game.bodies:
        integrateForcesHalf(b)
        integrateVelocity(b)
        integrateForcesHalf(b)

        
        #clear force

    for m in Game.contacts:   
        m.correctPosition()        
        

    for b in Game.bodies:
        b.force = Vec2(0,0)
        b.torque = 0
        #check body that needs being remove
        if b.pos.y  >  Game.screen_size[1]:
 
            Game.need_to_remove.append(b)
    
    # remove objects
    for b in Game.need_to_remove:
        Game.bodies.remove(b)
    Game.need_to_remove = []



    
           
    #print("contacts:", len(Game.contacts))
    #if len(Game.contacts) > 0:
    #    print("impulse normal:", Game.contacts[0].impulse_normal)
    #    print("contaces point:", Game.contacts[0].contact_points)
    #collision resolution    

        
        

    


    
    
            

    
def integrateForces(body, dt=DT):
    if body.invMass == 0 :
        return

    body.velocity += (body.force * body.invMass + GRAVITY)  * dt
    body.angularVelocity += body.torque * body.invInertia * dt

    
def integrateForcesHalf(body, dt=DT):
    if body.invMass == 0 :
        return

    body.velocity += (body.force * body.invMass + GRAVITY) * 0.5 * dt
    body.angularVelocity += body.torque * body.invInertia * 0.5 * dt
    
def integrateVelocity(body, dt=DT):
    if body.invMass == 0 :
        return
    body.pos += body.velocity * dt
    o = body.orient + body.angularVelocity * dt
    body.setOrient(o)
    
        
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
            pos = (int(b.pos.x),int(b.pos.y))
            pygame.draw.circle(Game.screen, YELLOW, pos, radius, 1)
            #pygame.draw.circle(Game.screen, YELLOW, pos, radius, 3)
            #orientPos = (int(b.pos.x + rx), int(b.pos.y + ry))
            orientPos = (int(b.pos.x + rx),  int(b.pos.y + ry))
            pygame.draw.line(Game.screen, YELLOW, pos, orientPos, 1)
        elif isinstance(b.shape, Polygon):
            point_list = []
            for v in b.shape.vertices:
                v = b.shape.u * v
                v += b.pos
                p = (int(v.x),int(v.y)) 
                point_list.append(p)
            pygame.draw.polygon(Game.screen,WHITE,point_list,1)
             
            

    # draw contacts
    for m in Game.contacts:
        for i in range(m.contactCount):
            pos = m.contact_points[i]
            n = m.impulse_normal
            
            start_pos = (int(pos.x), int( pos.y))
            normal_pos = (int(pos.x + n.x*10), int( pos.y + n.y*10))
            if isinstance(m.A.shape, Circle):
                pygame.draw.line(Game.screen, YELLOW,start_pos, normal_pos)
            else:
                pygame.draw.line(Game.screen, WHITE,start_pos, normal_pos)
            
            if i == 0 :
                pygame.draw.circle(Game.screen, RED, start_pos, 2, 0)
            else:
                pygame.draw.circle(Game.screen, GREEN, start_pos, 2, 0)
    
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
        Game.clock.tick(FPS)

    pygame.quit()    
    
if __name__ == '__main__' : 
    init()
    main_loop()