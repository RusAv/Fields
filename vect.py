import matplotlib.pyplot as plt
from random import *
import numpy as np
from matplotlib.animation import *


# TODO: Сделать нормальную размерность у всех векторов. Так оно, конечно, тоже работает, но лучше бы реализовать как-то иначе.

class Vector(list):
    def __init__(self, *el):
        '''
        Создание нового вектора.
        *el - набор координат
        '''
        for l in el:
            self.append(l)

    def __add__(self, other_vector):
        '''
        Сложение векторов
        '''

        r = Vector()
        for i in range(len(self)):
            r.append(self[i] + other_vector[i])
        return r

    def __sub__(self, other_vector):
        '''
        Вычитание векторов
        '''

        r = Vector()
        for i in range(len(self)):
            r.append(self[i] - other_vector[i])
        return r

    def __mod__(self, other_vector):
        '''
        Вычисляет длину вектора-разности self и other_vector
        '''

        r = 0
        for i in range(len(self)):
            r += (self[i] - other_vector[i]) ** 2
        return r ** 0.5

    def __mul__(self, scalar):
        '''
        Умножение вектора на скаляр
        '''

        r = Vector()
        for i in range(len(self)):
            r.append(self[i] * scalar)
        return r

    def __abs__(self):
        '''
        Модуль вектора
        '''

        r = 0
        for i in range(len(self)):
            r += self[i] ** 2
        return r ** 0.5

    def __truediv__(self, other_vector):
        '''
        Задаем операцию векторного умножения x на y
        Задаётся выражением "x/y"
        '''

        r = Vector(*[0 for i in range(len(self))])
        for i in range(len(self)):
            if i != len(self) - 2:
                r[(i + 2) % len(self)] = (-1) ** i * (self[i] * other_vector[(i + 1) % len(self)]
                                                      - self[(i + 1) % len(self)] * other_vector[i])
            else:
                r[(i + 2) % len(self)] = (-1) ** (i + 1) * (self[i] * other_vector[(i + 1) % len(self)]
                                                            - self[(i + 1) % len(self)] * other_vector[i])
        return r
        #                                                                  _ _
        # Прошла проверку на 9590 тестах, но выглядит страшно             |o o|
        #                                                              \  | 7 |  /
        # Понять её я даже не пытался))                                 \ | 0 | /
        #                                                                \~~~~~/

    def perp(self, other):
        '''
        ???
        '''

        # NOTE (to @RusAv) Вообще непонятно, зачем это нужно

        return (self / other) * (1 / (abs(other)*abs(self)))

    def __floordiv__(self, other_vector):
        '''
        Скалярное проиведение векторов
        Задаётся 'x//y'
        '''

        r = 0
        for i in range(len(self)):
            r += self[i] * other_vector[i]
        return r

    def rotated(self, alpha):
        '''
        Поворот вектора на угол alpha в пл-ти Oxy
        '''

        x, y = self[0], self[1]
        return Vector(x * np.cos(alpha) - y * np.sin(alpha), x * np.sin(alpha) + y * np.cos(alpha), self[2])


class Point:
    def __init__(self, coords=Vector(), speed=Vector(), mass=0, acc=None, q=1):
        '''
        Создание точки
        '''
        self.coords = coords
        self.speed = speed
        self.mass = mass
        self.acc = acc
        self.q = q

    def kinetic_en(self):
        '''
        Функция вычисляет кинетическую энергию точки
        '''
        return self.mass * abs(self.speed) ** 2 / 2

    def move(self, dt):
        '''
        Функция изменяет координаты точки в зависимости от имеющейся скорости
        '''
        self.coords = self.coords + self.speed * dt
        # print(self.speed)  # TODO: Удалить в самом конце

    def accelerate(self, dt):
        '''
        Вычисляет скорости точки в зависимости от имеющего ускорения
        '''
        self.speed = self.speed + self.acc * dt
        # print(self.speed)  # TODO: Удалить в самом конце

    def acer(self, Force):
        '''
        Вычисляет ускорение точки в зависимости от приложенной к ней силы
        '''
        self.acc = Force * (1 / self.mass)
        # print(self.acc)  # TODO: Удалить в самом конце


