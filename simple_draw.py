#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Библиотека для рисования графических примитивов
    v 2.4
"""
import datetime
import math
import os
import tempfile
import time
from random import choice, randint

import turtle

background_color = (0, 8, 98)
resolution = (600, 600)
caption = 'Draw the Turtle!'

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

COLOR_RED = (255, 0, 0)
COLOR_ORANGE = (255, 127, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_CYAN = (0, 255, 255)
COLOR_BLUE = (0, 0, 255)
COLOR_PURPLE = (255, 0, 255)

COLOR_DARK_YELLOW = (127, 127, 0)
COLOR_DARK_ORANGE = (127, 63, 0)
COLOR_DARK_RED = (127, 0, 0)
COLOR_DARK_GREEN = (0, 127, 0)
COLOR_DARK_CYAN = (0, 127, 127)
COLOR_DARK_BLUE = (0, 0, 127)
COLOR_DARK_PURPLE = (127, 0, 127)

_is_inited = False
_screen = None
_background = None
_exit_performed = False
_listen_exit = False
_auto_flip = True
_background_image = None
_turtle = None
_scroll_koef = (4, 8)
_mouse_buttons_state = [0, 0, 0]
_mouse_click_time = 0.1     # Сколько времени в секундах после клика считать нажатой кнопку мыши
_mouse_click_timings = [0, 0, 0]


# Core functions

def _init_mouse_handlers(button_number):
    def _set_mouse_buttons_state(*args, **kwargs):      # оставил арги и кварги, потому что onclick передаёт координаты
        global _mouse_buttons_state, _mouse_click_timings
        _mouse_buttons_state[button_number] = 1
        _mouse_click_timings[button_number] = time.time()
    return _set_mouse_buttons_state


def _check_mouse_click_timings():
    global _mouse_buttons_state, _mouse_click_timings
    for button, timing in enumerate(_mouse_click_timings):
        if _mouse_buttons_state[button] and time.time() - timing > _mouse_click_time:
            _mouse_buttons_state[button] = 0


def _init():
    """
        Инициализация экрана для рисования
    """
    global _screen, _turtle, _is_inited, _mouse_buttons_state
    _check_mouse_click_timings()
    if not _is_inited:
        _screen = turtle.Screen()
        _screen.title(caption)
        # Докидываем несколько пикселей чтобы избавиться от полос прокрутки
        _screen.setup(resolution[0] + _scroll_koef[0], resolution[1] + _scroll_koef[1])
        _screen.setworldcoordinates(8, 7, *resolution)
        _screen.colormode(255)
        _screen.bgcolor(background_color)
        _screen.tracer(n=0)
        _screen.update()

        _turtle = turtle.Turtle()
        _turtle.screen = _screen
        _turtle.hideturtle()
        _turtle.penup()
        _turtle.speed(0)

        # черепаха у мыши обрабатывает только клики, поэтому немного поизвращаемся, чтобы приближенно сэмулировать
        # работу get_pressed из pygame
        # собираем функции-обработчики кликов мышью и вешаем их на клики
        buttons_assoc = [1, 3, 2]   # у черепахи порядок кнопок мыши отличается от pygame, поэтому скорректируем его
        for button in range(0, 3):
            handler = _init_mouse_handlers(button)
            _screen.onclick(handler, buttons_assoc[button])

        _screen.onkey(_screen.bye, 'Q')
        _screen.onkey(_screen.bye, 'q')
        _screen.onkey(_screen.bye, 'Escape')
        _screen.listen()
        _is_inited = True


def _to_screen(x, y):
    """
        Преобразовать координаты к экранным
    """
    return int(x), int(y)


def _to_screen_rect(left_bottom, right_top):
    """
        Получить ширину и высоту прямоуголника в экранных координатах
    """
    return right_top.x - left_bottom.x, right_top.y - left_bottom.y


def set_screen_size(width=600, height=600):
    global resolution
    resolution = (width, height)


# deprecated. Сейчас система в фоне ждёт нажатия кнопок выхода с самого момента инициализации
def user_want_exit(sleep_time=None):
    """
        проверка ввода от пользователя
    """
    pass





def pause():
    """
        Завершение процесса рисования и ожидание закрытия окна
    """
    turtle.done()


def quit():
    """
        Завершение процесса рисования, освобождение ресурсов
    """
    _screen.bye()


def start_drawing():
    """
        Начать рисование на экране без автоматического отображения
    """
    global _auto_flip, _screen
    _init()
    _auto_flip = False


def finish_drawing():
    """
        Закончить рисование на экране и отобразить нарисованное
    """
    global _auto_flip, _screen
    _init()
    _auto_flip = True
    _screen.update()


def sleep(seconds=0):
    """
        Замереть на N секунд
    """
    time.sleep(seconds)


def clear_screen():
    """
        очистить экран
    """
    _init()
    _turtle.reset()
    _turtle.shape('blank')


def get_mouse_state():
    """
        получить состояние мыши - координаты и нажатую кнопку
    """
    _init()
    canvas = _screen.getcanvas()
    # знаю, что protected элементы лучше не трогать, но другого выбора нет. Но я его не изменяю, а только читаю
    mouse_pos_x = canvas.winfo_pointerx() - _screen._root.winfo_rootx() - _scroll_koef[0]
    mouse_pos_y = canvas.winfo_pointery() - _screen._root.winfo_rooty() - resolution[1]
    mouse_pos = Point(x=mouse_pos_x, y=mouse_pos_y)
    #  _mouse_buttons_state - кортеж вида (1,0,0),
    #  где числа значат: (левая кнопка нажата, средня кнопка нажата, правая кнопка нажата)
    #
    return mouse_pos, _mouse_buttons_state


# Utils
def _is_point(param):
    """
        является ли параметр координатой?
    """
    return isinstance(param, Point)


def _is_all_points(point_list):
    """
        все ли элементы списка - координаты?
    """
    return all([True for elem in point_list if not _is_point(elem)])


def invert_color(color):
    """
        Инвертировать цвет (выдать комплиментарный по RGB)
    """
    return tuple(255 - i for i in color)


def random_number(a=0, b=300):
    """
        Выдать случайное целое из диапазона [a,b]
    """
    return randint(a, b)


def random_color():
    """
        Выдать случайный цвет из набора предопределенных
    """
    colors = [
        COLOR_RED,
        COLOR_ORANGE,
        COLOR_YELLOW,
        COLOR_GREEN,
        COLOR_CYAN,
        COLOR_BLUE,
        COLOR_PURPLE,
        COLOR_DARK_YELLOW,
        COLOR_DARK_ORANGE,
        COLOR_DARK_RED,
        COLOR_DARK_GREEN,
        COLOR_DARK_CYAN,
        COLOR_DARK_BLUE,
        COLOR_DARK_PURPLE,
    ]
    return choice(colors)


def random_point():
    """
        Сгенерировать случнайную точку внутри области рисования
    """
    return Point()


def _to_radians(angle):
    return (float(angle) / 180) * math.pi


def sin(angle):
    """
        Синус угла в градусах
    """
    return math.sin(_to_radians(angle))


def cos(angle):
    """
        Косинус угла в градусах
    """
    return math.cos(_to_radians(angle))


def take_background():
    """
        Сохранить снимок экрана во временный файл для фона
    """
    global _background_image
    _init()
    tempfile.gettempdir()
    file_name_img = os.path.join(tempfile.tempdir, 'sd_background_image')
    take_snapshot(file_name=file_name_img)
    _background_image = file_name_img + '.gif'


def draw_background():
    """
        Вывести картинку в фон
    """
    global _screen
    _init()
    if _background_image is not None:
        _screen.bgpic(_background_image)


# TODO разобраться с этим добром
def take_snapshot(file_name=None, path=None):
    """
        сделать снимок экрана и сохранить его в файл
    """
    from PIL import Image, ImageGrab
    if file_name is None:
        now = datetime.datetime.now()
        current_time = now.strftime('%Y%m%d_%H%M%S_%f')
        file_name = 'sd_snapshot_{}'.format(current_time)
    if path:
        file_name = os.path.join(path, file_name)
    _init()
    # _screen.getcanvas().postscript(file=file_name + '.eps')
    x = _screen._root.winfo_x()
    y = _screen._root.winfo_y()
    img = Image.open(file_name + '.eps')
    img.save(file_name + '.png')
    # ImageGrab.grab().crop((x, y, x+resolution[0], y+resolution[1])).save(file_name + '.gif')


def _set_params(turtle, color, width):
    """
        задать параметры рисования фигуры
    """
    turtle.penup()
    turtle.pencolor(*color)
    turtle.fillcolor(*color)
    turtle.pensize(width)


# Primitives
def line(start_point, end_point, color=COLOR_YELLOW, width=1):
    """
        Нарисовать линию цветом color
        Начиная с точки start
        Заканчивая точкой end
    """
    if not _is_all_points([start_point, end_point]):
        print("'start_point' and 'end_point' params must be point (x,y,)")
        return
    _init()
    _set_params(_turtle, color, width)
    _turtle.penup()
    _turtle.setpos(*start_point.to_screen())
    _turtle.pendown()
    _turtle.setpos(*end_point.to_screen())
    _turtle.penup()
    if _auto_flip:
        _screen.update()


def lines(point_list, color=COLOR_YELLOW, closed=False, width=1):
    """
        Нарисовать ломанную линию цветом color
        Координаты вершин передаются в списке point_list
        Если closed=True - соединить первую и последнюю точки
    """
    if not _is_all_points(point_list):
        print("'point_list' param must contain only points (x,y,)")
        return
    _init()
    converted_point_list = [pos.to_screen() for pos in point_list]
    if closed:
        converted_point_list.append(converted_point_list[0])
    _set_params(_turtle, color, width)
    _turtle.penup()
    _turtle.setpos(*converted_point_list[0])
    _turtle.pendown()
    for point in converted_point_list[1:]:
        _turtle.setpos(*point)
    _turtle.penup()
    if _auto_flip:
        _screen.update()


def circle(center_position, radius=50, color=COLOR_YELLOW, width=1):
    """
        Нарисовать окружность цветом color
        С центром в точке center_position
        Радиусом radius
        Толщиной линии width
        Если width==0 то заполнить цветом
    """
    if not _is_point(center_position):
        print("'center_position' param must be point (x,y,)")
        return
    _init()
    _set_params(_turtle, color, width)
    _turtle.penup()
    _turtle.setpos(center_position.to_screen()[0], center_position.to_screen()[1] - radius)
    _turtle.pendown()
    if not width:
        _turtle.begin_fill()
    _turtle.circle(radius)
    _turtle.end_fill()
    _turtle.penup()
    if _auto_flip:
        _screen.update()


def ellipse(left_bottom, right_top, color=COLOR_YELLOW, width=0):
    """
        Нарисовать эллипс цветом color
        Вписанный в прямоугольник (left_bottom, right_top)
        Толщиной линии width
        Если width==0 то заполнить цветом
    """
    if not _is_all_points([left_bottom, right_top]):
        print("'left_bottom' and 'right_top' params must be point (x,y,)")
        return
    _init()
    width_height = _to_screen_rect(left_bottom, right_top)
    _set_params(_turtle, color, width)
    _turtle.penup()

    # у черепашки нет своего овала, так что немного несложной математики
    _turtle.goto(left_bottom.to_screen()[0] + width_height[0] // 2,
                 left_bottom.to_screen()[1] + width_height[1])
    _turtle.pendown()
    if not width:
        _turtle.begin_fill()
    for i in range(0, 361, 10):
        t = i * (math.pi / 180)
        x = width_height[0] * math.sin(t) // 2
        y = width_height[1] * math.cos(t) // 2
        _turtle.goto(x + left_bottom.to_screen()[0] + width_height[0] // 2,
                     y + left_bottom.to_screen()[1] + width_height[1] // 2)
    _turtle.penup()
    _turtle.end_fill()
    if _auto_flip:
        _screen.update()


def square(left_bottom, side=50, color=COLOR_YELLOW, width=0):
    """
        Нарисовать квадрат цветом color
        С левой нижней вершиной в точке left_bottom
        С длинной стороны side
        Толщиной линии width
        Если width==0 то заполнить цветом
    """
    right_top = Point(left_bottom.x + side, left_bottom.y + side)
    rectangle(left_bottom, right_top, color, width)


def rectangle(left_bottom, right_top, color=COLOR_YELLOW, width=0):
    """
        Нарисовать прямоугольник цветом color
        С левой нижней вершиной в точке left_bottom
        С правой верхней вершиной в точке right_top
        Толщиной линии width
        Если width==0 то заполнить цветом
    """
    if not _is_all_points([left_bottom, right_top]):
        print("'left_bottom' and 'right_top' params must be point (x,y,)")
        return
    _init()
    points = [left_bottom, Point(left_bottom.x, right_top.y),
              right_top, Point(right_top.x, left_bottom.y)]
    if not width:
        _turtle.begin_fill()
    lines(points, color=color, width=width, closed=True)
    _turtle.end_fill()
    if _auto_flip:
        _screen.update()


def polygon(point_list, color=COLOR_YELLOW, width=1):
    """
        Нарисовать прямоугольник цветом color
        Координаты вершин передаются в списке point_list
        Толщиной линии width.
        Если width==0 то заполнить цветом
    """
    if not _is_all_points(point_list):
        print("'point_list' param must contain only points (x,y,)")
        return
    _init()
    if not width:
        _turtle.begin_fill()
    lines(point_list, color=color, width=width, closed=True)
    _turtle.end_fill()
    if _auto_flip:
        _screen.update()


def snowflake(center, length=100, color=COLOR_WHITE, factor_a=0.6, factor_b=0.35, factor_c=60):
    """
        нарисовать снежинку в точке center с длинной лучей length цветом color
        factor_a - место ответвления лучиков
        factor_b - длина лучиков
        factor_c - угол отклонения лучиков
    """
    assert 0 < factor_a <= 1
    assert 0 < factor_b <= 1
    assert 0 < factor_c < 180
    global _auto_flip
    if _auto_flip:
        _auto_flip = False
        restore_auto_flip = True
    else:
        restore_auto_flip = False
    for angle in range(0, 361, 60):
        arm = Vector(center, angle, length)
        arm.draw(color)
        arm.multiply(factor_a)
        left_sub_arm = Vector(arm.end_point, angle + factor_c, length * factor_b)
        left_sub_arm.draw(color)
        right_sub_arm = Vector(arm.end_point, angle - factor_c, length * factor_b)
        right_sub_arm.draw(color)
    if restore_auto_flip:
        _screen.update()
        _auto_flip = True


# Point support
class Point:
    """
        Класс точки экрана
    """

    def __init__(self, x=None, y=None):
        self._x = random_number(1, resolution[0]) if x is None else int(x)
        self._y = random_number(1, resolution[1]) if y is None else int(y)

    def to_screen(self):
        return int(self._x), int(self._y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = int(value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = int(value)

    def __str__(self):
        return 'Point(x={}, y={})'.format(self.x, self.y)


def get_point(x, y):
    """
        получить точку в координате (x,y)
    """
    return Point(x=x, y=y)


# Vector support
class Vector:
    """Класс математического вектора"""

    def __init__(self, start_point, direction, length, width=1):
        """
            Создать вектор из точки start_point в направлении direction (градусы) длинной lenght
            Внимание! Параметр width в следующей версии будет удален, используйте .draw(..., width)
        """
        self.start_point = start_point
        direction = (direction * math.pi) / 180
        self.dx = math.cos(direction) * length
        self.dy = math.sin(direction) * length
        self.module = length
        self.width = width

    def _determine_module(self):
        return math.sqrt(self.dx ** 2 + self.dy ** 2)

    @property
    def end_point(self):
        return Point(self.start_point.x + self.dx, self.start_point.y + self.dy, )

    @property
    def angle(self):
        if self.dx == 0:
            if self.dy >= 0:
                return 90
            else:
                return 270
        else:
            angle = math.atan(self.dy / self.dx) * (180 / math.pi)
            if self.dx < 0:
                angle += 180
        return angle

    def add(self, vector2):
        """Сложение векторов"""
        self.dx += vector2.dx
        self.dy += vector2.dy
        self.module = self._determine_module()

    def __str__(self):
        return 'vector([%.2f,%.2f],{%.2f,%.2f})' % (self.dx, self.dy, self.angle, self.module)

    def __repr__(self):
        return str(self)

    def __nonzero__(self):
        """Проверка на пустоту"""
        return int(self.module)

    def draw(self, color=COLOR_YELLOW, width=None):
        """
            Нарисовать вектор
        """
        width = width if width else self.width
        line(start_point=self.start_point, end_point=self.end_point, color=color, width=width)

    def is_tiny(self):
        """
            Очень маленький вектор?
        """
        return self.module <= 3

    def multiply(self, factor):
        """
            Умножить вектор на скалярное число
        """
        self.dx *= factor
        self.dy *= factor
        self.module = self._determine_module()

    def rotate(self, angle):
        """
            Повернуть вектор на угол
        """
        new_angle = self.angle + angle
        self.dx = math.cos(new_angle) * self.module
        self.dy = math.sin(new_angle) * self.module
        self.module = self._determine_module()

    @property
    def length(self):
        return self.module


def get_vector(start_point, angle, length=100, width=1):
    """
        Получить вектор из точки start, в направлении angle, длиной length
        Внимание! Параметр width в следующей версии будет удален, используйте Vector.draw(..., width)
    """
    return Vector(start_point=start_point, direction=angle, length=length, width=width)


def vector(start, angle, length, color=COLOR_YELLOW, width=1):
    """
        Нарисовать вектор цветом color толщиной width
        Из точки start
        В направлении angle
        Длиной length
    """
    if not _is_point(start):
        print("'start' param must be point (x,y,)")
        return
    _init()
    v = Vector(start_point=start, direction=angle, length=length)
    v.draw(color=color, width=width)
    return v.end_point
