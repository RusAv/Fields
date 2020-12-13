from vect import *
from vect_interface import *
from tkinter import messagebox

# CONSTANTS
add_working = False
rem_working = False
con_working = False
del_working = False
add_clicks = 0
rem_clicks = 0
con_clicks = 0
del_clicks = 0
pau_clicks = 0
dt = 0.001
x_size = 300
y_size = 300
paused = False
window_width = 610
window_height = 610

def electro():
    global mode
    mode = 0
    electro_button.config(bg='cyan')
    magnet_button.config(bg='gray94')
    gravit_button.config(bg='gray94')

def magnet():
    global mode
    mode = 2
    electro_button.config(bg='gray94')
    magnet_button.config(bg='deep sky blue')
    gravit_button.config(bg='gray94')

def gravit():
    global mode
    mode = 1
    electro_button.config(bg='gray94')
    magnet_button.config(bg='gray94')
    gravit_button.config(bg='SlateBlue1')

def add_check():
    global add_clicks, rem_clicks, con_clicks, del_clicks
    global add_working, rem_working, con_working, del_working
    add_clicks += 1
    if not rem_working and not con_working and not del_working:
        if add_clicks % 2 == 1:
            add_button.config(text="Режим добавления точек: выключить",
                              bg = 'orange')
            add_working = True
        else:
            add_button.config(text="Режим добавления точек: включить",
                              bg = 'gray94')
            add_working = False
    elif (rem_working or con_working or del_working) and add_clicks % 2 == 1:
        add_working = True
        add_button.config(text="Режим добавления точек: выключить",
                              bg = 'orange')
        con_working = False
        con_clicks = 0
        connect_button.config(text="Режим соединения: включить",
                              bg = 'gray94')
        del_working = False
        del_clicks = 0
        delete_button.config(text="Режим удаления: включить",
                          bg = 'gray94')
        rem_working = False
        rem_clicks = 0
        remove_button.config(text="Режим удаления точек: включить",
                          bg = 'gray94')

def rem_check():
    global add_clicks, rem_clicks, con_clicks, del_clicks
    global add_working, rem_working, con_working, del_working
    rem_clicks += 1
    if not add_working and not con_working and not del_working:
        if rem_clicks % 2 == 1:
            remove_button.config(text="Режим удаления точек: выключить",
                              bg = 'purple')
            rem_working = True
        else:
            remove_button.config(text="Режим удаления точек: включить",
                              bg = 'gray94')
            rem_working = False
    elif (add_working or con_working or del_working) and rem_clicks % 2 == 1:
        rem_working = True
        remove_button.config(text="Режим удаления точек: выключить",
                              bg = 'purple')
        con_working = False
        con_clicks = 0
        connect_button.config(text="Режим соединения: включить",
                              bg = 'gray94')
        del_working = False
        del_clicks = 0
        delete_button.config(text="Режим удаления: включить",
                          bg = 'gray94')
        add_working = False
        add_clicks = 0
        add_button.config(text="Режим добавления точек: включить",
                          bg = 'gray94')
        
def connect_check():
    global add_clicks, rem_clicks, con_clicks, del_clicks
    global add_working, rem_working, con_working, del_working, bonds
    con_clicks += 1
    if not rem_working and not del_working and not add_working:
        if con_clicks % 2 == 1:
            connect_button.config(text="Режим соединения: выключить",
                              bg = 'red')
            con_working = True
        else:
            connect_button.config(text="Режим соединения: включить",
                              bg = 'gray94')
            con_working = False
    elif (rem_working or del_working or add_working) and con_clicks % 2 == 1:
        con_working = True
        connect_button.config(text="Режим соединения: выключить",
                              bg = 'red')
        add_working = False
        add_clicks = 0
        add_button.config(text="Режим добавления точек: включить",
                              bg = 'gray94')
        del_working = False
        del_clicks = 0
        delete_button.config(text="Режим удаления: включить",
                          bg = 'gray94')
        rem_working = False
        rem_clicks = 0
        remove_button.config(text="Режим удаления точек: включить",
                          bg = 'gray94')

def delete_check():
    global add_clicks, rem_clicks, con_clicks, del_clicks
    global add_working, rem_working, con_working, del_working
    del_clicks += 1
    if not rem_working and not con_working and not add_working:
        if del_clicks % 2 == 1:
            delete_button.config(text="Режим удаления: выключить",
                              bg = 'blue')
            del_working = True
        else:
            delete_button.config(text="Режим удаления: включить",
                              bg = 'gray94')
            del_working = False
    elif (rem_working or con_working or add_working) and del_clicks % 2 == 1:
        del_working = True
        delete_button.config(text="Режим удаления: выключить",
                              bg = 'red')
        add_working = False
        add_clicks = 0
        add_button.config(text="Режим добавления точек: включить",
                              bg = 'gray94')
        con_working = False
        con_clicks = 0
        connect_button.config(text="Режим соединения: включить",
                          bg = 'gray94')
        rem_working = False
        rem_clicks = 0
        remove_button.config(text="Режим удаления точек: включить",
                          bg = 'gray94')
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

