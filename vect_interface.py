'''
Этот модуль отвечает за реализацию интерфейса программы

Он содержит в себе один класс:
    Mouse - обрабатывает и хранит координаты при нажатии на мышь

Функции:
    sigm_el - 
    sigm_gr -
    sigm_mg - 
    scale_x - 
    scale_y - 
    scale_x_back - 
    scale_y_back - 
    create_electro_vectors - 
    create_gravit_vectors - 
    creae_points - 
    create_lines_between_points - 
    dist_mouse_to_line - 
    dist_point_to_point - 
    quotients - 
    highlight_lines_between_points - 
    create_magnet_squares - 
'''

from tkinter import *

# CONSTANTS
sense = 7 #дальность обнаружения мыши для точки
max_dist = 5 #дальность обнаружения мыши для прямой


C = 120

class Mouse():
    '''
    Этот класс хранит координаты мыши

    Функции:
        __init__ -  конструктор. Создёт атрибуты:
            self.x, self.y - координаты мыши в СК Tkinter. 
    '''
    def __init__(self, x=-610, y=-609):
        self.x = x
        self.y = y

    def coords(self, event):
        self.x = event.x
        self.y = event.y


def sigm_el(x):
    '''
    Раскраска векторов электрического поля
    
    Параметры:
        x - напряженность, для которой необхожимо рассчитать цвет
    
    Возвращает:
        float - Некототрый коэффициент, по которому красится вектор
                Подробнее читайте documentaion.pdf
    '''
    return 1 / (1 + 1.055 ** (-x/50))


def sigm_gr(x):
    '''
    Раскраска векторов гравитационного поля
    
    Параметры:
        x - напряженность, для которой необхожимо рассчитать цвет
    
    Возвращает:
        float - Некототрый коэффициент, по которому красится вектор
                Подробнее читайте documentaion.pdf
    '''
    return 1 / (1 + 1.055 ** (-x*200))


def sigm_mg(x):
    '''
    Раскраска "магнитных" квадратов
    
    Параметры:
        x - напряженность, для которой необхожимо рассчитать цвет
    
    Возвращает:
        float - Некототрый коэффициент, по которому красится вектор
                Подробнее читайте documentaion.pdf
    '''
    return 1 / (1 + 2 ** (-x*100))


def scale_x(x, window_settings):
    '''
    Масштабирование по горизонтальной оси

    Параметры:
        x - координата в глобальной системе координат с нулём в центре
        window_settings - размеры окна в формате [x_size, y_size] 

    Возвращает:
        float - координату точки в экранной системе координат    
    '''
    return ((x+22)*window_settings[0]/(2*window_settings[2]) +
            window_settings[0]/2)


def scale_y(y, window_settings):
    '''
    Масштабирование по вертикальной оси

    Параметры:
        y - координата в глобальной системе координат с нулём в центре
        window_settings - размеры окна в формате [x_size, y_size] 

    Возвращает:
        float - координату точки в экранной системе координат    
    '''
    return ((y+22)*window_settings[1]/(2*window_settings[3]) +
            window_settings[1]/2)


def scale_x_back(x, window_settings):
    '''
    Вычисление глобальной горизонтальной координаты по экранной

    Параметры:
        x - координата в экранной системе координат с нулём в центре
        window_settings - размеры окна в формате [x_size, y_size] 

    Возвращает:
        float - координату точки в глобальной системе координат    
    '''
    return ((2*x - window_settings[0])*window_settings[2]/window_settings[0] - 22)


def scale_y_back(y, window_settings):
    '''
    Вычисление глобальной вертикальной координаты по экранной

    Параметры:
        x - координата в экранной системе координат с нулём в центре
        window_settings - размеры окна в формате [x_size, y_size] 

    Возвращает:
        float - координату точки в глобальной системе координат    
    '''
    return ((2*y - window_settings[1])*window_settings[3]/window_settings[1] - 22)


def create_electro_vectors(vectors, window_settings, screen):
    '''
    Здесь рисуются вектора электрического поля, которые передаются из массива vectors
    
    Параметры:
        vectors -  массив векторов, которые нужно изобразить. Список (x, y, z) - неотнормированные вектора,
                                    Перечисление происходит построчно справо налево и сверху вниз.
        window_settings - Размеры окна в формате [x_size, y_size] 
        screen - экран - объект Tkinter
        '''
    global C
    for k in range (len(vectors)):
        pointx1 = scale_x(vectors[k][0][0], window_settings)
        pointy1 = scale_y(vectors[k][1][0], window_settings)
        pointx2 = scale_x(vectors[k][0][1], window_settings)
        pointy2 = scale_y(vectors[k][1][1], window_settings)
        color = '#' + (hex(int(sigm_el(vectors[k][2])*255))[2:].ljust(2, '0') + '1a' +
                       hex(int((1 - sigm_el(vectors[k][2]))*204))[2:].ljust(2, '0'))
        screen.create_line(pointx1, pointy1, pointx2, pointy2, width = 2, fill = color)
        '''стрелочка на конце'''
        length = dist_point_to_point(pointx1, pointy1, pointx2, pointy2)
        if length > 0:
            A, B = quotients(pointx1, pointy1, pointx2, pointy2)
            C_new = B*(pointx1 + 3*pointx2)/4 - A*(pointy1 + 3*pointy2)/4
            x_a = A*length/(8*(A**2+B**2)**(1/2)) + (B*C_new - A*C)/(A**2+B**2)
            y_a = (B*x_a - C_new)/A
            x_b = -A*length/(8*(A**2+B**2)**(1/2)) + (B*C_new - A*C)/(A**2+B**2)
            y_b = (B*x_b - C_new)/A
            screen.create_polygon([pointx2, pointy2, x_a, y_a, x_b, y_b], width = 1, fill = color)


