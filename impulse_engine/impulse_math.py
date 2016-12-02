
from vector import Vec2

EPSILON = 0.0001
EPSILON_SQ = EPSILON ** 2.0
FPS = 30
DT = 1.0 / 20 
GRAVITY = Vec2(0,200) # downward
RESTING = (GRAVITY*DT).lengthSq() #+ 30
RESTITUTION = 0.3
BIAS_RELATIVE = 0.95
BIAS_ABSLUTE = 0.01
PENETRATION_ALLOWANCE = 0.05
PENETRATION_CORRECTION = 0.6
STATIC_FRICTION = 0.5
DYNIMIC_FRICTION =  0.3


def gt (a, b):
    return a >= b * BIAS_RELATIVE + a * BIAS_ABSLUTE
    
def equal(a, b):
    return abs( a-b) <= EPSILON
    
