from tkinter import *

# CONSTANTS
sense = 5 #дальность обнаружения мыши
con_working = False
con_clicks = 0

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

'''Надо задать функцию соединения точек, на которые наводится мышь'''

class Mouse():
    x = 0
    y = 0
    def coords(self, event):
        self.x = event.x
        self.y = event.y

window = Tk()
window_width = 615
window_height = 615
electro = Canvas(window, width=window_width, height=window_height, bg="white")
electro.pack(side=LEFT)
magnet = Canvas(window, width=window_width, height=window_height, bg="white")
magnet.pack(side=RIGHT)
frame = Frame(window)
frame.pack(side=BOTTOM)
connect_button = Button(frame, width = 25, text="Режим соединения: включить",
                        command = connect_check)
connect_button.pack()

'''Массив точек, генерируемых в теоретическом модуле'''
r = [[-17, -20, 0], [-8, 7, 0], [-11, -12, 0], [0, -2, 0],
     [10, 2, 0], [5, -12, 0], [14, 6, 0]]

mouse = Mouse()

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
    
    '''Получение координат мыши'''
    try:
        window.bind('<Motion>', mouse.coords)
    except TclError:
        break
    
    window.update()
    try:
        electro.delete('all')
        magnet.delete('all')
    except TclError:
        break
