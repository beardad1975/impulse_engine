
from vector import Vec2

EPSILON = 0.0001
DT = 0.02 # 1/50
GRAVITY = Vec2(0, -500)  # downward
RESTING = (GRAVITY*DT).lengthSq() #+ 30
RESTITUTION = 0.2