class Body:
    def __init__(self, dim=3):
        '''
        Создание объекта класса тело
        '''
        self.points = []  # Инициализируется список точек в теле. Изначально он пустой
        self.mass = 0  # Масса тела равна нулю, т.к. в нём ещё нет точек
        self.omega = 0  # Угловая скорость
        self.acc = Vector(*[0 for i in range(dim)])  # Ускорение центра масс тела
        self.eps = Vector(*[0 for i in range(dim)])  # Угловое ускорение относительно центра масс
        self.speed = Vector(*[0 for i in range(dim)])  # Скорость центра масс
        self.I = 0  # Момент инерции тела
        self.center = Vector()  #

    def append(self, point):
        '''
        Добавление точки в тело
        '''
        self.points.append(point)

    def calc_center(self):
        '''
        Вычисление координат центра масс
        '''
        center = Vector(*[0 for i in range(len(self.points[0].coords))])
        sum_mass = 0
        for p in self.points:
            for i in range(len(p.coords)):
                center[i] += p.coords[i] * p.mass
            sum_mass += p.mass
        return center * (1 / sum_mass)

    def calc_i(self):
        '''
        Вычисление момента инерции тела
        '''
        I = 0
        self.center = self.calc_center()
        for p in self.points:
            I += p.mass * abs(p.coords - self.center) ** 2
        return I

    def calc_F(self, Forces: list):
        '''
        Вычисляет геометрическую сумму сил, действующих на все точки данного тела
        Forces - массив сил
        '''

        F = Vector(*[0 for i in range(len(self.points[0].coords))])
        for p in Forces:
            F = F + p
        # print(F)  # TODO: Удалить в самом конце
        return F

    def calc_momentum(self, Forces: list):
        '''
        Вычисляет момент сил относительно центра масс тела.
        Возвращает скаляр, т.к. момент всегда перпендикулярен плокости Oxy при плоском движении
        '''
        # Момент вычисляется сначала векторно чтобы избежать путаницы со знаками
        momentum = Vector(*[0 for i in range(3)])
        self.center = self.calc_center()
        #print(Forces,'dcd')
        for i in range(len(Forces)):
            momentum = momentum - (self.points[i].coords - self.center) / (
            Forces[i])  # TODO: Почему стоит знак "минус"?
        #print(momentum,'sdfsdf')
        return abs(momentum)

    def calc_params(self):
        '''
        Рассчитывает параметры тела, такие как:
        масса, энергия, момент инерции, положение центра масс, линейная скорость, угловая скорость
        '''
        mas = 0
        energ = 0
        self.center = self.calc_center()
        vel = Vector(*[0 for i in range(3)])
        for p in self.points:
            mas += p.mass
            energ += p.kinetic_en()
            vel = vel + p.speed * p.mass
        self.mass = mas
        self.I = self.calc_i()
        self.speed = vel * (1 / mas)
        self.omega = (2 * (energ - (abs(self.speed) ** 2) * mas / 2) / self.I) ** 0.5
        #print(self.I,self.center,self.omega,self.speed)

    def delete(self, point):
        '''
        При удалении точки из тела пересчитываем параметры твердого тела
        '''
        self.points.remove(point)
        self.calc_params()

    def acer(self, forces):
        '''
        Выичсление углового и линейного ускорени тела исходя из действующих на него сил
        '''
        self.eps = self.calc_momentum(forces) / self.I
        self.acc = self.calc_F(forces) * (1 / self.mass)

    def accelerate(self, dt):
        '''
        Вычисление угловой и линейной скорости тела, исходя из имеющихся ускорений
        '''
        self.omega += self.eps * dt
        self.speed = self.speed + self.acc * dt

    def move(self, dt):
        '''
        Изменение координат центра масс тела, исходя из имеющейся линейной скорости
        '''
        self.center = self.center + self.speed * dt


