"""
Finite field class that implements GF(q) where q is prime
Support element wise arithmetic and polynomial arithmetic
Oct 31 2017
danz
"""


class gfp:
    @staticmethod
    def isPrime(x):
        return all(x % i for i in range(2, x))
    
    def __init__(self, p = 2, v = 0):
        if v == []:
            v = 0
            
        if not self.isPrime(p):
            raise ValueError("Characteristic p must be a prime")
            
        self.p = p
        if isinstance(v, int):
            self.v = [elem % p for elem in [v]]
        else:
            self.v = [elem % p for elem in v]
        
        self.invTable = [0 for i in range(p)]
        for i in range(1, p):
            invVal = 1
            for j in range(p-2):
                invVal = (invVal * i) % p
                
            assert (i * invVal) % p == 1
            self.invTable[i] = invVal
            
        # make it proper
        self.v = self.dropLeadingZero(self.v)
        if self.v == []:
            self.v = [0]

    def __hash__(self):
        return hash(str(self.p) + str(self.dropLeadingZero(self.v)))
                    
    def __add__(self, other):
        if self.p == other.p and len(self.v) == len(other.v):
            return gfp(self.p, [(self.v[i] + other.v[i]) % self.p for i in range(len(self.v))])
        else:
            raise TypeError("Cannot add two vectors from different fields or of different length")
            
    def __sub__(self, other):
        if self.p == other.p and len(self.v) == len(other.v):
            return gfp(self.p, [(self.v[i] - other.v[i]) % self.p for i in range(len(self.v))])
        else:
            raise TypeError("Cannot subtract two vectors from different fields or of different lengthh")
            
    def __mul__(self, other):
        if self.p == other.p and len(self.v) == len(other.v):
            return gfp(self.p, [(self.v[i] * other.v[i]) % self.p for i in range(len(self.v))])
        else:
            raise TypeError("Cannot multiply two vectors from different fields")
            
    def __truediv__(self, other):
        if self.p == other.p and len(self.v) == len(other.v):
            return gfp(self.p, [(self.v[i] * self.inv(other.v[i])) % self.p for i in range(len(self.v))])
        else:
            raise TypeError("Cannot divide two vectors from different fields")
    
    def __neg__(self):
        return gfp(self.p, [-e for e in self.v])
    
    def __eq__(self, other):
        if self.p == other.p:
            left = self.proper()
            right = other.proper()
            return left.v == right.v
        else:
            return False
    
    def polyAdd(self, other):
        if self.p == other.p:
            if len(self.v) >= len(other.v):
                delta = len(self.v)-len(other.v)
                return gfp(self.p, self.v[0:delta] + [(self.v[delta + j] + other.v[j]) % self.p for j in range(len(other.v))])
            else:
                delta = len(other.v)-len(self.v)
                return gfp(self.p, other.v[0:delta] + [(other.v[delta + j] + self.v[j]) % self.p for j in range(len(self.v))])
        else:
            raise TypeError("Cannot add two polynomials with coefficients from differnet fields")
    
    def polySub(self, other):
        return self.polyAdd(-other)
        
    def inv(self, val):
        if val == 0:
            raise ValueError("Division by zero.")
        else:
            return self.invTable[val]
        
    def __repr__(self):
        return self.v.__repr__()
    
    def copy(self):
        return gfp(self.p, self.v)
    
    @staticmethod
    def _conv(v1, v2):
        """ regular poly conv without notion of finite field """
        ret = []
        for i in range(len(v1) + len(v2) - 1):
            s = 0
            for j in range(max(0, i - len(v2) + 1), min(i, len(v1) - 1) + 1):
                s += v1[j] * v2[i-j]    
            ret.append(s)
            
        return ret
                
    def conv(self, other):
        if self.p == other.p:
            return gfp(self.p, self._conv(self.v, other.v))
        else:
            raise TypeError("Cannot convolve two vectors from different fields")
            
    def deconv(self, other):
        if self.p == other.p:
            v = self.proper().v
            t = other.proper().v
            if t == [0]:
                raise ZeroDivisionError("deconv divisor cannot be empty (zero)")
              
            q = []
            qLen = len(v) - len(t) + 1
            for i in range(qLen):
                qElem = (v[i] * self.invTable[t[0]]) % self.p
                for j in range(len(t)):
                    v[i+j] = (v[i+j] - t[j] * qElem) % self.p
                    
                q.append(qElem)
                
            if len(t) > 1:
                return (gfp(self.p, q), gfp(self.p, v[-len(t)+1:]))
            else:
                return (gfp(self.p, q), gfp(self.p))
        else:
            raise TypeError("Cannot deconvolve two vectors from different fields")
            
    def isZero(self):
        return self.v == [0 for i in len(self.v)]
    
    def monic(self):
        newSelf = self.proper()
        if not newSelf.isEmpty():
            leadingInv = newSelf.inv(newSelf.v[0])
            for j in range(len(newSelf.v)):
                newSelf.v[j] = (newSelf.v[j] * leadingInv) % newSelf.p
        else:
            raise ValueError("Cannot convert to monic")
            
        return newSelf
            
    def proper(self):
        v = self.dropLeadingZero(self.v)
        if v == []:
            v = [0]
            
        return gfp(self.p, v)
    
    @staticmethod
    def dropLeadingZero(v):
        for i in range(len(v)):
            if v[0] == 0:
                v.pop(0)
            else:
                break
            
        return v
    
    def isEmpty(self):
        return not self.v
    
    def __getitem__(self, key):
        if not isinstance(key, int):
            raise TypeError("gfp can only be indexed by integers")
            
        if key >= len(self.v):
            raise IndexError("gfp index out of bound")
            
        return self.v[key]
    
    
    
if __name__ == '__main__':
    v = gfp()
    v1 = gfp(7, [3, 4, 5, 2, 1])
    v2 = gfp(7, [2, 5, 1, 6, 4])
    v = v1 / v2
    print(v)
    
    v1 = gfp(2, [1, 0, 1])
    v2 = gfp(2, [1, 0, 1])
    v = v1.conv(v2)
    print(v)
    
    b = gfp(2, 1)
    
    t1 = gfp(2, [1, 0, 1, 1])
    t2 = gfp(2, [0, 1, 1])
    t1.deconv(t2)
    
    t1 = gfp(3, [1, 0, 2])
    t2 = gfp(3, [1, 1])
    t = t1.polyAdd(t2)
    
    t1 = gfp()
    t2 = gfp(2, [1, 1])
    q, r = t1.deconv(t2)