# -*- coding: utf-8 -*-
import math
from random import randint, choice

from . import constants, point


def _is_point(param):
    """
        является ли параметр координатой?
    """
    return isinstance(param, point.Point)


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
        constants.COLOR_RED,
        constants.COLOR_ORANGE,
        constants.COLOR_YELLOW,
        constants.COLOR_GREEN,
        constants.COLOR_CYAN,
        constants.COLOR_BLUE,
        constants.COLOR_PURPLE,
        constants.COLOR_DARK_YELLOW,
        constants.COLOR_DARK_ORANGE,
        constants.COLOR_DARK_RED,
        constants.COLOR_DARK_GREEN,
        constants.COLOR_DARK_CYAN,
        constants.COLOR_DARK_BLUE,
        constants.COLOR_DARK_PURPLE,
    ]
    return choice(colors)


def random_point():
    """
        Сгенерировать случнайную точку внутри области рисования
    """
    return point.Point()


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