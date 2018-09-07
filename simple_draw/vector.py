# -*- coding: utf-8 -*-
import math

from . import core, point, constants, primitives, utils


class Vector:
    """Класс математического вектора"""

    def __init__(self, start_point, direction, length, width=1):
        """Создать вектор из точки start_point в направлении direction (градусы) длинной lenght"""
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
        return point.Point(self.start_point.x + self.dx, self.start_point.y + self.dy, )

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

    def draw(self, color=constants.COLOR_YELLOW):
        """
            Нарисовать вектор
        """
        primitives.line(start_point=self.start_point, end_point=self.end_point, color=color, width=self.width)

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
        Получить вектор из точки start
        в направлении angle
        длинной length
    """
    return Vector(start_point=start_point, direction=angle, length=length, width=width)


def vector(start, angle, length, color=constants.COLOR_YELLOW):
    """
        Нарисовать вектор цветом color
        Из точки start
        В направлении angle
        Длинной length
    """
    if not utils._is_point(start):
        print("'start' param must be point (x,y,)")
        return
    core._init()
    v = Vector(start, angle, length)
    v.draw(color)
    return v.end_point