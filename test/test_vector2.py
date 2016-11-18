import unittest
from impulse_engine.vector2 import Vec2

class Vec2Test(unittest.TestCase):
    def setUp(self):
        self.v1 = Vec2(3,5)
        self.v2 = Vec2(4,6)

    def test_create_vector_by_component(self):
        tmp = Vec2(-5, 8)
        self.assertEqual(tmp.x , -5)
        self.assertEqual(tmp.y , 8)
        
    def test_create_vector_by_vector(self):
        tmp = Vec2(self.v1)
        self.assertEqual(tmp.x , self.v1.x)
        self.assertEqual(tmp.y , self.v1.y)
        
    def test_negative_vector(self):
        tmp = - self.v1
        self.assertEqual(self.v1.x , -tmp.x, "negative x component")
        self.assertEqual(self.v1.y , -tmp.y, "negative y component")
    
    def test_vector_multiply_scalar(self):
        tmp = self.v1 * 5
        self.assertEqual(tmp.x, self.v1.x*5, "multiply x component by scalar 5")
        self.assertEqual(tmp.y, self.v1.y*5, "multiply y component by scalar 5")
        
    def test_vector_multiply_vector(self):
        tmp = self.v1 * self.v2
        self.assertEqual(tmp.x, self.v1.x * self.v2.x , "vector mul vector x component")
        self.assertEqual(tmp.y, self.v1.y * self.v2.y , "vector mul vector y component")
        
    def test_vector_multiply_scalar_in_place(self):
        tmp = Vec2(self.v1)
        tmp *= 9 
        self.assertEqual(tmp.x , self.v1.x * 9)
        self.assertEqual(tmp.y , self.v1.y * 9)
    
    def test_vectoer_multiply_vector_in_place(self):
        tmp = Vec2(self.v1)
        tmp *= self.v2
        self.assertEqual(tmp.x, self.v1.x * self.v2.x)
        self.assertEqual(tmp.y, self.v1.y * self.v2.y)
        
if __name__ == '__main__':
    unittest.main()
    
    
    
    