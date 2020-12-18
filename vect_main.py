'''
Это главный модуль всего проекта. Он не содержит ни одного класса.
Его задача заключаеся в создании графического интерефейса,
    
    но детальном управлении им - 
    для этих целей существует модуль vect_interface, 
реализации взаимодействия с пользователем и реализации взаимоействия между 
модулями вычислительной (vect) и грфаической (vect_interface) частей.
Функции:
    # Обработка нажатия на кнопки:
    electro() - электричсекое поле
    magnet() - магнитное поле
    gravit() - гравитационное поле
    add_check() - создание точки
    rem_check() - удаление точки
    connect_check() - соединения точек
    delete_check() - разъединения точек
    paused_check() - постановка на паузу
    
    ###
    connect(event) - соединение точек
    delete(event) - разъединение точек
    create_point(event) - создание новой точки
    
    ###
    on_closing() - обработка выхода из программы
'''

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
window_width = 400
window_height = 400
max_points = 10
min_scale = 300
max_scale = 1200
min_mass = 1
max_mass = 500
min_charge = -50
max_charge = 50
flag = False
mode = 0  # Отвечает за тип отображаемого поля: 0 - электр., 1 - гравитационное, 2 - магнитное
bonds = []
Links = [[]]

ending_message = "Вы покидаете виртуальный мир и возвращаетесь в реальный." + '\n' + \
                 "Не забудьте, что НАСТОЯЩИЕ гравитационные и электромагнитные поля могут Вас убить!" + '\n' + '\n' +\
                    "Вы действительно хотите выйти?"


starting_message = 'Данный продукт является результатом труда команды разработчиков DDR-crew.' + '\n' +'\n'+ \
                'Авторы продукта не несут отсветсвенности за приченный пользоватлям ущерб здоровью или ущерб любого иного характера.' +'\n' + '\n' +\
                'Данный продукт является общественным достоянием, поэтому разрешено копирование, хранение и использование \
                исходных материалов в любых целях.' + '\n' + '\n' +\
                'Документация к использованию изложена в файлах "README.md" и "documentaion.pdf".' + '\n' + '\n' +\
                'Благодарим за то, что выбрали нас!'

rules = 'Правила.'

def electro():
    '''
    Эта функция выделяет кнопку электрического поля. Она вызывается при активации отображения эл. поля
    '''
    global mode
    mode = 0
    electro_button.config(bg='cyan')
    magnet_button.config(bg='gray94')
    gravit_button.config(bg='gray94')

def magnet():
    '''
    Эта функция выделяет кнопку магнитного поля. Она вызывается при активации отображения маг. поля
    '''
    global mode
    mode = 2
    electro_button.config(bg='gray94')
    magnet_button.config(bg='deep sky blue')
    gravit_button.config(bg='gray94')

def gravit():
    '''
    Эта функция выделяет кнопку гравитационного поля. Она вызывается при активации отображения гр. поля
    '''
    global mode
    mode = 1
    electro_button.config(bg='gray94')
    magnet_button.config(bg='gray94')
    gravit_button.config(bg='SlateBlue1')


def add_check():
    '''
    Функция обрабатывает нажатие на кнопку "Режим добавления"
    '''
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
        delete_button.config(text="Режим разъединения: включить",
                          bg = 'gray94')
        rem_working = False
        rem_clicks = 0
        remove_button.config(text="Режим удаления точек: включить",
                          bg = 'gray94')

def rem_check():
    '''
    Функция обрабатывает нажатие на кнопку "Режим удаления (точек)"
    '''
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
        delete_button.config(text="Режим разъединения: включить",
                              bg = 'gray94')
        add_working = False
        add_clicks = 0
        add_button.config(text="Режим добавления точек: включить",
                              bg = 'gray94')
        
def connect_check():
    '''
    Функция обрабатывает нажатие на кнопку "Режим соединения"
    '''
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
        delete_button.config(text="Режим разъединения: включить",
                              bg = 'gray94')
        rem_working = False
        rem_clicks = 0
        remove_button.config(text="Режим удаления точек: включить",
                              bg = 'gray94')

