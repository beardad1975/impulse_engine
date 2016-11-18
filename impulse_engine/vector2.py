

class Vec2:
    def __init__(self, a=0, b=0):
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
        
if __name__ == '__main__':
    print("In main")