def create_gravit_vectors(vectors, window_settings, screen):
    '''
    Здесь рисуются вектора гравитационного поля, которые передаются из
        массива vectors
    
    Параметры:
        vectors -  массив векторов, которые нужно изобразить. Список (x, y, z) - неотнормированные вектора,
                                    Перечисление происходит построчно справо налево и сверху вниз.
        window_settings - Размеры окна в формате [x_size, y_size] 
        screen - экран - объект Tkinter
    '''
    global C
    for k in range (len(vectors)):
        pointx1 = scale_x(vectors[k][0][0], window_settings)
        pointy1 = scale_y(vectors[k][1][0], window_settings)
        pointx2 = scale_x(vectors[k][0][1], window_settings)
        pointy2 = scale_y(vectors[k][1][1], window_settings)
        color = '#' + (hex(int(sigm_gr(vectors[k][2])*255))[2:].ljust(2, '0') + '1a' +
                       hex(int((1 - sigm_gr(vectors[k][2]))*204))[2:].ljust(2, '0'))
        screen.create_line(pointx1, pointy1, pointx2, pointy2, width = 2, fill = color)
        '''стрелочка на конце'''
        length = dist_point_to_point(pointx1, pointy1, pointx2, pointy2)
        if length > 0:
            A, B = quotients(pointx1, pointy1, pointx2, pointy2)
            C_new = B*(pointx1 + 3*pointx2)/4 - A*(pointy1 + 3*pointy2)/4
            x_a = A*length/(8*(A**2+B**2)**(1/2)) + (B*C_new - A*C)/(A**2+B**2)
            y_a = (B*x_a - C_new)/A
            x_b = -A*length/(8*(A**2+B**2)**(1/2)) + (B*C_new - A*C)/(A**2+B**2)
            y_b = (B*x_b - C_new)/A
            screen.create_polygon([pointx2, pointy2, x_a, y_a, x_b, y_b], width = 1, fill = color)
        

def create_points(mouse, con_working, rem_working, points, window_settings,
                  screen):
    '''
    Здесь рисуются точки, передающиеся в массиве points, также
       рисуются точки покрупнее при наведении на них мыши
    
    Параметры:
        mouse - объкт класса Mouse, который хранит координаты клика
        con_working - Bool переменная. True - если включено соединение, иначе - False
        rem_working - Bool переменная. True - если включено удаление точек, иначе - False
        points - массив точек, которые необходимо отобразить. Массив (x, y) в экранных координатах
        window_settings - Параметры окна в формате [x_size, y_size]
        screen - экран. Объект Tkinter
    '''
    for k in range (len(points)):
        x = mouse.x
        y = mouse.y
        pointx = scale_x(points[k][0], window_settings)
        pointy = scale_y(points[k][1], window_settings)
        screen.create_oval(pointx - 4, pointy - 4, pointx + 4,
                            pointy + 4, fill="cyan")
        
        # Если мышь рядом с точкой и включён один из режимов:
        #                                       удаление точек
        #                                       соединение точек
        # То точка краситс в жёлтый цвет и становится больше
        if (x - pointx)**2 + (y - pointy)**2 < sense**2 and (con_working or rem_working):
            screen.create_oval(pointx - sense, pointy - sense, pointx + sense,
                                pointy + sense, fill="yellow")
            

def create_lines_between_points(con_working, points, bonds, x, y,
                                window_settings, screen):
    '''
    Здесь рисуются межточечные связи (ребра), лежащие в массиве bonds
    
    Параметры:
        con_working - Bool переменная. True - если включён режим соединения точек, иначе - False
        points - массив координат точек (х, у) в экранной СК
        bonds - массив рёбер в формате [(point_1, point_2), ...]
        window_settings - параметры окна в формате [x_size, y_size]
        screen - экран. Объект Tkinter.
    '''
    for k in range (len(bonds)):
        if len(bonds[k]) == 2:
            pointx1 = scale_x(points[bonds[k][0]][0], window_settings)
            pointy1 = scale_y(points[bonds[k][0]][1], window_settings)
            pointx2 = scale_x(points[bonds[k][1]][0], window_settings)
            pointy2 = scale_y(points[bonds[k][1]][1], window_settings)
            screen.create_line(pointx1, pointy1, pointx2, pointy2, fill = 'cyan', width = 2)
        elif len(bonds[k]) == 1 and con_working:
            pointx1 = scale_x(points[bonds[k][0]][0], window_settings)
            pointy1 = scale_y(points[bonds[k][0]][1], window_settings)
            screen.create_line(pointx1, pointy1, x, y, fill = 'cyan', width = 2)


