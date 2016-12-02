from vector import Vec2, cross
from impulse_math import RESTITUTION

class Body:
    def __init__(self, shape, posX, posY, orient=0,density=1):
        self.shape = shape
        self.pos = Vec2(posX, posY)
        self.velocity = Vec2(0, 0)
        self.force = Vec2(0, 0)

        self.angularVelocity = 0
        self.torque = 0
        self.orient = orient
        self.mass = 0
        self.invMass = 0
        self.inertia = 0
        self.invInertia = 0
        self.staticFriction = 0.4
        self.dynamicFriction = 0.3
        self.restitution = RESTITUTION
        
        self.shape.computeMass(density, self)
        self.shape.setOrient(self.orient)
        
    def setStatic(self):
        self.inertia = 0
        self.invInertia = 0
        self.mass = 0
        self.invMass = 0
        
    def setOrient(self, radians):
        self.orient = radians
        self.shape.setOrient(radians)
        
    def applyImpulse(self, impulse, contactVector):
        self.velocity  += impulse * self.invMass
        self.angularVelocity += self.invInertia * cross(contactVector, impulse)
        #print (self.angularVelocity)
    