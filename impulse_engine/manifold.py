
import math

from vector import Vec2, dot, cross, distanceSq
from body import Body
from shape import Circle, Polygon
from impulse_math import RESTING, EPSILON, gt, PENETRATION_ALLOWANCE, PENETRATION_CORRECTION, equal

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
        self.e = 0.3
        self.sf = 0.4
        self.df = 0.2
        
    def solve(self):
        if isinstance(self.A.shape, Circle) and isinstance(self.B.shape, Circle):
            self.collisionCircleCircle()
        elif isinstance(self.A.shape, Polygon) and isinstance(self.B.shape, Polygon):
            self.collisionPolygonPolygon()
        elif isinstance(self.A.shape, Circle) and isinstance(self.B.shape, Polygon):
            self.collitionCirclePolygon(self.A, self.B)
        elif isinstance(self.B.shape, Circle) and isinstance(self.A.shape, Polygon):  
            self.collitionCirclePolygon(self.B, self.A)
            if self.contactCount > 0 :
                self.impulse_normal = - self.impulse_normal
            
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
            pos = self.impulse_normal * radiusA + self.A.pos
            self.contact_points[0].set(pos)

    def collisionPolygonPolygon(self):
        polyA = self.A.shape
        polyB = self.B.shape
        
        self.contactCount = 0
        
        faceA = [None]
        penetrationA = self.findAxisLeastPenetration(faceA,polyA,polyB)    
        if penetrationA >= 0 :
            #seperating
            return
            
        faceB = [None]
        penetrationB = self.findAxisLeastPenetration(faceB,polyB,polyA)
        if penetrationB >= 0 :
            return
        #print("faceA:",faceA)
        #print("faceB:", faceB)
        
        referenceIndex = None
        flip = None
        refPoly = None
        incPoly = None
        
        if gt(penetrationA, penetrationB):
            refPoly = polyA
            incPoly = polyB
            referenceIndex = faceA[0]
            flip = False
        else:
            refPoly = polyB
            incPoly = polyA
            referenceIndex = faceB[0]
            flip = True
            
        incidentFace = [0, 0]  # array of Vec2
        self.findIncidentFace(incidentFace, refPoly, incPoly, referenceIndex)
        
        #setup reference face vertices
        v1 = refPoly.vertices[referenceIndex]
        referenceIndex = 0 if referenceIndex+1 == refPoly.vertexCount else referenceIndex+1
        v2 = refPoly.vertices[referenceIndex]
    
        #transform vertices to world space
        v1 = refPoly.u * v1 + refPoly.body.pos
        v2 = refPoly.u * v2 + refPoly.body.pos
        
        sidePlaneNormal = v2 - v1
        sidePlaneNormal.normalize()
        
        refFaceNormal = Vec2(sidePlaneNormal.y, -sidePlaneNormal.x)
        
        refC = dot(refFaceNormal, v1)
        negSide = -dot(sidePlaneNormal, v1)
        posSide = dot(sidePlaneNormal, v2)
        
        if self.clip(-sidePlaneNormal,negSide, incidentFace) < 2:
            return
    
        if self.clip(sidePlaneNormal,posSide, incidentFace) < 2:
            return
            
        self.impulse_normal.set(refFaceNormal)
        if flip:
            self.impulse_normal = -self.impulse_normal
            
        cp = 0
        separation = dot(refFaceNormal, incidentFace[0]) - refC
        if separation <= 0:
            self.contact_points[cp].set(incidentFace[0])
            self.penetration = - separation
            cp += 1
        else :
            self.penetration = 0
            
        separation = dot(refFaceNormal, incidentFace[1] ) - refC
        if separation <= 0:
            self.contact_points[cp].set(incidentFace[1])
            self.penetration += -separation
            cp += 1
            self.penetration /= cp
            
        self.contactCount = cp
    
    def collitionCirclePolygon(self, a, b):
        circleA = a.shape
        polyB = b.shape
        
        self.contactCount = 0
        
        center = a.pos
        center = polyB.u.transpose() * (center - b.pos)
        
        separation = -100000000
        faceNormal = 0
        for i in range(polyB.vertexCount):
            s = dot(polyB.normals[i], center - polyB.vertices[i])
            if s > circleA.radius:
                return
                
            if s > separation:
                separation = s
                faceNormal = i
                
        v1 = polyB.vertices[faceNormal]
        i2 = faceNormal+1 if faceNormal+1 < polyB.vertexCount else 0
        v2 = polyB.vertices[i2]
        
        if separation < EPSILON:
            self.contactCount = 1
            self.impulse_normal = -(polyB.u * polyB.normals[faceNormal])
            self.contact_points[0] = self.impulse_normal * circleA.radius + a.pos
            self.penetration = circleA.radius
            return
        
        dot1 = dot(center - v1, v2 - v1)
        dot2 = dot(center - v2, v1 - v2)
        self.penetration = circleA.radius - separation
        
        if dot1 <= 0:
            if distanceSq(center, v1 ) > circleA.radius **2:
                return
                
            self.contactCount = 1
            n = v1 - center
            n = polyB.u * n
            n.normalize()
            self.impulse_normal = n
            v1 = polyB.u * v1 + b.pos
            self.contact_points[0] = v1
        elif dot2 <= 0:
            if distanceSq(center, v2) > circleA.radius **2:
                return
                
            self.contactCount = 1
            n = v2 - center
            v2 = polyB.u * v2 + b.pos
            self.contact_points[0] = v2
            n = polyB.u * n
            n.normalize()
            self.impulse_normal = n
            
        else:
            n = polyB.normals[faceNormal]
            if dot(center - v1, n) > circleA.radius:
                return
                
            n = polyB.u * n
            self.impulse_normal = -n
            self.contact_points[0] = self.impulse_normal * circleA.radius + a.pos
            self.contactCount = 1
            
        
        
    
    def findAxisLeastPenetration(self, faceIndex, poly1, poly2):
        
        bestDistance = -1000000.0
        bestIndex = 0
        
        for i in range(poly1.vertexCount):
           
            #transform A's face normal int B's model space
            nw = poly1.u * poly1.normals[i]
            buT = poly2.u.transpose()
            n = buT * nw

            #retrieve support point from B along -n
            s = poly2.getSupport( -n )
            
            #retrieve vertex on face from A , transform into B's model space
            v = poly1.vertices[i]
            v = poly1.u * v + poly1.body.pos
            v -= poly2.body.pos
            v = buT * v
    
            #compute penetration ( in B's model)
            d = dot(n, s - v)
            
            if d > bestDistance:
                bestDistance = d
                bestIndex = i 
        
        faceIndex[0] = bestIndex    
        return bestDistance        
    
    def findIncidentFace(self, incidentFace, refPoly, incPoly, referenceIndex):
        referenceNormal = refPoly.normals[referenceIndex]
        
        #calculate normal in incidents' frame ofo reference
        referenceNormal = refPoly.u * referenceNormal
        referenceNormal = incPoly.u.transpose() * referenceNormal
    
        # find most anti-normal face on incident polygon
        face = 0
        minDot = 10000000.0
        for i in range(incPoly.vertexCount):
            d = dot(referenceNormal, incPoly.normals[i])
            if d < minDot:
                minDot = d
                face = i
        
        incidentFace[0] = incPoly.u * incPoly.vertices[face] + incPoly.body.pos
        face = 0 if face + 1 >= incPoly.vertexCount else face + 1
        incidentFace[1] = incPoly.u * incPoly.vertices[face] + incPoly.body.pos

    def clip(self, n, c, face):
        sp = 0
        out = [ Vec2(face[0]), Vec2(face[1]) ]
        
        d1 = dot(n, face[0]) - c
        d2 = dot(n, face[1]) - c
        
        if d1 <= 0 :
            out[sp].set(face[0])
            sp += 1
        
        if d2 <= 0 :
            out[sp].set(face[1])
            sp += 1
            
        if d1 * d2 < 0 :
            alpha = d1 / (d1-d2)
            out[sp] = face[0] +  (face[1] - face[0]) * alpha
            sp += 1
            
        face[0] = out[0]
        face[1] = out[1]
        
        return sp

        
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
    
        if equal(A.invMass + B.invMass, 0 )  :
            self.infiniteMassCorrection()
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
            
            #invMassSum = A.invMass + B.invMass - (raCrossN**2) * A.invInertia - (rbCrossN**2) * B.invInertia
            
            j = -(1+ self.e)* contactVel
            j /=invMassSum
            j /=self.contactCount
            
            impulse = self.impulse_normal * j
            
            
            
            A.applyImpulse(-impulse, ra)
            B.applyImpulse(impulse, rb)
            
            
            
            # Friction Impulse
            rv = B.velocity + cross(B.angularVelocity, rb) - A.velocity - cross(A.angularVelocity, ra)
            
            # t is tangent unit vector
            t = rv -  (self.impulse_normal * dot(rv, self.impulse_normal))
            t.normalize()
            
            # j is tangent magnitude
            jt = -1 * dot(rv, t)
            jt /= invMassSum
            jt /= self.contactCount
            
            
            
            if equal(jt, 0) :
                
                return
                
            # Coulumb's Law
            tangentImpulse = None
            if abs(jt) < j * self.sf:
                tangentImpulse = t * jt
            else:
                tangentImpulse = t * (-j * self.df)
            
            
            #print(tangentImpulse)  
                    
            A.applyImpulse(-tangentImpulse, ra)
            B.applyImpulse(tangentImpulse, rb)
            
            
            
    def correctPosition(self):
        A = self.A
        B = self.B
        correction = max( self.penetration - PENETRATION_ALLOWANCE ,0)/ (A.invMass + B.invMass)  * PENETRATION_CORRECTION
        
        A.pos -=  self.impulse_normal * correction * A.invMass
        B.pos +=  self.impulse_normal * correction * B.invMass
        
    def infiniteMassCorrection(self):
        self.A.velocity.set(0,0)
        self.B.velocity.set(0,0)