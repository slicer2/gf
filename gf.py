# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 15:37:19 2017

@author: danz
"""

from primitive import enumerateMonicPoly, primitivePoly
from gfp import gfp

class gf:
    additionTable = dict()
    def __init__(self, p = 2, n = 1, v = 0, addTableFile = None):
        self.p = p
        self.n = n
        self.order = p**n
        if not self.order in self.additionTable:
            if addTableFile:
                self.additionTable[self.order] = gf.loadAdditionTable(addTableFile)
            else:
                self.generator = primitivePoly(p, n)[0]
                self.additionTable[self.order] = self.generateAdditionTable(p, n, self.generator)
        
        if isinstance(v, int):
            self.v = [v % self.order]
        else:
            self.v = [e % self.order for e in v]
    
    def __add__(self, other):
        if not self.order == other.order:
            raise TypeError("Cannot add vectors from different fields")
        
        v, ov = self.v, other.v
        
        if not len(v) == len(ov):
            if len(v) == 1:
                v = [v[0] for i in range(len(ov))]
            elif len(other.v) == 1:
                ov = [ov[0] for i in range(len(v))]
            else:
                raise ValueError("Vectors to be multiplied elementwise must have equal length")
            
        v = [self.additionTable[self.order][v[i]][ov[i]] \
             for i in range(len(v)) ]
        
        return gf(self.p, self.n, v)
    
    def __mul__(self, other):
        if not self.order == other.order:
            raise TypeError("Cannot multiply vectors from different fields")
        
        v, ov = self.v, other.v
        
        if not len(v) == len(ov):
            if len(v) == 1:
                v = [v[0] for i in range(len(ov))]
            elif len(other.v) == 1:
                ov = [ov[0] for i in range(len(v))]
            else:
                raise ValueError("Vectors to be multiplied elementwise must have equal length")
            
        prod = [(v[i] + ov[i]) % (self.order - 1) \
                if (not v[i] == self.order - 1) and (not ov[i] == self.order - 1) \
                else self.order - 1 \
                for i in range(len(v))]
        
        return gf(self.p, self.n, prod)
    
    def __eq__(self, other):
        return self.order == other.order and self.v == other.v
    
    @staticmethod
    def loadAdditionTable(addTableFile):
        table = []
        with open(addTableFile, encoding = 'utf-8') as a_file:
            for a_line in a_file:
                fields = a_line.split()
                table.append([int(e) for e in fields])
                
        return table
    
    @staticmethod
    def generateAdditionTable(p, n, genPoly):
        cyclicGroup = gf.findPrimitiveElement(p, n, genPoly)
        elem = cyclicGroup + [gfp(p)]
#        generator = gfp(p, [1, 1])
#        elem = [gfp(p, 1), generator]
#        order = p**n
#        for i in range(2, order - 1):
#            nextPoly = elem[-1].conv(generator)
#            q, r = nextPoly.deconv(genPoly)
#            print(r)
#            if r in elem:
#                print('stop')
#            elem.append(r)
#            
#        elem.append(gfp(p))
        
        addTab = []
        order = p**n
        for i in range(order):
            addTab.append([elem.index(elem[i].polyAdd(elem[j])) for j in range(order)])
            
        return addTab
    
    @staticmethod
    def findPrimitiveElement(p, n, genPoly):
        mPoly = [gfp(p, v) for v in enumerateMonicPoly(p, n)]
        order = p**n
        isPrimitive = [True for i in range(order - 2)]
        cyclicGroup = [gfp(p, [1])]
        i = 0
        
        while len(cyclicGroup) < order - 1:
            cyclicGroup = [gfp(p, [1])]
            
            while not isPrimitive[i]:
                i += 1
                
            nextPoly = mPoly[i]
            while not nextPoly == cyclicGroup[0]:
                isPrimitive[mPoly.index(nextPoly)] = False
                cyclicGroup.append(nextPoly)
                dummy, nextPoly = nextPoly.conv(mPoly[i]).deconv(genPoly)
                
        return cyclicGroup
    
    def __repr__(self):
        return self.v.__repr__()
    
    def polyVal(self, poly):
        if not self.p == poly.p or not self.n == poly.n:
            raise TypeError("Polynomial coefficients must lie in the same field with variable")
            
        val = gf(self.p, self.n, 0)
        for e in poly.v:
            val = val * self + gf(self.p, self.n, e)
            
        return val
            
if __name__ == '__main__':
#    t = gf(2, 8)
#    with open('GF256add.txt', mode='w', encoding='utf-8') as a_file:
#        table = t.additionTable[256]
#        for line in table:
#            for e in line:
#                a_file.write(str(e) + ' ')
#            a_file.write('\n')
    
    t = gf(2, 8, 0, addTableFile = 'GF256add.txt')
    t = gf(2, 8, 0)
    t1 = gf(2, 8, 1)
    t2 = gf(2, 8, 2)
    t = t1 + t2
    t1 = gf(2, 8, [3, 7, 13, 101, 5, 0])
    t2 = gf(2, 8, [4, 11, 22, 200, 203])
    t = t1.polyVal(t2)