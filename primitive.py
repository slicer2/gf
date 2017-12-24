# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 15:55:19 2017

@author: danz
"""                                                 

from gfp import gfp
def enumerateMonicPoly(p, n):
    """ Enumerate all monic polynomials """
    mSet = []
    pSet = [[i] for i in range(p)]
    
    for _n in range(2, n+1):
        _pSet = []
        for j in range(0, p):
            _pSet.extend([[j] + pSet[k] for k in range(len(pSet))])
            
        _mSet = []
        _mSet.extend([[1] + pSet[k] for k in range(len(pSet))])
        
        mSet.extend(_mSet)
        
        pSet = _pSet
    
    return mSet
    
def polyInt(p, poly):
    """ Convert a polynomial to a p-ary integer """
    myInt = poly[0]
    for j in range(1, len(poly)):
        myInt = myInt * p + poly[j]
        
    return myInt

def irreduciblePoly(p, n):
    """ irreducible polynomials of characteristic-p up to order n-1 """
    assert n >= 2
    mPoly = enumerateMonicPoly(p, n)
    mPrime = [True for i in range(len(mPoly))]
    mPolyIdx = {polyInt(p, mPoly[j]):j for j in range(len(mPoly))}
    iPoly = []
    
    for i in range(len(mPoly)):
        if mPrime[i]:
            for j in range(i, len(mPoly)):
                prod = gfp._conv(mPoly[i], mPoly[j])
                if len(prod) > n:
                    continue
                
                pProd = [prod[k] % p for k in range(len(prod))]
                mPrime[mPolyIdx[polyInt(p, pProd)]] = False
            
            iPoly.append(mPoly[i])
            
    return iPoly

def primitivePoly(p, n):
    """ primitive polynomials of characteristic-p of order n-1 """
    iPoly = irreduciblePoly(p, n + 1)
    #print(iPoly)
    candidates = [gfp(p, v) for v in iPoly if len(v) == n + 1]
    #print(candidates)
    fieldPoly = [0 for i in range(p**n)]
    fieldPoly[0], fieldPoly[-1] = 1, -1
    fieldPoly = gfp(p, fieldPoly)
    #print(fieldPoly)
    
    pPoly = []
    for i in range(len(candidates)):
        q, r = fieldPoly.deconv(candidates[i])
        if r == gfp(p):
            pPoly.append(candidates[i])
    
    return pPoly

if __name__ == '__main__':
    print("enumerateMonicPoly(2, 1)")
    print(enumerateMonicPoly(2, 1))
    
    print("enumerateMonicPoly(2, 2)")
    print(enumerateMonicPoly(2, 2))
    
    print("enumerateMonicPoly(2, 3)")
    print(enumerateMonicPoly(2, 3))
    
    print("enumerateMonicPoly(2, 4)")
    print(enumerateMonicPoly(2, 4))
    
    print("enumerateMonicPoly(3, 2)")
    print(enumerateMonicPoly(3, 2))
    
    print("enumerateMonicPoly(3, 3)")
    print(enumerateMonicPoly(3, 3))
    
    print("polyInt(2, [1, 0])")
    print(polyInt(2, [1, 0]))
    
    print("polyInt(2, [1, 1, 0])")
    print(polyInt(2, [1, 1, 0]))
    
    
    print("polyInt(3, [1, 0, 1])")
    print(polyInt(3, [1, 0, 1]))
    
    print("irreduciblePoly(2, 2)")
    print(irreduciblePoly(2, 2))
    
    print("irreduciblePoly(2, 3)")
    print(irreduciblePoly(2, 3))
    
    
    print("irreduciblePoly(2, 4)")
    print(irreduciblePoly(2, 4))
    
    print("irreduciblePoly(2, 5)")
    print(irreduciblePoly(2, 5))
    
    print("irreduciblePoly(2, 6)")
    print(irreduciblePoly(2, 6))
    
    print("irreduciblePoly(2, 8)")
    print(irreduciblePoly(2, 8))
    
    
    print("irreduciblePoly(3, 3)")
    print(irreduciblePoly(3, 3))
    
    print("irreduciblePoly(3, 5)")
    print(irreduciblePoly(3, 5))
    
    print("primitivePoly(2, 2)")
    print(primitivePoly(2, 2))
    
    print("primitivePoly(2, 3)")
    print(primitivePoly(2, 3))
    
    print("primitivePoly(2, 8)")
    print(primitivePoly(2, 8))
    
    
    print("primitivePoly(7, 3)")
    print(primitivePoly(7, 3))