def create_point(event):
    x = event.x
    y = event.y
    if add_working:
        add_point(x,y,x_size,y_size)



root = Tk()


def on_closing():
    if messagebox.askyesno("Внимание!",
                                "Вы пытаетесь покинуть виртуальный мир и возвратиться в реальный." + '\n' + \
                                "Не забудьте, что НАСТОЯЩИЕ гравитационные и магнитные поля могут Вас убить!" + '\n' + '\n' +\
                                "Вы действительно хотите выйти?"):
        root.destroy()


flag = False
messagebox.showinfo('Добро пожаловать!', 
		'Данный продукт является результатом труда команды разработчиков DDR-crew.' + '\n' +'\n'+ \
                'Авторы продукта не несут отсветсвенности за приченный пользоватлям ущерб здоровью или ущерб любого иного характера.' +'\n' + '\n' +\
                'Данный продукт является общественным достоянием, поэтому разрешено копирование, хранение и использование \
                исходных материалов в любых целях.' + '\n' + '\n' +\
                'Документация к использованию изложена в файлах "README.md" и "Documentaion.pdf".' + '\n' + '\n' +\
                'Благодарим за то, что выбрали нас!'
		)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.title("Vecield")

mode_frame = Frame(root)
mode_frame.pack(side=TOP)
electro_button = Button(mode_frame, width = 25, text="Электрическое поле",
                        command = electro, bg = 'cyan')
electro_button.pack(side=LEFT)
magnet_button = Button(mode_frame, width = 25, text="Магнитное поле",
                       command = magnet)
magnet_button.pack(side=LEFT)
gravit_button = Button(mode_frame, width = 25, text="Гравитационное поле",
                       command = gravit)
gravit_button.pack(side=LEFT)
root_frame = Frame(root)
root_frame.pack(side=TOP)
screen = Canvas(root_frame, width=window_width, height=window_height, bg="black")
screen.pack(side=LEFT)
button_frame = Frame(root)
button_frame.pack(side=TOP)
button2_frame = Frame(root)
button2_frame.pack(side=TOP)
add_button = Button(button2_frame, width = 37,
                    text="Режим добавления точек: включить",
                    command = add_check)
add_button.pack(side=LEFT)
remove_button = Button(button2_frame, width = 37,
                    text="Режим удаления точек: включить",
                    command = rem_check)
remove_button.pack(side=LEFT)
connect_button = Button(button_frame, width = 24, text="Режим соединения: включить",
                        command = connect_check)
connect_button.pack(side=LEFT)
delete_button = Button(button_frame, width = 22, text="Режим удаления: включить",
                        command = delete_check)
delete_button.pack(side=LEFT)
pause_button = Button(button_frame, width = 20, text="Пауза",
                        command = paused_check)
pause_button.pack(side=LEFT)
scale = Scale(button2_frame, variable=x_size, from_=300,
                  to=1200, orient=HORIZONTAL)
scale.pack(side=LEFT)
mouse = Mouse()
make_points(x_size, y_size)
Re_calc_all()
mode = 0
Field, points, step, bodies = Grand_field(x_size, y_size, dt)
bonds = create_first_bonds(points, Links)

while True:
    y_size = x_size = scale.get()
    window_settings = [window_width, window_height, x_size, y_size]
    if flag:
        Re_calc_all()
        flag = False
    if not paused:
        Field, points, step, bodies = Grand_field(x_size, y_size, dt)
    x = mouse.x
    y = mouse.y
    if mode == 0:
        vectors = Field[0]
        create_electro_vectors(vectors, window_settings, screen)
    elif mode == 1:
        vectors = Field[1]
        create_gravit_vectors(vectors, window_settings, screen)
    else:
        vectors = Field[2]
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
        elif add_working:
            root.bind('<Button-1>', create_point)

    except TclError:
        break
    root.update()
    try:
        screen.delete('all')
    except TclError:
        break
        messagebox.showwarning("Внимание!",
                                "Вы покидаете виртуальный мир и возвращаетесь в реальный" + '\n' + \
                                "Не забудьте, что НАСТОЯЩИЕ гравитационные и магнитные поля могут Вас убить!" + '\n' + '\n' +\
                                "Удачи!")
