#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Библиотека для рисования графических примитивов
"""
import datetime
import math
import os
import tempfile
import time
import sys
from random import choice, randint
from typing import Any, Optional

if sys.version_info.major == 2 or (sys.version_info.major == 3 and sys.version_info.minor < 9):
    print()
    print("""
    Python versions before 3.9 are not supported. Install python 3.9 or over. 
     
    You also may downgrade simple_draw to version 2.8.x with command
    pip install simple-draw<2.9.0
    """)
    sys.exit(1)

import pygame
from pygame import locals as pgl, Surface


background_color = (0, 8, 98)
resolution = (600, 600)
caption = 'Draw the sky'

Color = tuple[int, int, int]

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

_is_inited: bool = False
_screen: Optional[Surface] = None
_background: Optional[Surface] = None
_exit_performed: bool = False
_auto_flip: bool = True
_background_image: Optional[Surface] = None


# Core functions
def _init():
    """
        Инициализация экрана для рисования
    """
    global _screen, _background, _is_inited
    if not _is_inited:
        pygame.init()
        screen_rectangle = pgl.Rect((0, 0), resolution)
        _screen = pygame.display.set_mode(screen_rectangle.size)
        pygame.display.set_caption(caption)
        _background = pygame.Surface(_screen.get_size())  # и ее размер
        _background = _background.convert()
        _background.fill(background_color)  # заполняем цветом
        _screen.blit(_background, (0, 0))
        pygame.display.flip()
        _is_inited = True


def _to_screen(x: int, y: int) -> tuple[int, int]:
    """
        Преобразовать координаты к экранным
    """
    return int(x), resolution[1] - int(y)


def _to_screen_rect(left_bottom: 'Point', right_top: 'Point'):
    """
        Получить прямоугольник в экранных координатах, готовый к отрисовке
    """
    width_height = (right_top.x - left_bottom.x, right_top.y - left_bottom.y)
    return pgl.Rect((left_bottom.x, resolution[1] - right_top.y), width_height)


def set_screen_size(width: int = 600, height: int = 600):
    global resolution
    resolution = (width, height)


def user_want_exit(sleep_time: float = 0) -> bool:
    """
        Проверка ввода от пользователя
    """
    global _exit_performed
    if _exit_performed:
        return True
    if sleep_time:
        sleep(sleep_time)
    try:
        _init()
        for event in pygame.event.get():
            if (event.type == pgl.QUIT) \
                    or (event.type == pgl.KEYDOWN and event.key == pgl.K_ESCAPE) \
                    or (event.type == pgl.KEYDOWN and event.key == pgl.K_q):
                _exit_performed = True
                break
        else:
            _exit_performed = False
        pygame.event.pump()
    except pygame.error as exc:
        _exit_performed = True
    return _exit_performed


def pause():
    """
        Завершение процесса рисования и ожидание закрытия окна
    """
    global _exit_performed
    while not _exit_performed:
        _exit_performed = user_want_exit(sleep_time=0.1)
    pygame.quit()


def quit():
    """
        Завершение процесса рисования, освобождение ресурсов
    """
    pygame.quit()


def start_drawing():
    """
        Начать рисование на экране без автоматического отображения
    """
    global _auto_flip
    _init()
    _auto_flip = False


def finish_drawing():
    """
        Закончить рисование на экране и отобразить нарисованное
    """
    global _auto_flip
    _init()
    _auto_flip = True
    pygame.display.flip()


def sleep(seconds: float = 0):
    """
        Замереть на seconds секунд
    """
    time.sleep(seconds)


def clear_screen():
    """
        Очистить экран
    """
    _init()
    if _background:
        _background.fill(background_color)  # заполняем цветом
        _screen.blit(_background, (0, 0))
        pygame.display.flip()


def get_mouse_state() -> tuple['Point', tuple[bool, bool, bool]]:
    """
        Получить состояние мыши - точку на экране и нажатую кнопку.
        Нажатые кнопки передаются в виде кортежа (True, False, False),
        где bool значат
        (левая кнопка нажата, средняя кнопка нажата, правая кнопка нажата)

    """
    _init()
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    mouse_pos_x, mouse_pos_y = _to_screen(x=mouse_pos_x, y=mouse_pos_y)
    mouse_pos = Point(x=mouse_pos_x, y=mouse_pos_y)
    # точка на экране, где находится мышь

    mouse_buttons = pygame.mouse.get_pressed()
    # кортеж вида (1,0,0) где числа значат:
    # (левая кнопка нажата, средняя кнопка нажата, правая кнопка нажата)

    return mouse_pos, mouse_buttons


# Utils
def _is_point(param: Any) -> bool:
    """
        Является ли параметр координатой?
    """
    return isinstance(param, Point)


def _is_all_points(point_list: list['Point']) -> bool:
    """
        Все ли элементы списка - координаты?
    """
    return all([True for elem in point_list if not _is_point(elem)])


def invert_color(color: Color) -> tuple[int, ...]:
    """
        Инвертировать цвет (выдать комплиментарный по RGB)
    """
    return tuple(255 - i for i in color)


def random_number(a: int = 0, b: int = 300) -> int:
    """
        Выдать случайное целое из диапазона [a,b]
    """
    return randint(a, b)


def random_color() -> Color:
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


def random_point() -> 'Point':
    """
        Сгенерировать случайную точку внутри области рисования
    """
    return Point()


def _to_radians(angle: float) -> float:
    return (float(angle) / 180) * math.pi


def sin(angle: float) -> float:
    """
        Синус угла в градусах
    """
    return math.sin(_to_radians(angle))


def cos(angle: float) -> float:
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
    file_name_img = os.path.join(tempfile.tempdir, "sd_background_image.png")
    take_snapshot(file_name=file_name_img)
    _background_image = pygame.image.load(file_name_img)


def draw_background():
    """
        Вывести картинку в фон
    """
    _init()
    if _background_image is not None:
        _screen.blit(_background_image, (0, 0))


def take_snapshot(file_name: str = None, path: str = None):
    """
        Сделать снимок экрана и сохранить его в файл
    """
    if file_name is None:
        now = datetime.datetime.now()
        current_time = now.strftime('%Y%m%d_%H%M%S_%f')
        file_name = 'sd_snapshot_{}.png'.format(current_time)
    if path:
        file_name = os.path.join(path, file_name)
    _init()
    pygame.image.save(_screen, file_name)

# Primitives
def line(
        start_point: 'Point', end_point: 'Point', 
        color: Color = COLOR_YELLOW, width: int = 1,
):
    """
        Нарисовать линию цветом color толщиной width
        Начиная с точки start
        Заканчивая точкой end
    """
    if not _is_all_points([start_point, end_point]):
        print("'start_point' and 'end_point' params must be Point(x,y)")
        return
    _init()
    pygame.draw.line(_screen, color,
                     start_point.to_screen(), end_point.to_screen(),
                     width)
    if _auto_flip:
        pygame.display.flip()


def lines(
        point_list: list['Point'], color: Color = COLOR_YELLOW,
        closed: bool = False, width: int = 1,
):
    """
        Нарисовать ломанную линию цветом color толщиной width
        Координаты вершин передаются в списке point_list
        Если closed=True - соединить первую и последнюю точки
    """
    if not _is_all_points(point_list):
        print("'point_list' param must contain only Point(x,y)")
        return
    _init()
    converted_point_list = [pos.to_screen() for pos in point_list]
    pygame.draw.lines(_screen, color, closed, converted_point_list, width)
    if _auto_flip:
        pygame.display.flip()


def circle(
        center_position: 'Point', radius: int = 50, 
        color: Color = COLOR_YELLOW, width: int = 1
):
    """
        Нарисовать окружность цветом color
        С центром в точке center_position
        Радиусом radius
        Толщиной линии width
        Если width==0 то заполнить цветом
    """
    if not _is_point(center_position):
        print("'center_position' param must be Point(x,y)")
        return
    _init()
    pygame.draw.circle(_screen, color,
                       center_position.to_screen(), radius, width)
    if _auto_flip:
        pygame.display.flip()


def ellipse(
        left_bottom: 'Point', right_top: 'Point',
        color: Color = COLOR_YELLOW, width: int = 0
):
    """
        Нарисовать эллипс цветом color
        Вписанный в прямоугольник (left_bottom, right_top)
        Толщиной линии width
        Если width==0 то заполнить цветом
    """
    if not _is_all_points([left_bottom, right_top]):
        print("'left_bottom' and 'right_top' params must be Point(x,y)")
        return
    _init()
    rect = _to_screen_rect(left_bottom, right_top)
    pygame.draw.ellipse(_screen, color, rect, width)
    if _auto_flip:
        pygame.display.flip()


def square(
        left_bottom: 'Point', side: int = 50, 
        color: Color = COLOR_YELLOW, width: int = 0,
):
    """
        Нарисовать квадрат цветом color
        С левой нижней вершиной в точке left_bottom
        С длинной стороны side
        Толщиной линии width
        Если width==0, то заполнить цветом
    """
    right_top = Point(left_bottom.x + side, left_bottom.y + side)
    rectangle(left_bottom, right_top, color, width)


def rectangle(
        left_bottom: 'Point', right_top: 'Point', 
        color: Color = COLOR_YELLOW, width: int = 0,
):
    """
        Нарисовать прямоугольник цветом color
        С левой нижней вершиной в точке left_bottom
        С правой верхней вершиной в точке right_top
        Толщиной линии width
        Если width==0, то заполнить цветом
    """
    if not _is_all_points([left_bottom, right_top]):
        print("'left_bottom' and 'right_top' params must be point (x,y,)")
        return
    _init()
    if left_bottom.x > right_top.x or left_bottom.y > right_top.y:
        color = invert_color(color)
    rect = _to_screen_rect(left_bottom, right_top)
    pygame.draw.rect(_screen, color, rect, width)
    if _auto_flip:
        pygame.display.flip()


def polygon(
        point_list: list['Point'], 
        color: Color = COLOR_YELLOW, width: int = 1,
):
    """
        Нарисовать многоугольник цветом color
        Координаты вершин передаются в списке point_list
        Толщиной линии width.
        Если width==0, то заполнить цветом
    """
    if not _is_all_points(point_list):
        print("'point_list' param must contain only points (x,y,)")
        return
    _init()
    converted_point_list = [pos.to_screen() for pos in point_list]
    pygame.draw.polygon(_screen, color, converted_point_list, width)
    if _auto_flip:
        pygame.display.flip()


def snowflake(
        center: 'Point', length: int = 100,
        color: Color = COLOR_YELLOW,
        factor_a: float = 0.6, factor_b: float = 0.35, factor_c: float = 60,
):
    """
        Нарисовать снежинку в точке center с длинной лучей length цветом color
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
        pygame.display.flip()
        _auto_flip = True