def delete_check():
    '''
    Функция обрабатывает нажатие на кнопку "Режим разъединения"
    '''
    global add_clicks, rem_clicks, con_clicks, del_clicks
    global add_working, rem_working, con_working, del_working
    del_clicks += 1
    if not rem_working and not con_working and not add_working:
        if del_clicks % 2 == 1:
            delete_button.config(text="Режим разъединения: выключить",
                              bg = 'blue')
            del_working = True
        else:
            delete_button.config(text="Режим разъединения: включить",
                              bg = 'gray94')
            del_working = False
    elif (rem_working or con_working or add_working) and del_clicks % 2 == 1:
        del_working = True
        delete_button.config(text="Режим разъединения: выключить",
                              bg = 'blue')
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
    '''
    Функция брабатывает нажатие на кнопку "Пауза/Возобновить"
    '''
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
    '''
    Функция прорисовывает и полностью обрабатывает процесс соединения двух точек. Она изменяет массив Links из vect.py
    
    Параметры:
        event - обрабатываемое в данный момент Tkinter событие
    '''
    global points, con_working, bonds, flag
    x = event.x
    y = event.y
    for k in range (len(points)):
        pointx = scale_x(points[k][0], window_settings)
        pointy = scale_y(points[k][1], window_settings)
        if (x - pointx)**2 + (y - pointy)**2 < sense**2:
            if len(bonds) == 0 or len(bonds[-1]) == 2:
                bonds.append([k])
            elif len(bonds[-1]) == 1:
                if bonds[-1][0] != k:
                    flag = True
                    bonds[-1].append(k)
                    ind1 = bonds[-1][0]
                    ind2 = bonds[-1][1]
                    Links[ind1][ind2] = 1
                    Links[ind2][ind1] = 1
                else:
                    del bonds[-1]


def delete(event):
    '''
    Функция прорисовывает и полностью обрабатывает процесс разъединения двух точек. Она изменяет массив Links из vect.py
    
    Параметры:
        event - обрабатываемое в данный момент Tkinter событие
    '''
    global points, con_working, bonds, flag
    x = event.x
    y = event.y
    highlight_lines_between_points(del_working, points, bonds, x, y,
                                   window_settings, screen)
    for k in range (len(bonds)-1, -1, -1):
        if len(bonds[k]) == 2:
            dist = dist_mouse_to_line(k, points, bonds, x, y, window_settings)
            if dist < max_dist:
                flag = True
                Links[bonds[k][0]][bonds[k][1]] = 0
                Links[bonds[k][1]][bonds[k][0]] = 0
                del bonds[k]


def create_point(event):
    '''
    Функция обрабатывает событие Tkinter - event и вызывает функцию из vect.py, которая создаёт мат. точку с кординатами (x, y)
    
    Параметры:
        event - обрабатываемое в данный момент Tkinter событие
    '''
    x = scale_x_back(event.x, window_settings)
    y = scale_y_back(event.y, window_settings)
    mass = mass_scale.get()
    charge = charge_scale.get()
    if event.widget == screen:
        add_point(x, y, mass, charge, Links)

def remove_point(event):
    '''
    Функция обрабатывает событие Tkinter - event и вызывает функцию из vect.py, которая удаляет мат. точку с кординатами (x, y)
    
    Параметры:
        event - обрабатываемое в данный момент Tkinter событие
    '''
    x = event.x
    y = event.y
    for k in range (len(points)-1, -1, -1):
        pointx = scale_x(points[k][0], window_settings)
        pointy = scale_y(points[k][1], window_settings)
        if (x - pointx)**2 + (y - pointy)**2 < sense**2 and event.widget == screen:
            for i in range (len(bonds)-1, -1, -1):
                if k in bonds[i]:
                    del bonds[i]
                elif k not in bonds[i]:
                    if bonds[i][0] > k:
                        bonds[i][0] -= 1
                    if bonds[i][1] > k:
                        bonds[i][1] -= 1
            del_point(points[k][0], points[k][1], Links)

def show_rules():
    '''
    Функция выводит правила пользования. 
    '''
    messagebox.showinfo("Правила", rules)
def on_closing():
    '''
    Функция просто выводит на экран предупреждающее о попытке выхода окно. 
    '''
    if messagebox.askyesno("Внимание!", ending_message):
        root.destroy()

root = Tk()

# При открытии приложения показывается "Дисклеймер"
messagebox.showinfo('Добро пожаловать!', starting_message)

# Создание протокола обработки выхода пользователя из приложения
root.protocol("WM_DELETE_WINDOW", on_closing)


# Название окна
root.title("Vecield")

### Весь код дальше относится к созданию графического окружения, но не работе с ним. Данные действия проблематично 
### описать в функциях, т.к. необходимо постянно передавать глобальные объекты, к примеру, mode_frame и т.д.

mode_frame = Frame(root)
mode_frame.pack(side=TOP)
# Создание кнопки переключения на правила пользования
rules_button = Button(mode_frame, width = 25, text="Правила",
                        command = show_rules)
rules_button.pack(side=TOP)
# Создание кнопки переключения на элекрическое поле
electro_button = Button(mode_frame, width = 25, text="Электрическое поле",
                        command = electro, bg = 'cyan')
electro_button.pack(side=LEFT)

# Создание кнопки переключения на магнитное поле
magnet_button = Button(mode_frame, width = 25, text="Магнитное поле",
                       command = magnet)
magnet_button.pack(side=LEFT)

# Создание кнопки переключния на гравитационное поле
gravit_button = Button(mode_frame, width = 25, text="Гравитационное поле",
                       command = gravit)
