import math

class NotImplement(Exception):pass

class Vec2:
    def __init__(self, a=0, b=0):
        if isinstance(a, Vec2):
            self.set(a)
        else:
            self.set(a, b)

    def set(self, a, b=0):
        if isinstance(a, Vec2):
            self.x = a.x
            self.y = a.y
        else:
            self.x = a
            self.y = b
            
    def __neg__(self):
        return Vec2(-self.x , -self.y)
        
    def __repr__(self):
        return "Vec2(x={},y={})".format(self.x, self.y)
        
    def __mul__(self, other):
        if isinstance(other, Vec2):
            v = Vec2()
            v.x  = self.x * other.x
            v.y  = self.y * other.y
            return v
        else:
            return Vec2(self.x*other, self.y*other)
        
    def __imul__(self, other):
        if isinstance(other, Vec2):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
        return self  
        
    def __add__(self, other):
        if not isinstance(other, Vec2):
            raise NotImplement
        v = Vec2()
        v.x = self.x + other.x
        v.y = self.y + other.y
        return v
        
    def __iadd__(self, other):
        if not isinstance(other, Vec2):
            raise NotImplement 
    
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        if not isinstance(other, Vec2):
            raise NotImplement
        v = Vec2()
        v.x = self.x - other.x
        v.y = self.y - other.y
        return v

    def __isub__(self, other):
        if not isinstance(other, Vec2):
            raise NotImplement 
    
        self.x -= other.x
        self.y -= other.y
        return self 

    def __truediv__(self, other):
        v = Vec2()
        v.x = self.x / other
        v.y = self.y / other
        return v
        
    def __itruediv__(self, other):
        self.x /= other
        self.y /= other
        return self
    
    def lengthSq(self):
        return self.x ** 2 + self.y ** 2
        
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
        
    def normalize(self, epsilonSq=0.000001):
        lenSq = self.lengthSq()
                
        if lenSq > epsilonSq :
            invLen = 1/math.sqrt(lenSq)
            self.x *= invLen
            self.y *= invLen
    


        

def dot(a, b):
        if not isinstance(a, Vec2) or not isinstance(b, Vec2) :
            raise NotImplement
        
        return a.x * b.x + a.y * b.y 

        
def cross(a, b):
        a_is_vector = isinstance(a, Vec2)
        b_is_vector = isinstance(b, Vec2)
        if not a_is_vector and not b_is_vector :
            raise NotImplement       
        elif a_is_vector and b_is_vector:
            return a.x * b.y - a.y * b.x          
        elif a_is_vector and not b_is_vector:
            return Vec2(a.y * b, a.x * -b)
        elif not a_is_vector and b_is_vector:
            return Vec2(b.y * -a, b.x * a)
        
def distanceSq(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    
    return dx**2 + dy**2

        
        
if __name__ == '__main__':
    print("In main")