import math
from vector import Vec2

class NotImplement(Exception):pass


class Mat2:

    def __init__(self):
        self.m00 = 0
        self.m01 = 0
        self.m10 = 0
        self.m11 = 0
        
    def set(self, radians):
        c = math.cos(radians)
        s = math.sin(radians)
        
        self.m00 = c
        self.m01 = -s
        self.m10 = s
        self.m11 = c
        
    def transpose(self):
        out = Mat2()
        out.m00 = self.m00
        out.m01 = self.m10
        out.m10 = self.m01
        out.m11 = self.m11
        return out
        
    def __mul__(self, other):
        if not isinstance(other, Vec2):
            raise NotImplement
            
        out = Vec2()
        out.x = self.m00 * other.x + self.m01 * other.y 
        out.y = self.m10 * other.x + self.m11 * other.y
        return out
        
        
        
        
        
        