def dist_mouse_to_line(k, points, bonds, x, y, window_settings):
    '''
    Вычисление расстояния от курсора до ребра

    В функции использована функция расчета 
    расстояния от точки до прямой с учетом того, что прямая задается уравнением
    A*x + B*y + C = 0
    
    Параметры: 
        k - номер ребра, расстояние до которого от мыши ищем
        points - список координат точек (х, у) в экранной СК
        bonds - список рёбер в формате [point_1, point_2, ...]
        x, y - координаты курсора в экранной СК
        window_settings - параметры окна в формате [x_size, y_size]
    '''
    x1 = scale_x(points[bonds[k][0]][0], window_settings)
    y1 = scale_y(points[bonds[k][0]][1], window_settings)
    x2 = scale_x(points[bonds[k][1]][0], window_settings)
    y2 = scale_y(points[bonds[k][1]][1], window_settings)
    A, B = quotients(x1, y1, x2, y2)
    dist = abs(A*x + B*y + C) / (A**2 + B**2)**(1/2)
    return dist


def dist_point_to_point(x1, y1, x2, y2):
    '''
    Вычисление расстояния между двумя точками
    
    Параметры:
        x1, y1 - координаты первой точки
        x2, y2 - координаты второй точки

    Врзвращает:
        float - расстоние между точками
    '''
    return ((x2 - x1)**2 + (y2 - y1)**2)**(1/2)


def quotients(x1, y1, x2, y2):
    '''
    Вычисление коэффициентов прямой, заданной уравнением A*x + B*y + C = 0
       по двум точкам
    С - глобальная константа

    Параметры:
        x1, y1 - координаты первой точки
        x2, y2 - координаты второй точки

    Возвращает:
        float, float - A, B - коэффициенты прямой в вышеописанном виде. 
    '''
    global C
    B = C *(x1 - x2) / (y1*x2 - y2*x1)
    A = - (C + B*y1) / x1
    return A, B


def highlight_lines_between_points(del_working, points, bonds, x, y,
                                   window_settings, screen):
    '''
    Подсвечивание ребер между точками в режиме удаления при наведении на них
       курсора

    Параметры: 
        del_working - Bool переменная. True - если включен режим разъединения, иначе - False 
        points - массив координат точек (х, у) в экранной СК
        bonds - список ребер в формат [(point_1, point_2), ...]
        x, y - координаты курсора мыши в экранной СК
        window_settings - параметры окна в формате [x_size, y_size]
        screen - экран. Объект Tkinter
    '''
    for k in range (len(bonds)):
        if len(bonds[k]) == 2 and del_working:
            dist = dist_mouse_to_line(k, points, bonds, x, y, window_settings)
            if dist < max_dist:
                pointx1 = scale_x(points[bonds[k][0]][0], window_settings)
                pointy1 = scale_y(points[bonds[k][0]][1], window_settings)
                pointx2 = scale_x(points[bonds[k][1]][0], window_settings)
                pointy2 = scale_y(points[bonds[k][1]][1], window_settings)
                if (x - pointx1)**2 + (y - pointy1)**2 < max_dist**2 + ((pointx1 - pointx2)**2 + (pointy1 - pointy2)**2)/2 or (
                    (x - pointx2)**2 + (y - pointy2)**2 < max_dist**2 + ((pointx1 - pointx2)**2 + (pointy1 - pointy2)**2)/2):
                    screen.create_line(pointx1, pointy1, pointx2, pointy2, fill = 'blue', width = 5)


def create_magnet_squares(vectors, step, window_settings,
                          screen):
    '''
    Здесь рисуются квадраты, иллюстрирующие вектора магнитного поля
    
    Параметры:
        vectors - массив векторов магнитной напряженности в виде списка (x, y, z) - неотнормированные вектора.
                                                Перчисление идёт построчно слева направо сверху вниз.
        step - размер квадрата, а именно длина его стороны
        window_settings - параметры окна в формате [x_size, y_size]
        screen - экран. Объект Tkinter.

    '''
    for k in range (len(vectors)):
        x_center = scale_x((vectors[k][0][0]+vectors[k][0][1])/2, window_settings)
        y_center = scale_y((vectors[k][1][0]+vectors[k][1][1])/2, window_settings)
        color = '#' + (hex(int(sigm_mg(vectors[k][2])*255))[2:].ljust(2, '0') + '1a' +
                       hex(int((1 - sigm_mg(vectors[k][2]))*204))[2:].ljust(2, '0'))
        screen.create_polygon([x_center - step/2-1, y_center - step/2-1,
                                x_center + step/2+1, y_center - step/2-1,
                                x_center + step/2+1, y_center + step/2+1,
                                x_center - step/2-1, y_center + step/2+1],
                                fill = color)


if __name__ == '__main__':
    print("This module is not for direct call")
