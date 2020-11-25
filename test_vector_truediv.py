import numpy as np
from random import random as rnd

class Vector(list):
    def __init__(self,*el):
        for l in el:
            self.append(l)
    
    def __truediv__(self, other):
        ''' 
        Задаем операцию векторного умножения x/y
        '''
        r=Vector(*[0 for i in range(len(self))])
        for i in range(len(self)):
            if i != len(self)-2 : 
                r[(i+2)%len(self)]=(-1)**i*(self[i] * other[(i+1) % len(self)]
                                        -self[(i+1) % len(self)] * other[i])
            else: 
                r[(i+2)%len(self)]=(-1)**(i+1)*(self[i] * other[(i+1)%len(self)]
                                        -self[(i+1) % len(self)] * other[i])
        return r


if __name__ == "__main__":
    L = 50
    N = 100
    vecs = [Vector((rnd()-0.5)*L, (rnd()-0.5)*L, (rnd()-0.5)*L) for i in range(N)]
    np_vecs = [np.array(vector) for vector in vecs]

    for i in range(N):
        for j in range(N):
            if any(np.cross(np_vecs[i], np_vecs[j]) != Vector.__truediv__(vecs[i], vecs[j])):
                print (vecs[i], vecs[j], i, j)
            else:
                print ('OK')