class Field:
    G = 100  # Гравитационная постоянная
    k = 10 ** 7  # Электрическая постоянная
    mu_0 = 0.6  # Магнитная постоянная

    def __init__(self):
        '''
        Конструктор объекта для управлния полями.
        Также он хранит множество всех материальных точек в симуляции, изначльно это множество пустое
        '''
        self.points = []

    def append(self, p):
        '''
        Добавление материальной точки в список точек, участвующих в симуляции
        '''
        self.points.append(p)

    def El_intensity(self, coord, pointis=[]):
        '''
        Вычисляет напряженность электрического поля в данной точке с координатами coords.
        При этом игнорируются точки из массива points
        '''
        proj = Vector(*[0 for i in range(len(coord))])
        for point in self.points:
            if point not in pointis:
                if coord % point.coords < 10 ** (-9):
                    continue
                proj = proj - (point.coords - coord) * (Field.k * point.q / ((point.coords % coord) ** 3))
        proj[2]=0
        return proj

    def Gr_intensity(self, vect, pointis=[]):
        '''
        Вычисляет напряженность магнитного поля в данной точке с координатами vect.
        При этом игнорируются точки из массива points
        '''
        inten = Vector(*[0 for i in range(len(vect))])
        for p in self.points:
            if p not in pointis:
                if vect % p.coords < 10 ** (-9):
                    continue
                inten = inten - (vect - p.coords) * (Field.G * p.mass / abs(vect - p.coords) ** 3)
        inten[2]=0
        return inten

    def Mg_intensity(self, vect, pointis=[]):
        '''
        Вычисляет напряженность гравитационного поля в данной точке с координатами vect.
        При этом игнорируются точки из массива points
        '''
        inten = Vector(*[0 for i in range(len(vect))])
        for p in self.points:
            if p not in pointis:
                if vect % p.coords < 10 ** (-9):
                    continue
                inten = inten + (p.speed / (p.coords - vect)) * (Field.mu_0 / abs(p.coords - vect) ** 3)
        inten[1] = 0
        inten[0] = 0
        return inten

    def step(self, InBody, dt):
        '''
        Изменяет значения координат и скорости для каждой точке в теле
        '''
        for i in range(len(self.points)):
            p = self.points[i]
            if InBody[i] == -1:
                p.move(dt)
                p.acer(self.El_intensity(p.coords) * p.q +
                       self.Gr_intensity(p.coords) * p.mass +
                       (p.speed / self.Mg_intensity(p.coords)) * p.q)
                p.accelerate(dt)


class body_field:
    def __init__(self):
        '''
        Создание объекта класса body_field, который отвечает за перемещение тел в поле внешних сил.
        Подразумевается наличие единственного объекта данного класса
        '''  # TODO: Уточнить, действительно ли обеъкт этого лкасса один
        self.bodies = []

    def append(self, body):
        '''
        Добавление тела в список всех существующих тел
        '''
        self.bodies.append(body)

    def initial(self, in_body, field):
        '''
        Тут происходит создание поля по массиву в котором каждой точке сопоставлен номер тела, в котором она состоит.
        Также вычисляютсю параметры такого тела.
        Вызов этой функции происходит каждый раз когда меняется поле.
        '''
        l = max(in_body) + 1
        self.bodies = [Body() for i in range(l)]
        for i in range(len(in_body)):
            if in_body[i] != -1: self.bodies[in_body[i]].points.append(field.points[i])
        for body in self.bodies:
            body.calc_params()

    def change_params(self, field, dt):
        '''
        Вычисляет, какие силы действуют на каждое тело посредством суммирования сил, действиующих на каждую точку тела
        '''
        for body in self.bodies:
            forces = [field.El_intensity(body.points[i].coords, body.points) * body.points[i].q +
                      field.Gr_intensity(body.points[i].coords, body.points) * body.points[i].mass
                      + (body.points[i].speed / field.Mg_intensity(body.points[i].coords)) * body.points[i].q
                      for i in range(len(body.points))]
            body.acer(forces)

    def move_points(self, dt):
        '''
        Изменяет положение всех точек в теле согласно движению тела как целого
        '''
        for body in self.bodies:
            for p in body.points:
                s = p.coords - body.center
                # print(abs(s),"vbh")  # TODO: Удалить в самом конце
                p.coords = p.coords + body.speed * dt + (s.rotated(5 * body.omega * dt) - s)
            body.move(dt)

    def speed_points(self, dt):
        '''
        Изменяет скорости всех точек тела согласно движению тела как целого        
        '''
        for body in self.bodies:
            body.accelerate(dt)
            for p in body.points:
                s = p.coords - body.center
                if abs(s) <1: print(abs(s),'   ',body.center)  # TODO: Удалить в самом конце
                p.speed = body.speed + \
                          s.perp(Vector(0,0,1)) * \
                          (body.omega * abs(s) * (1 / abs(s.perp(Vector(0,0,1)))))
                
    def step(self, field, dt):
        '''
        Вызывают методы изменения параметров поля (его напряженности), изменения положения точек всех тел и их скоростей
        '''
        self.change_params(field, dt)
        self.move_points(dt)
        self.speed_points(dt)


# TODO: Что это такое??? Всё, что не нужно, удалите, пожалуйста. Какие-то массивы. Просто страшно смотреть...   

