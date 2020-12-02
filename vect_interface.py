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
    x = 0
    y = 0
    def coords(self, event):
        self.x = event.x
        self.y = event.y

def color_vector(max_length, k, vectors):
    x1 = vectors[k][0][0]
    y1 = vectors[k][1][0]
    x2 = vectors[k][0][1]
    y2 = vectors[k][1][1]
    red = int((((x1 - x2)**2 + (y1 - y2)**2)**(1/2)/max_length)*255)
    blue = int((1 - ((x1 - x2)**2 + (y1 - y2)**2)**(1/2)/max_length)*255)
    color = '#' + hex(red)[2:].ljust(2, '0') + '00' + hex(blue)[2:].ljust(2, '0')
    return color

def create_electro_vectors(step, vectors, electro):
    for k in range (len(vectors)):
        pointx1 = vectors[k][0][0] + window_width/2 + 15
        pointy1 = vectors[k][1][0] + window_height/2 + 15
        pointx2 = vectors[k][0][1] + window_width/2 + 15
        pointy2 = vectors[k][1][1] + window_height/2 + 15
        color = color_vector(step, k, vectors)
        electro.create_line(pointx1, pointy1, pointx2, pointy2, width = 5, fill = color)

def create_points(mouse, con_working, points, electro, magnet):
    for k in range (len(points)):
        x = mouse.x
        y = mouse.y
        pointx = points[k][0] + window_width/2 + 15
        pointy = points[k][1] + window_height/2 + 15
        electro.create_oval(pointx - 1, pointy - 1, pointx + 1,
                            pointy + 1, fill="black")
        magnet.create_oval(pointx - 1, pointy - 1, pointx + 1,
                            pointy + 1, fill="black")
        if (x - pointx)**2 + (y - pointy)**2 < sense**2 and con_working:
            electro.create_oval(pointx - sense, pointy - sense, pointx + sense,
                                pointy + sense, fill="red")
            magnet.create_oval(pointx - sense, pointy - sense, pointx + sense,
                                pointy + sense, fill="red")
            
def create_lines_between_points(con_working, points, bonds, x, y, electro, magnet):
    for k in range (len(bonds)):
        if len(bonds[k]) == 2:
            pointx1 = points[bonds[k][0]][0] + window_width/2 + 15
            pointy1 = points[bonds[k][0]][1] + window_height/2 + 15
            pointx2 = points[bonds[k][1]][0] + window_width/2 + 15
            pointy2 = points[bonds[k][1]][1] + window_height/2 + 15
            electro.create_line(pointx1, pointy1, pointx2, pointy2)
            magnet.create_line(pointx1, pointy1, pointx2, pointy2)
        elif len(bonds[k]) == 1 and con_working:
            pointx1 = points[bonds[k][0]][0] + window_width/2 + 15
            pointy1 = points[bonds[k][0]][1] + window_height/2 + 15
            electro.create_line(pointx1, pointy1, x, y)
            magnet.create_line(pointx1, pointy1, x, y)

def dist_mouse_to_line(k, points, bonds, x, y):
    global C
    x1 = points[bonds[k][0]][0] + window_width/2 + 15
    y1 = points[bonds[k][0]][1] + window_height/2 + 15
    x2 = points[bonds[k][1]][0] + window_width/2 + 15
    y2 = points[bonds[k][1]][1] + window_height/2 + 15
    B = C *(x1 - x2) / (y1*x2 - y2*x1)
    A = - (C + B*y1) / x1
    dist = abs(A*x + B*y + C) / (A**2 + B**2)**(1/2)
    return dist

def highlight_lines_between_points(del_working, points, bonds, x, y, electro, magnet):
    for k in range (len(bonds)):
        if len(bonds[k]) == 2 and del_working:
            dist = dist_mouse_to_line(k, points, bonds, x, y)
            if dist < max_dist:
                pointx1 = points[bonds[k][0]][0] + window_width/2 + 15
                pointy1 = points[bonds[k][0]][1] + window_height/2 + 15
                pointx2 = points[bonds[k][1]][0] + window_width/2 + 15
                pointy2 = points[bonds[k][1]][1] + window_height/2 + 15
                if (x - pointx1)**2 + (y - pointy1)**2 < max_dist**2 + ((pointx1 - pointx2)**2 + (pointy1 - pointy2)**2)/2 or (
                    (x - pointx2)**2 + (y - pointy2)**2 < max_dist**2 + ((pointx1 - pointx2)**2 + (pointy1 - pointy2)**2)/2):
                    electro.create_line(pointx1, pointy1, pointx2, pointy2, fill = 'blue', width = 5)
                    magnet.create_line(pointx1, pointy1, pointx2, pointy2, fill = 'blue', width = 5)
            
