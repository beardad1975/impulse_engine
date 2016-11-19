import math

PI = math.pi

class Circle:
    def __init__(self,size ):
        self.radius = size
        
        
    def computeMass(self, density, body):
        body.mass = PI * (self.radius**2) * density
        body.invMass = 1.0/body.mass if body.mass >= 0 else 0
        body.inertia = body.mass * (self.radius**2)
        body.invInertia = 1.0/body.inertia if body.inertia >=0 else 0 