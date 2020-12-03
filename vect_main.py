from vect import *
from vect_interface import *

# CONSTANTS
con_working = False
del_working = False
con_clicks = 0
del_clicks = 0
pau_clicks = 0
window_width = 610
window_height = 610
dt = 0.001
paused = False


def connect_check():
    global con_clicks, del_clicks, con_working, del_working, bonds
    con_clicks += 1
    if not del_working:
        if con_clicks % 2 == 1:
            connect_button.config(text="Режим соединения: выключить",
                              bg = 'red')
            con_working = True
        else:
            connect_button.config(text="Режим соединения: включить",
                              bg = 'gray94')
            con_working = False
    elif del_working and con_clicks % 2 == 1:
        connect_button.config(text="Режим соединения: выключить",
                              bg = 'red')
        del_working = False
        del_clicks = 0
        delete_button.config(text="Режим удаления: выключить",
                              bg = 'gray94')
        con_working = True

def delete_check():
    global con_clicks, del_clicks, con_working, del_working, bonds
    del_clicks += 1
    if not con_working:
        if del_clicks % 2 == 1:
            delete_button.config(text="Режим удаления: выключить",
                              bg = 'blue')
            del_working = True
        else:
            delete_button.config(text="Режим удаления: включить",
                              bg = 'gray94')
            del_working = False
    elif con_working and del_clicks % 2 == 1:
        connect_button.config(text="Режим соединения: включить",
                              bg = 'gray94')
        con_working = False
        con_clicks = 0
        delete_button.config(text="Режим удаления: выключить",
                              bg = 'blue')
        del_working = True

def paused_check():
    global pau_clicks, paused
    pau_clicks += 1
    if pau_clicks % 2 == 1:
        paused = True
        pause_button.config(text="Возобновить",
                              bg = 'green')
    else:
        paused = False
        pause_button.config(text="Пауза",
                              bg = 'gray94')

def connect(event):
    global points, con_working, bonds
    x = event.x
    y = event.y
    for k in range (len(points)):
        pointx = points[k][0] + window_width/2 + 15
        pointy = points[k][1] + window_height/2 + 15
        if (x - pointx)**2 + (y - pointy)**2 < sense**2 and con_working:
            if len(bonds) == 0 or len(bonds[-1]) == 2:
                bonds.append([k])
            elif len(bonds[-1]) == 1:
                if bonds[-1][0] != k:
                    bonds[-1].append(k)
                else:
                    del bonds[-1]

def delete(event):
    global points, con_working, bonds
    x = event.x
    y = event.y
    highlight_lines_between_points(del_working, points, bonds, x, y, electro, magnet)
    for k in range (len(bonds)-1, -1, -1):
        if len(bonds[k]) == 2:
            dist = dist_mouse_to_line(k, points, bonds, x, y)
            if dist < max_dist and del_working:
                del bonds[k]

root = Tk()
root_frame = Frame(root)
root_frame.pack(side=TOP)
electro = Canvas(root_frame, width=window_width, height=window_height, bg="white")
electro.pack(side=LEFT)
magnet = Canvas(root_frame, width=window_width, height=window_height, bg="white")
magnet.pack(side=RIGHT)
button_frame = Frame(root)
button_frame.pack(side=BOTTOM)
connect_button = Button(button_frame, width = 25, text="Режим соединения: включить",
                        command = connect_check)
connect_button.pack(side=LEFT)
delete_button = Button(button_frame, width = 25, text="Режим удаления: включить",
                        command = delete_check)
delete_button.pack(side=LEFT)
pause_button = Button(button_frame, width = 25, text="Пауза",
                        command = paused_check)
pause_button.pack(side=LEFT)
mouse = Mouse()
points = []
bonds = []
    
make_points()
while True:
    if not paused:
        vectors, points, step = Grand_field(dt)
    x = mouse.x
    y = mouse.y
    create_electro_vectors(vectors, electro)
    create_points(mouse, con_working, points, electro, magnet)
    create_lines_between_points(con_working, points, bonds, x, y, electro, magnet)
    highlight_lines_between_points(del_working, points, bonds, x, y, electro, magnet)
    try:
        root.bind('<Motion>', mouse.coords)
        if con_working:
            root.bind('<Button-1>', connect)
        elif del_working:
            root.bind('<Button-1>', delete)
    except TclError:
        break
    root.update()
    try:
        electro.delete('all')
        magnet.delete('all')
    except TclError:
        break
