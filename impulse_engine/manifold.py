
import math

from vector import Vec2, dot, cross
from body import Body
from shape import Circle
from impulse_math import RESTING, EPSILON

class NotImplement(Exception): pass


class Manifold:
    def __init__(self, a, b):
        if not isinstance(a, Body) or  not isinstance(b, Body):
            raise NotImplement
        
        self.A = a
        self.B = b
        self.penetration = 0
        self.impulse_normal = Vec2()
        self.contact_points = [Vec2(), Vec2()]
        self.contactCount = 0
        self.e = 0.2
        self.sf = 0.5
        self.df = 0.3
        
    def solve(self):
        if isinstance(self.A.shape, Circle) and isinstance(self.B.shape, Circle):
            self.collisionCircleCircle()
            
    def collisionCircleCircle(self):
        normal = self.B.pos -  self.A.pos
        dist_sqr = normal.lengthSq()
        radiusA = self.A.shape.radius 
        radiusB = self.B.shape.radius
        radius = radiusA + radiusB
        
        if dist_sqr >= radius ** 2:
            return
            
        distance = math.sqrt(dist_sqr)
        self.contactCount = 1
        
        if distance == 0:
            self.penetration = radiusA
            self.impulse_normal.set(1, 0)
            self.contact_points[0].set(self.A.pos)
        else:
            self.penetration = radius - distance
            self.impulse_normal = normal / distance
            v = self.impulse_normal * radiusA + self.A.pos
            self.contact_points[0].set(v)

    def initialize(self):
        A = self.A
        B = self.B
        for i in range(self.contactCount):
            ra = self.contact_points[i] - A.pos
            rb = self.contact_points[i] - B.pos
            
            rv = B.velocity + cross(B.angularVelocity, rb) - A.velocity - cross(A.angularVelocity, ra)
            
            #print(RESTING)
            if rv.lengthSq() < RESTING :
                self.e = 0
                
                # if A.angularVelocity == 0 and B.angularVelocity == 0:
                    # return
                
                # if abs(A.angularVelocity) < 0.03:
                    # A.angularVelocity = 0
                # else:    
                    # A.angularVelocity *= 0.9
                
                # if abs(B.angularVelocity) < 0.03:
                    # B.angularVelocity = 0
                # else:
                    # B.angularVelocity *= 0.9
                
                
    def applyImpulse(self):
        A = self.A
        B = self.B
    
        if abs(A.invMass + B.invMass) < 0.000001 :
            
            return
            
        for i in range(self.contactCount):
            
            ra = self.contact_points[i] - A.pos
            rb = self.contact_points[i] - B.pos

            #Impulse
            rv = B.velocity + cross(B.angularVelocity, rb) - A.velocity - cross(A.angularVelocity, ra)

            contactVel = dot(rv, self.impulse_normal)
            if contactVel > 0:
                return
                
            raCrossN = cross(ra, self.impulse_normal)
            rbCrossN = cross(rb, self.impulse_normal)
            invMassSum = A.invMass + B.invMass + (raCrossN**2) * A.invInertia + (rbCrossN**2) * B.invInertia
            
            j = -(1+ self.e)* contactVel
            j /=invMassSum
            j /=self.contactCount
            
            impulse = self.impulse_normal * j
            A.applyImpulse(-impulse, ra)
            B.applyImpulse(impulse, rb)
            
            # Friction Impulse
            rv = B.velocity + cross(B.angularVelocity, rb) - A.velocity - cross(A.angularVelocity, ra)
            
            t = Vec2(rv)
            t = t +  (self.impulse_normal * -1 *dot(rv, self.impulse_normal))
            t.normalize()
            
            # j tangent magnitude
            jt = -1 * dot(rv, t)
            jt /= invMassSum
            jt /= self.contactCount
            
            
            
            if abs(jt) <= EPSILON:
                return
                
            # Coulumb's Law
            tangentImpulse = Vec2()
            if abs(jt) < j * self.sf:
                tangentImpulse = t * jt
            else:
                tangentImpulse = t * -j * self.df
            
            
            #print(tangentImpulse)        
            A.applyImpulse(-tangentImpulse, ra)
            B.applyImpulse(tangentImpulse, rb)
            
            
    def correctPosition(self):
        A = self.A
        B = self.B
        correction = max( self.penetration - 0.05 ,0)/ (A.invMass + B.invMass)  * 0.4
        
        A.pos +=  self.impulse_normal * correction * -A.invMass
        B.pos +=  self.impulse_normal * correction * B.invMass