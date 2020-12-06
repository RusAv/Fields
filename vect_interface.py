from tkinter import *

# CONSTANTS
window_width = 610
window_height = 610
sense = 7 #дальность обнаружения мыши для точки
max_dist = 5 #дальность обнаружения мыши для прямой
'''В функции dist_point_to_line будет использована функция расчета 
расстояния от точки до прямой с учетом того, что прямая задается уравнением
A*x + B*y + C = 0'''
C = 120

class Mouse():
    x = -610
    y = -610
    def coords(self, event):
        self.x = event.x
        self.y = event.y

def sigm(x):
    return 1 / (1 + 1.055 ** (-x*400))

def scale(x):
    return x + window_width/2 + 15

def create_vectors(vectors, screen):
    global C
    for k in range (len(vectors)):
        pointx1 = scale(vectors[k][0][0])
        pointy1 = scale(vectors[k][1][0])
        pointx2 = scale(vectors[k][0][1])
        pointy2 = scale(vectors[k][1][1])
        color = '#' + (hex(int(sigm(vectors[k][2])*255))[2:].ljust(2, '0') + '1a' +
                       hex(int((1 - sigm(vectors[k][2]))*204))[2:].ljust(2, '0'))
        screen.create_line(pointx1, pointy1, pointx2, pointy2, width = 1, fill = color)
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
        
def create_points(mouse, con_working, points, screen):
    for k in range (len(points)):
        x = mouse.x
        y = mouse.y
        pointx = scale(points[k][0])
        pointy = scale(points[k][1])
        screen.create_oval(pointx - 2, pointy - 2, pointx + 2,
                            pointy + 1, fill="orange")
        if (x - pointx)**2 + (y - pointy)**2 < sense**2 and con_working:
            screen.create_oval(pointx - sense, pointy - sense, pointx + sense,
                                pointy + sense, fill="red")

'''def create_first_bonds(points, bodies):
    bonds = []
    for i in range (len(bodies)):
        for j in range (len(bodies[i].points)-1):
            ind1 = ind2 = -1
            for k in range (len(points)):
                if points[k] == bodies[i].points[j].coords:
                    ind1 = k
                elif points[k] == bodies[i].points[j+1].coords:
                    ind2 = k
            if ind1 != -1 and ind2 != -1:
                bonds.append([ind1, ind2])
    return bonds'''

def create_first_bonds(points, Links):
    bonds = []
    for i in range (len(Links)):
        for j in range (len(Links[i])):
            if Links[i][j] == 1:
                bonds.append([i, j])
    return bonds
            
def create_lines_between_points(con_working, points, bonds, x, y, screen):
    for k in range (len(bonds)):
        if len(bonds[k]) == 2:
            pointx1 = scale(points[bonds[k][0]][0])
            pointy1 = scale(points[bonds[k][0]][1])
            pointx2 = scale(points[bonds[k][1]][0])
            pointy2 = scale(points[bonds[k][1]][1])
            screen.create_line(pointx1, pointy1, pointx2, pointy2)
        elif len(bonds[k]) == 1 and con_working:
            pointx1 = scale(points[bonds[k][0]][0])
            pointy1 = scale(points[bonds[k][0]][1])
            screen.create_line(pointx1, pointy1, x, y)

def dist_mouse_to_line(k, points, bonds, x, y):
    x1 = scale(points[bonds[k][0]][0])
    y1 = scale(points[bonds[k][0]][1])
    x2 = scale(points[bonds[k][1]][0])
    y2 = scale(points[bonds[k][1]][1])
    A, B = quotients(x1, y1, x2, y2)
    dist = abs(A*x + B*y + C) / (A**2 + B**2)**(1/2)
    return dist

def dist_point_to_point(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**(1/2)

def quotients(x1, y1, x2, y2):
    global C
    B = C *(x1 - x2) / (y1*x2 - y2*x1)
    A = - (C + B*y1) / x1
    return A, B

def highlight_lines_between_points(del_working, points, bonds, x, y, screen):
    for k in range (len(bonds)):
        if len(bonds[k]) == 2 and del_working:
            dist = dist_mouse_to_line(k, points, bonds, x, y)
            if dist < max_dist:
                pointx1 = scale(points[bonds[k][0]][0])
                pointy1 = scale(points[bonds[k][0]][1])
                pointx2 = scale(points[bonds[k][1]][0])
                pointy2 = scale(points[bonds[k][1]][1])
                if (x - pointx1)**2 + (y - pointy1)**2 < max_dist**2 + ((pointx1 - pointx2)**2 + (pointy1 - pointy2)**2)/2 or (
                    (x - pointx2)**2 + (y - pointy2)**2 < max_dist**2 + ((pointx1 - pointx2)**2 + (pointy1 - pointy2)**2)/2):
                    screen.create_line(pointx1, pointy1, pointx2, pointy2, fill = 'blue', width = 5)
