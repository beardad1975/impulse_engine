
from vector import Vec2

EPSILON = 0.0001
EPSILON_SQ = EPSILON ** 2.0
FPS = 30
DT = 1.0 / FPS 
GRAVITY = Vec2(0,500) # downward
RESTING = (GRAVITY*DT).lengthSq() #+ 30
RESTITUTION = 0.2
BIAS_RELATIVE = 0.95
BIAS_ABSLUTE = 0.01
PENETRATION_ALLOWANCE = 0.01
PENETRATION_CORRECTION = 0.4



def gt (a, b):
    return a >= b * BIAS_RELATIVE + a * BIAS_ABSLUTE
    
def equal(a, b):
    return abs( a-b) <= EPSILON
    
