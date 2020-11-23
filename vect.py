import matplotlib.pyplot as plt
from random import *
import numpy as np
from matplotlib.animation import *
class Vector(list):
    def __init__(self,*el):
        for l in el:
            self.append(l)

    def __add__(self,other):
        r=Vector()
        for i in range(len(self)):
            r.append(self[i] + other[i])
        return r

    def __sub__(self, other):
        r = Vector()
        for i in range(len(self)):
            r.append(self[i] - other[i])
        return r

    def __mod__(self, other):
        r=0
        for i in range(len(self)):
            r+=(self[i]-other[i]) ** 2
        return r**0.5

    def __mul__(self, other):
        r=Vector()
        for i in range(len(self)):
            r.append(self[i]*other)
        return r

    def __abs__(self):
        r=0
        for i in range(len(self)):
            r+=self[i]**2
        return r**0.5

    def __truediv__(self, other):
        ''' Задаем операцию векторного умножения x/y'''
        r=Vector(*[0 for i in range(len(self))])
        for i in range(len(self)):
            if i!=len(self)-2 : r[(i+2)%len(self)]=(-1)**i*(self[i] * other[(i+1) % len(self)]
                                        -self[(i+1) % len(self)] * other[i])
            else: r[(i+2)%len(self)]=(-1)**(i+1)*(self[i] * other[(i+1)%len(self)]
                                        -self[(i+1) % len(self)] * other[i])
        return r
        #проверить ее надо))
    def perp(self,other):
        return abs((self/other)/(abs(other)))

    def __floordiv__(self, other):
        r=0
        for i in range(len(self)):
            r+=self[i]*other[i]
        return r

class Point:
    def __init__(self,coords=Vector(),speed=Vector(),mass=0,acc=None,q=1):
        self.coords=coords
        self.speed=speed
        self.mass=mass
        self.acc=acc
        self.q=q

    def move(self,dt):
        self.coords=self.coords+self.speed*dt
        #print(self.speed)

    def accelerate(self,dt):
        self.speed=self.speed+self.acc*dt
        #print(self.acc)

    def acer(self,Force):
        self.acc=Force*(1/self.mass)
        #print(self.acc)


class Body:
    def __init__(self):
        self.points=[-1]*10
        self.omega=0
        self.acc=0
        self.eps=0
        self.speed=0
        self.I=0
        self.center=0

    def append(self,p , i):
        self.points[i]=p


    def delete(self,i):
        self.points[i]=-1


    def calc_center(self):
        center=Vector(*[0 for i in range(len(self.points[0]))])
        sum_mass=0
        for p in self.points:
            if type(p)!=int:
                for i in range(len(p)):
                    center[i]+=p[i]*p.mass
                sum_mass+=p.mass
        return center*(1/sum_mass)

    def calc_i(self):
        I=0
        self.center=self.calc_center()
        for p in self.points:
            if type(p) != int:
                I += p.mass * abs(p.coords - self.center) ** 2

        return I
    def calc_F(self,Forces):
        #принимает на вход массив
        F=Vector(*[0 for i in range(len(self.points[0]))])
        for p in Forces:
            F+=p
        return p


    def move(self,dt):
        # сначала передвигаем все точки на вектор скорости центра масс
        for p in self.points:
            p.move(dt)
        #затем поворачиваем конструкцию
        for p in self.points:
            pass

G=100
K=10**7
class Field:
    def __init__(self):
        self.points=[]
    def append(self,p):
        self.points.append(p)

    def intensity(self,coord,pointis=[]):

        if len(pointis)==0: pointis=[-1]*len(self.points)
        proj = Vector(*[0 for i in range(len(coord))])
        i=0
        for point in self.points:
            if type(pointis[i])==int:
                if coord % point.coords < 10 ** (-11):
                    continue
                proj = proj - (point.coords - coord) * (K * point.q / ((point.coords % coord) ** 3))
                # print(point.coords-coord)
            i+=1
        return proj

    def Gr_intensity(self, vect, pointis=[]):
        if len(pointis) == 0: pointis = [-1] * len(self.points)
        i=0
        inten = Vector(*[0 for i in range(len(vect))])
        for p in self.points:
            if type(pointis[i]) == int:
                if vect % p.coords < 10 ** (-11):
                    continue
                inten = inten - (vect - p.coords)*(G * p.mass  / abs(vect - p.coords) ** 3)
            i+=1
        return inten

    def step(self,dt):
        for p in self.points:
            p.acer(self.intensity(p.coords)*p.q+self.Gr_intensity(p.coords)*p.mass)
            p.accelerate(dt)
            p.move(dt)



n=7
x_size=20
y_size=20
fig=plt.figure()
ax=plt.subplot(111)
ax.set_xlim(-x_size*10,x_size*10)
ax.set_ylim(-y_size*10,y_size*10)
field = Field()
print(type(57)==int)
for i in range(0, n):
    field.append(Point(Vector(randint(-x_size, x_size), randint(-y_size, y_size),0), Vector(0, 0, 0), 10, Vector(0, 0,0 ), 1))


def sigm(x):
    '''
    Отвечает за градиент поля
    :param x: 
    :return:
    '''
    return 1 / (1 + 1.0000055 ** (-x))


def anim(steps):
    print(steps)
    field1=Field()
    for i in range(0, n):
        field1.append(field.points[i])
    for i in range(0, steps):
        field.step(0.00006)


    res=[]
    STEP=1
    for x in np.arange(-20,20,STEP):
        for y in np.arange(-20,20,STEP):
            vec=field1.intensity(Vector(x,y,0))
            grad=abs(vec)
            vec=vec*STEP*(1/abs(vec))
            res.append(([x-vec[0]/2,x+vec[0]/2],[y-vec[1]/2,y+vec[1]/2],grad))
    ax.clear()
    ax.set_xlim(-x_size , x_size )
    ax.set_ylim(-y_size , y_size )
    #print(res)
    lines=[]
    for r in res:
        lines.append(ax.plot(r[0],r[1],color=(sigm(r[2]),0.1,0.8 * (1 - sigm(r[2])))))


    return lines



steps=10
animate=FuncAnimation(fig,anim,interval=50,frames=300,blit=False)
#animate.save('field3.gif')
plt.show()