gravit_button.pack(side=LEFT)

###
root_frame = Frame(root)
root_frame.pack(side=TOP)

# Создание области отображения полей в окне
screen = Canvas(root_frame, width=window_width, height=window_height, bg="black")
screen.pack(side=LEFT)


button_frame = Frame(root)
button_frame.pack(side=TOP)


button2_frame = Frame(root)
button2_frame.pack(side=TOP)

point_features = Frame(root)
point_features.pack(side=TOP)

# Создание кнопки создания точек
# width - её ширина
add_button = Button(button2_frame, width = 37,
                    text="Режим добавления точек: включить",
                    command = add_check)
add_button.pack(side=LEFT)

# Создание кнопки удаления точек
# width - её ширина
remove_button = Button(button2_frame, width = 37,
                    text="Режим удаления точек: включить",
                    command = rem_check)
remove_button.pack(side=LEFT)

# Создание кнопки соединения точек
# width - её ширина
connect_button = Button(button_frame, width = 37, text="Режим соединения: включить",
                        command = connect_check)
connect_button.pack(side=LEFT)

# Создание кнопки разъединения точек
# width - её ширина
delete_button = Button(button_frame, width = 37, text="Режим разъединения: включить",
                        command = delete_check)
delete_button.pack(side=LEFT)

# Создание кнопки постановки на паузу и возобновления
# width - её ширина
pause_button = Button(button_frame, width = 20, text="Пауза",
                        command = paused_check)
pause_button.pack(side=LEFT)

mass_label = Label(point_features, text="Масса, кг")
mass_scale = Scale(point_features, from_=min_mass,
                  to=max_mass, orient=HORIZONTAL)
mass_label.pack(side=LEFT)
mass_scale.pack(side=LEFT)
charge_label = Label(point_features, text="Заряд, Кл")
charge_scale = Scale(point_features, from_=min_charge,
                  to=max_charge, orient=HORIZONTAL)
charge_label.pack(side=LEFT)
charge_scale.pack(side=LEFT)

# Создание ползунка, изменяющего масштаб поля
scale_label = Label(point_features, text="Масштаб")
scale = Scale(point_features, from_=min_scale,
                  to=max_scale, orient=HORIZONTAL)
scale_label.pack(side=LEFT)
scale.pack(side=LEFT)

mouse = Mouse()

while True:
    if Links == []:
        Links = [[]]
    y_size = x_size = scale.get()
    window_settings = [window_width, window_height, x_size, y_size]
    if flag:
        try:
            Re_calc_all(Links)
            flag = False
        except ValueError:
            pass
    x = mouse.x
    y = mouse.y
    try:
        Field, points, step, bodies = Grand_field(x_size, y_size, mode, paused, dt)
    except ZeroDivisionError:
        if paused:
            Field = [[], [], []]
        else:
            Field = [[]]
        points = []
        step = 0
    if paused:  # Прорисовка векторов всех полей в режиме паузы
        if mode == 0:
            vectors = Field[0]
            create_electro_vectors(vectors, window_settings, screen)
        elif mode == 1:
            vectors = Field[1]
            create_gravit_vectors(vectors, window_settings, screen)
        else:
            vectors = Field[2]
            create_magnet_squares(vectors, step, window_settings,
                                  screen)
    else:  # Прорисовка только активного поля в работющем режиме
        vectors = Field[0]
        if mode == 0:
            create_electro_vectors(vectors, window_settings, screen)
        elif mode == 1:
            create_gravit_vectors(vectors, window_settings, screen)
        else:
            create_magnet_squares(vectors, step, window_settings,
                                  screen)

    create_points(mouse, con_working, rem_working, points,
                  window_settings, screen)
    create_lines_between_points(con_working, points, bonds, x, y,
                                window_settings, screen)
    highlight_lines_between_points(del_working, points, bonds, x, y,
                                   window_settings, screen)
    
    try:  # Определение, что будет вызывать нажатие мыши на экран
        root.bind('<Motion>', mouse.coords)
        if con_working:
            root.bind('<Button-1>', connect)
        elif del_working:
            root.bind('<Button-1>', delete)
        elif add_working:
            if len(points) <= max_points - 1:
                root.bind('<Button-1>', create_point)
            else:
                root.unbind('<Button-1>')
                add_working = False
                add_clicks = 0
                add_button.config(text = 'Режим добавления точек: недоступен',
                                  bg = 'gray')
        elif rem_working:
            root.bind('<Button-1>', remove_point)
    except TclError:
        break
    if len(points) <= max_points - 1 and not add_working:
        add_button.config(text = 'Режим добавления точек: включить',
                                  bg = 'gray94')
    root.update()
    try:
        screen.delete('all')
    except TclError:
        break
        messagebox.showwarning('Внимание!', ending_message)
