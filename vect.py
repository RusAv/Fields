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
        return (self/other)*(1/abs(other))

    def __floordiv__(self, other):
        r=0
        for i in range(len(self)):
            r+=self[i]*other[i]
        return r
    def rotated(self,alpha):
        x,y=self[0],self[1]
        return Vector(x*np.cos(alpha)-y*np.sin(alpha),x*np.sin(alpha)+y*np.cos(alpha),self[2])
class Point:
    def __init__(self,coords=Vector(),speed=Vector(),mass=0,acc=None,q=1):
        self.coords=coords
        self.speed=speed
        self.mass=mass
        self.acc=acc
        self.q=q
    def kinetic_en(self):
        return self.mass*abs(self.speed)**2/2
    def move(self,dt):
        self.coords=self.coords+self.speed*dt
        #print(self.speed)

    def accelerate(self,dt):
        self.speed=self.speed+self.acc*dt
        #print(self.speed)

    def acer(self,Force):
        self.acc=Force*(1/self.mass)
        #print(self.acc)


class Body:
    def __init__(self,dim=3):
        self.points=[]
        self.mass=0
        self.omega=0
        self.acc=Vector(*[0 for i in range(dim)])
        self.eps=Vector(*[0 for i in range(dim)])
        self.speed=Vector(*[0 for i in range(dim)])
        self.I=0
        self.center=0

    def append(self,p):
        self.points.append(p)



    def calc_center(self):
        center=Vector(*[0 for i in range(len(self.points[0].coords))])
        sum_mass=0
        for p in self.points:
            for i in range(len(p.coords)):
                center[i]+=p.coords[i]*p.mass
            sum_mass+=p.mass
        return center*(1/sum_mass)

    def calc_i(self):
        I=0
        self.center=self.calc_center()
        for p in self.points:
            I += p.mass * abs(p.coords - self.center) ** 2

        return I
    def calc_F(self,Forces):
        #принимает на вход массив
        F=Vector(*[0 for i in range(len(self.points[0].coords))])
        for p in Forces:
            F=F+p
        #print(F)
        return F

    def calc_momentum(self,Forces):
        #момент вычисляется сначала векторно чтобы избежать путаницы со знаками
        momentum=Vector(*[0 for i in range(3)])
        self.center=self.calc_center()
        for i in range(len(Forces)):
            momentum=momentum-(self.points[i].coords-self.center)/ (Forces[i])
        return abs(momentum)

    def calc_params(self):
        mas = 0
        energ = 0
        self.I = self.calc_i()
        self.center = self.calc_center()
        vel = Vector(*[0 for i in range(3)])
        for p in self.points:
            mas += p.mass
            energ += p.kinetic_en()
            vel =vel+  p.speed * p.mass
        self.mass=mas
        self.speed = vel * (1 / mas)
        self.omega = (2*(energ - (abs(self.speed)**2) * mas / 2) / self.I)**2

    def delete(self,p):
        '''
        При удалении точки из тела пересчитываем параметры твердого тела
        '''
        self.points.remove(p)
        self.calc_params()
    
    def acer(self,forces):
        self.eps = self.calc_momentum(forces) / self.I
        self.acc = self.calc_F(forces) *(1 / self.mass)
    
    def accelerate(self,dt):
        self.omega += self.eps * dt
        self.speed = self.speed + self.acc*dt

    def move(self,dt):
        self.center=self.center + self.speed*dt

G=100
K=10**8
C=5
class Field:
    def __init__(self):
        self.points=[]
    def append(self,p):
        self.points.append(p)
    def intensity(self,coord,pointis=[]):

        proj = Vector(*[0 for i in range(len(coord))])
        for point in self.points:
            if point not in pointis:
                if coord % point.coords < 10 ** (-9):
                    continue
                proj = proj - (point.coords - coord) * (K * point.q / ((point.coords % coord) ** 3))
        return proj

    def Gr_intensity(self, vect, pointis=[]):
        inten = Vector(*[0 for i in range(len(vect))])
        for p in self.points:
            if p not in pointis:
                if vect % p.coords < 10 ** (-9):
                    continue
                inten = inten - (vect - p.coords)*(G * p.mass  / abs(vect - p.coords) ** 3)
        return inten

    def Magnetic_intensity(self, vect, pointis=[]):
        inten = Vector(*[0 for i in range(len(vect))])
        for p in self.points:
            if p not in pointis:
                if vect % p.coords < 10 ** (-9):
                    continue
                inten = inten+(p.speed/(p.coords-vect))*(C/abs(p.coords-vect)**3)
        return inten

    def step(self,InBody,dt):
        for i in range(len(self.points)):
            p=self.points[i]
            if InBody[i]==-1:
                p.move(dt)
                p.acer(self.intensity(p.coords)*p.q+self.Gr_intensity(p.coords)*p.mass+(p.speed/self.Magnetic_intensity(p.coords))*p.q)
                p.accelerate(dt)


