from tkinter import *

# CONSTANTS
sense = 5 #дальность обнаружения мыши
con_working = False
con_clicks = 0
window_width = 615
window_height = 615

def connect_check():
    global con_clicks, con_working
    con_clicks += 1
    if con_clicks % 2 == 1:
        connect_button.config(text="Режим соединения: выключить",
                              bg = 'red')
        con_working = True
    else:
        connect_button.config(text="Режим соединения: включить",
                              bg = 'gray94')
        con_working = False

def connect(event):
    global k, r, sense, con_working, bodies
    x = event.x
    y = event.y
    for k in range (len(r)):
        pointx = (r[k][0] + 20)*15
        pointy = (r[k][1] + 20)*15
        if (x - pointx)**2 + (y - pointy)**2 < sense**2 and con_working:
            if len(bodies) == 0 or len(bodies[-1]) == 2:
                bodies.append([k])
            elif len(bodies[-1]) == 1:
                bodies[-1].append(k)

class Mouse():
    x = 0
    y = 0
    def coords(self, event):
        self.x = event.x
        self.y = event.y

window = Tk()
electro = Canvas(window, width=window_width, height=window_height, bg="white")
electro.pack(side=LEFT)
magnet = Canvas(window, width=window_width, height=window_height, bg="white")
magnet.pack(side=RIGHT)
frame = Frame(window)
frame.pack(side=BOTTOM)
connect_button = Button(frame, width = 25, text="Режим соединения: включить",
                        command = connect_check)
connect_button.pack()
mouse = Mouse()

'''Массив точек, генерируемых в теоретическом модуле'''
r = [[-17, -20, 0], [-8, 7, 0], [-11, -12, 0], [0, -2, 0],
     [10, 2, 0], [5, -12, 0], [14, 6, 0]]
bodies = []

while True:
    
    x = mouse.x
    y = mouse.y
    
    '''Прорисовка точечных зарядов'''
    for k in range (len(r)):
        pointx = (r[k][0] + 20)*15
        pointy = (r[k][1] + 20)*15
        electro.create_oval(pointx - 1, pointy - 1, pointx + 1,
                            pointy + 1, fill="black")
        magnet.create_oval(pointx - 1, pointy - 1, pointx + 1,
                            pointy + 1, fill="black")
        if (x - pointx)**2 + (y - pointy)**2 < sense**2 and con_working:
            electro.create_oval(pointx - sense, pointy - sense, pointx + sense,
                                pointy + sense, fill="red")
            magnet.create_oval(pointx - sense, pointy - sense, pointx + sense,
                                pointy + sense, fill="red")
    for k in range (len(bodies)):
        if len(bodies[k]) == 2:
            pointx1 = (r[bodies[k][0]][0] + 20)*15
            pointy1 = (r[bodies[k][0]][1] + 20)*15
            pointx2 = (r[bodies[k][1]][0] + 20)*15
            pointy2 = (r[bodies[k][1]][1] + 20)*15
            electro.create_line(pointx1, pointy1, pointx2, pointy2)
            magnet.create_line(pointx1, pointy1, pointx2, pointy2)
        else:
            pointx1 = (r[bodies[k][0]][0] + 20)*15
            pointy1 = (r[bodies[k][0]][1] + 20)*15
            electro.create_line(pointx1, pointy1, x, y)
            magnet.create_line(pointx1, pointy1, x, y)
    
    '''Получение координат мыши'''
    try:
        window.bind('<Motion>', mouse.coords)
        window.bind('<Button-1>', connect)
    except TclError:
        break
    window.update()
    try:
        electro.delete('all')
        magnet.delete('all')
    except TclError:
        break
