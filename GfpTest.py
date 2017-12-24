# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 10:10:31 2017
Unit tests for gfp
@author: danz
"""

import unittest
from gfp import gfp

class GfpTest(unittest.TestCase):
    def test__init__(self):
        t = gfp(2, 1)
        #self.assertRaises(ValueError, gfp, 2, [])
        t = gfp(2, 0)
        t = gfp(3, [1])
        t = gfp(3, [1, 2, 0])
        t = gfp()
        t = gfp(3, [1, -1])
       
    def testNonPrimeCharacteristic(self):
        self.assertRaises(ValueError, gfp, 4, [1])
        self.assertRaises(ValueError, gfp, 6, [1])
        
    def testInvTable(self):
        t = gfp(2)
        self.assertEqual(t.invTable, [0, 1])
        t = gfp(3)
        self.assertEqual(t.invTable, [0, 1, 2])
        t = gfp(7)
        self.assertEqual(t.invTable, [0, 1, 4, 5, 2, 3, 6])
        
    def testInv(self):
        t = gfp(2)
        self.assertEqual(t.inv(1), 1)
        self.assertRaises(ValueError, t.inv, 0)
        
        t = gfp(7)
        self.assertEqual(t.inv(6), 6)
        self.assertEqual(t.inv(3), 5)
        
    def testConv(self):
        t1 = gfp(2, [1, 0, 1])
        t2 = gfp(2, [1, 1, 0])
        self.assertEqual(t1.conv(t2), gfp(2, [1, 1, 1, 1, 0]))
        t1 = gfp(2, [0, 0, 1])
        self.assertEqual(t1.conv(t2), gfp(2, [0, 0, 1, 1, 0]))
        
        t1 = gfp()
        t2 = gfp(2, [1, 0, 1])
        self.assertEqual(t1.conv(t2), gfp())
        
    def testProper(self):
        t1 = gfp(2, [0, 0, 1, 0])
        self.assertEqual(t1.proper(), gfp(2, [1, 0]))
        t1 = gfp()
        self.assertEqual(t1, gfp(2, [0]))
        t1 = gfp(2)
        self.assertEqual(t1, gfp(2, [0]))
        t1 = gfp(2, [0])
        self.assertEqual(t1, gfp())
        t1 = gfp(2, [0, 0])
        self.assertEqual(t1, gfp())
        t1 = gfp(3, [1, -1])
        t2 = gfp(3, [1, 2])
        self.assertEqual(t1, t2)
    
    def testPolySub(self):
        t1 = gfp(3, [1, 0, 2])
        t2 = gfp(3, [1, 1])
        self.assertEqual(t1.polySub(t2), gfp(3, [1, 2, 1]))
        
        t1 = gfp(2, [0, 1, 0])
        t2 = gfp(2, [1, 0, 0, 1])
        self.assertEqual(t1.polySub(t2), gfp(2, [1, 0, 1, 1]))
        
        t1 = gfp(7, [3, 1, 4, 1])
        t2 = gfp(7, [5, 2, 6, 0, 2])
        self.assertEqual(t1.polySub(t2), gfp(7, [2, 1, 2, 4, 6]))
        
    def testMonic(self):
        t1 = gfp(3, [2, 0, 1])
        self.assertEqual(t1.monic(), gfp(3, [1, 0, 2]))
        t1 = gfp(3, [0, 0])
        self.assertRaises(ValueError, t1.monic)
        t1 = gfp(7, [2, 3, 2, 6])
        self.assertEqual(t1.monic(), gfp(7, [1, 5, 1, 3]))
        
    def testDeconv(self):
        t1 = gfp(2, [1, 0, 1, 1])
        t2 = gfp(2, [0, 1, 1])
        self.assertEqual(t1.deconv(t2), (gfp(2, [1, 1, 0]), gfp(2, [1])))
        
        t1 = gfp(2, [1, 0, 1, 0, 0, 0, 1])
        t2 = gfp(2, [1, 0, 1, 0, 1])
        self.assertEqual(t1.deconv(t2), (gfp(2, [1, 0, 0]), gfp(2, [1, 0, 1])))
        
        t1 = gfp(2, [1, 1, 0])
        t2 = gfp(2, 1)
        self.assertEqual(t1.deconv(t2), (gfp(2, [1, 1, 0]), gfp()))
        
        t1 = gfp(2, [1, 1, 0])
        t2 = gfp()
        self.assertRaises(ZeroDivisionError, t1.deconv, t2)
        
        t1 = gfp(7, [3, 1, 4, 1, 5, 2])
        t2 = gfp(7, [2, 3, 5])
        self.assertEqual(t1.deconv(t2), (gfp(7, [5, 0, 0, 4]), gfp(7, 3)))
        
        t1 = gfp()
        t2 = gfp(2, [1, 1])
        self.assertEqual(t1.deconv(t2), (gfp(), gfp()))
        
        

if __name__ == '__main__':
    unittest.main()