# Point support
class Point:
    """Класс точки на экране"""

    def __init__(self, x: float = None, y: float = None):
        self._x = random_number(1, resolution[0]) if x is None else int(x)
        self._y = random_number(1, resolution[1]) if y is None else int(y)

    def to_screen(self) -> tuple[int, int]:
        return int(self._x), resolution[1] - int(self._y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = int(value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = int(value)

    def __str__(self):
        return 'Point(x={}, y={})'.format(self.x, self.y)


def get_point(x: int, y: int) -> 'Point':
    """Получить точку в координате (x,y)"""
    return Point(x=x, y=y)


# Vector support
class Vector:
    """Класс вектора на экране"""

    def __init__(
            self, start_point: Point, direction: float, 
            length: float, width: int = 1,
    ):
        """
            Создать вектор из точки start_point в направлении direction (градусы) длинной length
            Внимание! Параметр width в следующей версии будет удален, 
            используйте .draw(..., width)
        """
        self.start_point = start_point
        direction = (direction * math.pi) / 180
        self.dx = math.cos(direction) * length
        self.dy = math.sin(direction) * length
        self.module = length
        self.width = width

    def _determine_module(self) -> float:
        return math.sqrt(self.dx ** 2 + self.dy ** 2)

    @property
    def end_point(self) -> Point:
        return Point(self.start_point.x + self.dx, self.start_point.y + self.dy)

    @property
    def angle(self) -> float:
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

    def add(self, vector2: 'Vector'):
        """Сложение векторов"""
        self.dx += vector2.dx
        self.dy += vector2.dy
        self.module = self._determine_module()

    def __str__(self):
        return 'vector([%.2f,%.2f],{%.2f,%.2f})' % (
            self.dx, self.dy, self.angle, self.module,
        )

    def __repr__(self):
        return str(self)

    def __nonzero__(self) -> int:
        """Проверка на пустоту"""
        return int(self.module)

    def draw(self, color: Color = COLOR_YELLOW, width: int = None):
        """
            Нарисовать вектор
        """
        width = width if width else self.width
        line(
            start_point=self.start_point, end_point=self.end_point, 
            color=color, width=width,
        )

    def is_tiny(self) -> bool:
        """
            Очень маленький вектор?
        """
        return self.module <= 3

    def multiply(self, factor: float):
        """
            Умножить вектор на скалярное число
        """
        self.dx *= factor
        self.dy *= factor
        self.module = self._determine_module()

    def rotate(self, angle: float):
        """
            Повернуть вектор на угол
        """
        new_angle = self.angle + angle
        self.dx = math.cos(new_angle) * self.module
        self.dy = math.sin(new_angle) * self.module
        self.module = self._determine_module()

    @property
    def length(self) -> float:
        return self.module


def get_vector(
        start_point: Point, angle: float, length: float = 100, width: int = 1,
) -> Vector:
    """
        Получить вектор из точки start, в направлении angle, длиной length
        Внимание! Параметр width в следующей версии будет удален, используйте Vector.draw(..., width)
    """
    return Vector(
        start_point=start_point, direction=angle, length=length, width=width,
    )


def vector(
        start: Point, angle: float, length: float, 
        color: Color = COLOR_YELLOW, width: int = 1,
) -> Optional[Point]:
    """
        Нарисовать вектор цветом color толщиной width
        Из точки start
        В направлении angle
        Длиной length
        Цветом color
        Толщиной width
    """
    if not _is_point(start):
        print("'start' param must be point (x,y,)")
        return
    _init()
    v = Vector(start_point=start, direction=angle, length=length)
    v.draw(color=color, width=width)
    return v.end_point
