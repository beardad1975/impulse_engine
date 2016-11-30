import unittest
import math

from impulse_engine.vector import Vec2
from impulse_engine.vector import NotImplement
from impulse_engine.vector import dot, cross 

class Vec2Test(unittest.TestCase):
    def setUp(self):
        self.v1 = Vec2(-30,5)
        self.v2 = Vec2(19,60)

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

    def test_vector_add_vector(self):
        tmp = self.v1 + self.v2
        self.assertEqual(tmp.x, self.v1.x + self.v2.x)
        self.assertEqual(tmp.y, self.v1.y + self.v2.y)

        with self.assertRaises(NotImplement):
            tmp = tmp + 5

    def test_vector_add_vector_in_place(self):
        tmp = Vec2(self.v1)
        tmp += self.v2
        self.assertEqual(tmp.x, self.v1.x + self.v2.x)
        self.assertEqual(tmp.y, self.v1.y + self.v2.y)
        
        with self.assertRaises(NotImplement):
            tmp += 5

    def test_vector_subtract_vector(self):
        tmp = self.v1 - self.v2
        self.assertEqual(tmp.x, self.v1.x - self.v2.x)
        self.assertEqual(tmp.y, self.v1.y - self.v2.y)

        with self.assertRaises(NotImplement):
            tmp = tmp - 5

    def test_vector_subtract_vector_in_place(self):
        tmp = Vec2(self.v1)
        tmp -= self.v2
        self.assertEqual(tmp.x, self.v1.x - self.v2.x)
        self.assertEqual(tmp.y, self.v1.y - self.v2.y)
        
        with self.assertRaises(NotImplement):
            tmp -= 5

    def test_lengthSq(self):
        tmp = self.v1.lengthSq()
        self.assertEqual(tmp, self.v1.x ** 2 + self.v1.y **2)
        
        
         
    def test_length(self):
        tmp = self.v1.length()
        self.assertEqual(tmp, math.sqrt(self.v1.x ** 2 + self.v1.y **2)) 

                    
        length = Vec2(3,4).length()
        self.assertEqual(length, 5)

    def test_normalize(self):
        tmp = Vec2(self.v1)
        tmp.normalize()
        
        #test with round to 8 digital 
        length = self.v1.length()   
        self.assertEqual( round(tmp.x, 8), 
            round(self.v1.x / length, 8))
        self.assertEqual( round(tmp.y, 8), 
            round(self.v1.y / length, 8))
        
        #test small than epsilon
        tmp2 = Vec2(0.0001, 0.0002)
        tmp2.normalize()
        self.assertEqual(tmp2.x, 0.0001)
        self.assertEqual(tmp2.y, 0.0002)
        
    def test_vector_dot(self):
        i = Vec2(5, 4)
        j = Vec2(3, 7)
        result = dot(i, j)
        self.assertEqual(result, 5*3 + 4*7)
        
    def test_vector_cross(self):
        i = Vec2(5, 4)
        j = Vec2(5, 3)
        result = cross(i, j)
        self.assertEqual(result, 5*3 - 4*5)
        
        result = cross(i, 10)
        self.assertEqual(result.x, i.y * 10 )
        self.assertEqual(result.y, i.x * -10)
        
        result = cross(10, i)
        self.assertEqual(result.x, i.y * -10)
        self.assertEqual(result.y, i.x * 10)
        
    def test_set(self):
        tmp = Vec2()
        tmp.set(3, 7)
        self.assertEqual(tmp.x, 3)
        self.assertEqual(tmp.y, 7)
        
        tmp2 = Vec2()
        tmp2.set(tmp)
        self.assertEqual(tmp2.x, tmp.x)
        self.assertEqual(tmp2.y, tmp.y)
    
    def test_vector_divide(self):
        tmp = Vec2(12, 16)
        result = tmp / 4
        self.assertEqual(result.x, 3)
        self.assertEqual(result.y, 4)
        
        tmp /= 4
        self.assertEqual(tmp.x, 3)
        self.assertEqual(tmp.y, 4)
        
if __name__ == '__main__':
    unittest.main()
    
    
    
    