n = 7
field = Field()
InBody = [0, 0, 0, -1,0,0,0]
body_fi = body_field()
Links=[ [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,0,1,1,1],
        [1,1,0,0,0,0,0],
        [0,0,1,0,0,0,0],
        [0,0,1,0,0,0,1],
        [0,0,1,0,0,1,0] ]
stepik = 0
dt = 0.001

def make_points(x_size, y_size):
    '''
    Случайным образом создаёт точки в окне. Вызывается при первоначальном открытии окна.
    '''
    global body_fi
    for i in range(0, n):
        field.append(
            Point(Vector(randint(-x_size / 5, x_size / 5), randint(-y_size / 5, y_size / 5), 0), Vector(0, 0, 0), 10,
                  Vector(0, 0, 0), 1))
    body_fi.initial(InBody, field)


def sigm(x):
    '''
    Отвечает за градиент поля
    :param x:
    :return:
    '''
    return 1 / (1 + 1.000055 ** (-x))

def return_points():
    '''
    Функця возвращает набор корординат всех точек
    '''
    point_s=[]
    for p in field.points:
        point_s.append(p.coords)
        #print(p.coords)
    return point_s
        
def return_field(x_size, y_size, flag, STEP):
    '''
    Функция возвращает набор: (длина вектора по х, длина вектора по у, градиент его цвета) 
    для всех точек плоскости с шагом в STEP.
    При этом возращаются вектора еденичной длины, а от длины исходного вектора напряженности поля зависит градиент цвета   
    flag = 0: возвращает электрическое поле
    flag = 1: возвращает гравитационное поле
    flag = 2: возвращает магнитное поле
    '''

    res = []
    for x in np.arange(-x_size, x_size, STEP):
        for y in np.arange(-y_size, y_size, STEP):
            # print(x,'  ',y)
            if (flag==0) :
                vec = field.El_intensity(Vector(x, y, 0))
            elif (flag==1):
                vec = field.Gr_intensity(Vector(x, y, 0))
            elif (flag==2):
                vec = field.Mg_intensity(Vector(x, y, 0))
            grad = abs(vec)
            vec = vec * (STEP * (1 / abs(vec)))
            res.append(([x - vec[0]/2, x + vec[0]/2], [y - vec[1]/2, y + vec[1]/2], grad))
    return res

def return_bodies():
    '''
    Возращает набор множеств точек всех тел, 
    т.е. список списков, где каждый вложенный список - точки данного тела
    '''
    bodie = []
    for b in body_fi.bodies:
        bodie.append(b.points)
    return bodie

def Grand_field(x_size, y_size, dt):
    '''
    Эта функция возвращает:
    1) Field - набор векторов напряженности
    2) points - набор координат всех точек
    3) STEP - шаг, по которому было рассчитано Field
    4) bodie - набор всех тел, где каждое тело - набор точек, из которых оно состоит
    '''
    global  body_fi
    #шаг поля
    for i in range(9):
        field.step(InBody, dt)  # NOTE: Что это такое? Почему 9 раз нужно это сделать?
        body_fi.step(field, dt)
    STEP = 40
    Field = []
    for flag in range (3):
        Field.append(return_field(x_size, y_size, flag, STEP))
    points = return_points()
    bodie = return_bodies()
    return Field, points, STEP, bodie


def DFS(vertice, it):
    count = 0
    InBody[vertice] = it
    for i in range(len(Links[vertice])):
        if i != vertice and Links[i][vertice] == 1 and InBody[i] == -2:
            count += DFS(i, it)
    count += 1
    return count

def Re_calc_Links():
    global Links, InBody, body_fi
    marker = 0
    InBody = [-2 for i in range(len(InBody))]
    for i in range(len(InBody)):
        if InBody[i] == -2:
                c = DFS(i, marker)
                if c == 1:
                    InBody[i] = -1
                else: 
                    marker += 1



def Re_calc_all():
    Re_calc_Links()
    #print(InBody)
    body_fi.initial(InBody, field)

def add_point(x, y, x_size, y_size):
    global n, Links, InBody, field
    #print(x,y)
    InBody.append(-1)
    field.append(
        Point(Vector(x - x_size - 20, y - y_size - 20, 0), Vector(0, 0, 0), 10,
              Vector(0, 0, 0), 1))
    n += 1
    for i in range(len(Links)):
        Links[i].append(0)
    Links.append([0 for i in range(len(Links) + 1)])

if __name__ == '__main__':
    print("This module is not for direct call")
