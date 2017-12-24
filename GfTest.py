# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 22:30:10 2017

@author: danz
"""
import unittest
from gf import gf

class GfTest(unittest.TestCase):
    def test__init__(self):
        t = gf(2, 8, 0, 'GF256add.txt')
        self.assertEqual(t.order, 256)
        self.assertIn(256, t.additionTable)
        
    def test__mul__(self):
        t1 = gf(2, 8, [0])
        t2 = gf(2, 8, [0])
        self.assertEqual(t1 * t2, gf(2, 8, 0))
        
        t1 = gf(2, 8, [0])
        t2 = gf(2, 8, [2])
        self.assertEqual(t1 * t2, gf(2, 8, 2))
        
        t1 = gf(2, 8, [1])
        t2 = gf(2, 8, [2])
        self.assertEqual(t1 * t2, gf(2, 8, 3))
        
        t1 = gf(2, 8, [127])
        t2 = gf(2, 8, [128])
        self.assertEqual(t1 * t2, gf(2, 8, 0))
        
        t1 = gf(2, 8, [255])
        t2 = gf(2, 8, [1])
        self.assertEqual(t1 * t2, gf(2, 8, 255))
        
if __name__ == '__main__':
    unittest.main()