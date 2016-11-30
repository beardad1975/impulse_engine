import math
from  matrix import Mat2
from vector import Vec2, cross, dot

PI = math.pi

class Circle:
    def __init__(self,size ):
        self.radius = size
        
    def computeMass(self, density, body):
        body.mass = PI * (self.radius**2) * density
        body.invMass = 1.0/body.mass if body.mass >= 0 else 0
        body.inertia = body.mass * (self.radius**2)
        body.invInertia = 1.0/body.inertia if body.inertia >=0 else 0

        self.body = body

    def setOrient(self, radians):
        pass
                
        
class Polygon:
    MAX_POLY_VERTEX_COUNT = 30

    def __init__(self, verts=[], boxHw=0, boxHh=0):
        self.vertexCount = 0
        self.vertices = []
        self.normals = []
        self.u = Mat2()
        self.setOrient(0)
        
        
        if verts :  
            self.set(verts)
        elif boxHw and boxHh:
            self.setBox(boxHw, boxHh)

    def set(self, verts):
        rightMost = 0
        highestXCoord = verts[0].x
        for i in range(len(verts)):
            x = verts[i].x
            if x > highestXCoord:
                highestXCoord = x
                rightMost = i
            elif x == highestXCoord:
                if verts[i].y < verts[rightMost].y:
                    rightMost = i
        
        hull = [0] * Polygon.MAX_POLY_VERTEX_COUNT
        outCount = 0
        indexHull = rightMost
        nextHullIndex = 0
        
        while True:
            hull[outCount] = indexHull
            nextHullIndex = 0
            for i in range(len(verts)):
                if nextHullIndex == indexHull:
                    nextHullIndex = i
                    continue
                
                e1 = verts[nextHullIndex] - verts[hull[outCount]]
                e2 = verts[i] - verts[hull[outCount]]
                c = cross(e1, e2)
                if  c < 0:
                    nextHullIndex = i
                    
                if c == 0 and e2.lengthSq() > e1.lengthSq():
                    nextHullIndex = i
                    
            outCount += 1
            
            indexHull = nextHullIndex
            
            if nextHullIndex == rightMost:
                self.vertexCount = outCount
                break
        
        #copy vertices into shape's vertices
        #print(verts)
        #print("len verts:", len(verts))
        #print("vertexCount:", self.vertexCount)
        
        for i in range(self.vertexCount):
            #print("i:", i)
            self.vertices.append(Vec2( verts[hull[i]]))
            
        # Compute face normals    
        for i in range(self.vertexCount):
            face = self.vertices[(i+1)%self.vertexCount] - self.vertices[i]
            self.normals.append(Vec2(face.y, -face.x))
            self.normals[i].normalize()
    
    def setBox(self, hw, hh):
        self.vertexCount = 4
        self.vertices.append(Vec2(-hw, -hh))
        self.vertices.append(Vec2(hw, -hh))
        self.vertices.append(Vec2(hw, hh))
        self.vertices.append(Vec2(-hw, hh))
        self.normals.append(Vec2(0, -1))
        self.normals.append(Vec2(1, 0))
        self.normals.append(Vec2(0, 1))
        self.normals.append(Vec2(-1, 0))
        
    def computeMass(self, density, body):
        centroid = Vec2()
        area = 0 
        triangleArea = 0
        inertia = 0
        k_inv6 = 1.0 / 6
        
        #count centroid and inertia
        for i in range(self.vertexCount):
            p1 = self.vertices[i]
            p2 = self.vertices[ (i+1) % self.vertexCount]
            
            D = cross(p1, p2)
            triangleArea = 0.5 * D
            
            area += triangleArea
            #print(area)
            centroid += (p1 * D)
            centroid += (p2 * D)
            
            intx2 = p1.x ** 2 + p2.x * p1.x + p2.x ** 2
            inty2 = p1.y ** 2 + p2.y * p1.y + p2.y ** 2
            inertia += (0.5 * k_inv6 * D) * (intx2+ inty2)
            
        centroid =  centroid * k_inv6 / area
        
        #translate vertices to centroid
        for i in range(self.vertexCount):
            self.vertices[i] -= centroid
            
        body.mass = density * area
        body.invMass = 1 / body.mass if  body.mass else 0
        body.inertia = inertia * density
        body.invInertia = 1 / body.inertia if  body.inertia else 0
        
        self.body = body
        #print(body.mass, body.invMass, body.inertia, body.invInertia)
    
    def getSupport(self, dir):
        bestProjection = - 1000000
        bestVertex = None
        
        for i in range(self.vertexCount):
            v = self.vertices[i]
            projection = dot(v, dir)
            if projection > bestProjection:
                bestVertex = v
                bestProjection = projection
        return bestVertex
    
    def setOrient(self, radians):
        self.u.set(radians)