class body_field:
    def __init__(self):
         self.bodies=[]
    def append(self,body):
         self.bodies.append(body)

    def initial(self,in_body,field):
        '''
        Тут происходит созание поля по массиву в котором каждой точке сопоставлен номер тела, в котором она состоит
        Также вычисляютсю параметры такого тела
        Вызов этой функции происходит каждый ра зкогда меняется поле
        '''
        l=max(in_body)+1
        self.bodies=[Body() for i in range(l)]
        for i in range(len(in_body)):
            if in_body[i]!=-1 :self.bodies[in_body[i]].points.append(field.points[i])
        for body in self.bodies:
            body.calc_params()


    def change_params(self,field,dt):
        for body in self.bodies:
            #body.I=body.calc_i()
            forces=[field.intensity(body.points[i].coords,body.points)*body.points[i].q +
                    field.Gr_intensity(body.points[i].coords,body.points)*body.points[i].mass
                    +(body.points[i].speed/field.Magnetic_intensity(body.points[i].coords))*body.points[i].q
                    for i in range(len(body.points))]
            #print(forces)
            body.acer(forces)


    def move_points(self,dt):
        for body in self.bodies:
            for p in body.points:
                s=p.coords-body.center
                #print(abs(s),"vbh")
                p.coords=p.coords+body.speed*dt+(s.rotated(5*body.omega*dt)-s)
            body.move(dt)
            #print(abs(body.points[1].coords-body.center),'______________sfvd')

    def speed_points(self,dt):
        for body in self.bodies:
            body.accelerate(dt)
            for p in body.points:
                s = p.coords - body.center
                #print(abs(s))
                p.speed=body.speed+\
                        s.perp(Vector(*[1 for i in range(len(p.coords))]))*\
                        (body.omega*abs(s)*(1/abs(s.perp(Vector(*[1 for i in range(len(p.coords))])))))
                #Тут стоит некий костыль чтобы определить направление вращательной компоненты скорости мы берем
                #перпендикулярную проекцию вектора скорости центра масс на радиус вектор точки относ центра масс и делим ее на модуль этого вектора
                #тем самым получаем единичный вектор, перпендикулярный линии между тоской и цм
        print()
    def step(self,field,dt):
        self.change_params(field,dt)
        self.move_points(dt)
        self.speed_points(dt)




n=6
x_size=80
y_size=80
fig=plt.figure()
ax=plt.subplot(111)
ax.set_xlim(-x_size*10,x_size*10)
ax.set_ylim(-y_size*10,y_size*10)
field = Field()
InBody=[0,0,0,1,1,-1]
stepik=0

print(type(57)==int)
for i in range(0, n):
    field.append(Point(Vector(randint(-x_size/2, x_size/2), randint(-y_size/2, y_size/2),0), Vector(0, 0, 0), 10, Vector(0, 0,0 ), 1))
body_fi= body_field()
body_fi.initial(InBody,field)

def sigm(x):
    '''
    Отвечает за градиент поля
    :param x:
    :return:
    '''
    return 1 / (1 + 1.000055 ** (-x))


def anim(steps):
    global stepik
    print(steps)
    stepik+=1
    for i in range(9):
        field.step(InBody,0.001)
        body_fi.step(field,0.001)
    print(abs(body_fi.bodies[0].points[1].coords - body_fi.bodies[0].center))
    print(abs(field.points[2].coords - body_fi.bodies[0].center))
    res=[]
    STEP=4
    for x in np.arange(-x_size,x_size,STEP):
        for y in np.arange(-y_size,y_size,STEP):
            #print(x,'  ',y)
            vec=field.Gr_intensity(Vector(x,y,0))
            grad=abs(vec)
            vec=vec*(STEP*(1/abs(vec)))
            res.append(([x-vec[0]/2,x+vec[0]/2],[y-vec[1]/2,y+vec[1]/2],grad))
    ax.clear()
    ax.set_xlim(-x_size , x_size )
    ax.set_ylim(-y_size , y_size )
    lines=[]
    for r in res:
        lines.append(ax.plot(r[0],r[1],color=(sigm(r[2]),0.1,0.8 * (1 - sigm(r[2])))))


    return lines



steps=10
#anim(1000)
animate=FuncAnimation(fig,anim,interval=50,frames=300,blit=False)
#animate.save('field3.gif')
plt.show()
