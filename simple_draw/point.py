# -*- coding: utf-8 -*-

from . import constants, utils


class Point:
    """
        Класс точки экрана
    """

    def __init__(self, x=None, y=None):
        self._x = utils.random_number(1, constants.resolution[0]) if x is None else int(x)
        self._y = utils.random_number(1, constants.resolution[1]) if y is None else int(y)

    def to_screen(self):
        return int(self._x), constants.resolution[1] - int(self._y)

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


def get_point(x,y):
    """
        получить точку в координате (x,y)
    """
    return Point(x=x, y=y)