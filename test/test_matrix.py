import unittest
import math

from impulse_engine.matrix import Mat2, NotImplement
from impulse_engine.vector import Vec2

class Mat2Test(unittest.TestCase):

    def setUp(self):
        self.ma = Mat2()
        self.ma.m00 = 1
        self.ma.m01 = 2
        self.ma.m10 = 3
        self.ma.m11 = 4
        
        self.va = Vec2(5,10)
        
    def test_set(self):
        m = Mat2()
        m.set(0)
        self.assertEqual(m.m00, 1)
        self.assertEqual(m.m01, 0)
        self.assertEqual(m.m10, 0)
        self.assertEqual(m.m11, 1)
        
    def test_transpose(self):
        result = self.ma.transpose()
        self.assertEqual(result.m00, 1)
        self.assertEqual(result.m01, 3)
        self.assertEqual(result.m10, 2)
        self.assertEqual(result.m11, 4)
        
    def test_multiply(self):
        with self.assertRaises(NotImplement):
            self.ma * 5
        
        with self.assertRaises(NotImplement):
            self.ma * Mat2()
            
        result = self.ma * self.va    
        self.assertEqual(result.x , 25)
        self.assertEqual(result.y , 55)
            
        
        
        
if __name__ == '__main__':
    unittest.main()
    