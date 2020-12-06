from vect import *
from vect_interface import *

# CONSTANTS
con_working = False
del_working = False
con_clicks = 0
del_clicks = 0
pau_clicks = 0
dt = 0.001
paused = False
window_width = 610
window_height = 610
window_settings = [window_width, window_height, x_size, y_size]

def electro():
    global mode
    mode = 0
def magnet():
    global mode
    mode = 2
def gravit():
    global mode
    mode = 1

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
    global points, con_working, bonds, flag
    x = event.x
    y = event.y
    for k in range (len(points)):
        pointx = scale_x(points[k][0], window_settings)
        pointy = scale_y(points[k][1], window_settings)
        if (x - pointx)**2 + (y - pointy)**2 < sense**2 and con_working:
            if len(bonds) == 0 or len(bonds[-1]) == 2:
                bonds.append([k])
            elif len(bonds[-1]) == 1:
                if bonds[-1][0] != k:
                    flag = True
                    bonds[-1].append(k)
                    Links[bonds[-1][0]][bonds[-1][1]] = 1
                    Links[bonds[-1][1]][bonds[-1][0]] = 1
                else:
                    del bonds[-1]

def delete(event):
    global points, con_working, bonds, flag
    x = event.x
    y = event.y
    highlight_lines_between_points(del_working, points, bonds, x, y,
                                   window_settings, screen)
    for k in range (len(bonds)-1, -1, -1):
        if len(bonds[k]) == 2:
            dist = dist_mouse_to_line(k, points, bonds, x, y, window_settings)
            if dist < max_dist and del_working:
                flag = True
                Links[bonds[k][0]][bonds[k][1]] = 0
                Links[bonds[k][1]][bonds[k][0]] = 0
                del bonds[k]

flag = False
root = Tk()
mode_frame = Frame(root)
mode_frame.pack(side=TOP)
electro_button = Button(mode_frame, width = 25, text="Электрическое поле",
                        command = electro)
electro_button.pack(side=LEFT)
magnet_button = Button(mode_frame, width = 25, text="Магнитное поле",
                       command = magnet)
magnet_button.pack(side=LEFT)
gravit_button = Button(mode_frame, width = 25, text="Гравитационное поле",
                       command = gravit)
gravit_button.pack(side=LEFT)
root_frame = Frame(root)
root_frame.pack(side=TOP)
screen = Canvas(root_frame, width=window_width, height=window_height, bg="white")
screen.pack(side=LEFT)
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
make_points()
Re_calc_all()
mode = 0
Field, points, step, bodies = Grand_field(mode, dt)
bonds = create_first_bonds(points, Links)

while True:
    if flag:
        Re_calc_all()
        flag = False
    if not paused:
        Field, points, step, bodies = Grand_field(mode, dt)
    vectors = Field[0]
    x = mouse.x
    y = mouse.y
    if mode == 0:
        create_electro_vectors(vectors, window_settings, screen)
    elif mode == 1:
        create_gravit_vectors(vectors, window_settings, screen)
    else:
        create_magnet_squares(vectors, x_size, y_size, step, window_settings,
                              screen)
    create_points(mouse, con_working, points,
                  window_settings, screen)
    create_lines_between_points(con_working, points, bonds, x, y,
                                window_settings, screen)
    highlight_lines_between_points(del_working, points, bonds, x, y,
                                   window_settings, screen)
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
        screen.delete('all')
    except TclError:
        break
