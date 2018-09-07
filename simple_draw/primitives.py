# -*- coding: utf-8 -*-
import pygame

from . import core, utils, point, vector, constants as const


def line(start_point, end_point, color=const.COLOR_YELLOW, width=1):
    """
        Нарисовать линию цветом color
        Начиная с точки start
        Заканчивая точкой end
    """
    if not utils._is_all_points([start_point, end_point]):
        print("'start_point' and 'end_point' params must be point (x,y,)")
        return
    core._init()
    pygame.draw.line(core._screen, color,
                     start_point.to_screen(), end_point.to_screen(),
                     width)
    if core._auto_flip:
        pygame.display.flip()


def lines(point_list, color=const.COLOR_YELLOW, closed=False):
    """
        Нарисовать ломанную линию цветом color
        Координаты вершин передаются в списке point_list
        Если closed=True - соединить первую и последнюю точки
    """
    if not utils._is_all_points(point_list):
        print("'point_list' param must contain only points (x,y,)")
        return
    core._init()
    converted_point_list = [pos.to_screen() for pos in point_list]
    pygame.draw.lines(core._screen, color, closed, converted_point_list)
    if core._auto_flip:
        pygame.display.flip()


def circle(center_position, radius=50, color=const.COLOR_YELLOW, width=1):
    """
        Нарисовать окружность цветом color
        С центром в точке center_position
        Радиусом radius
        Толщиной линии width
        Если width==0 то заполнить цветом
    """
    if not utils._is_point(center_position):
        print("'center_position' param must be point (x,y,)")
        return
    core._init()
    pygame.draw.circle(core._screen, color,
                       center_position.to_screen(), radius, width)
    if core._auto_flip:
        pygame.display.flip()


def ellipse(left_bottom, right_top, color=const.COLOR_YELLOW, width=0):
    """
        Нарисовать эллипс цветом color
        Вписанный в прямоугольник (left_bottom, right_top)
        Толщиной линии width
        Если width==0 то заполнить цветом
    """
    if not utils._is_all_points([left_bottom, right_top]):
        print("'left_bottom' and 'right_top' params must be point (x,y,)")
        return
    core._init()
    rect = core._to_screen_rect(left_bottom, right_top)
    pygame.draw.ellipse(core._screen, color, rect, width)
    if core._auto_flip:
        pygame.display.flip()


def square(left_bottom, side=50, color=const.COLOR_YELLOW, width=0):
    """
        Нарисовать квадрат цветом color
        С левой нижней вершиной в точке left_bottom
        С длинной стороны side
        Толщиной линии width
        Если width==0 то заполнить цветом
    """
    right_top = point.Point(left_bottom.x + side, left_bottom.y + side)
    rectangle(left_bottom, right_top, color, width)


def rectangle(left_bottom, right_top, color=const.COLOR_YELLOW, width=0):
    """
        Нарисовать прямоугольник цветом color
        С левой нижней вершиной в точке left_bottom
        С правой верхней вершиной в точке right_top
        Толщиной линии width
        Если width==0 то заполнить цветом
    """
    if not utils._is_all_points([left_bottom, right_top]):
        print("'left_bottom' and 'right_top' params must be point (x,y,)")
        return
    core._init()
    if left_bottom.x > right_top.x or left_bottom.y > right_top.y:
        color = utils.invert_color(color)
    rect = core._to_screen_rect(left_bottom, right_top)
    pygame.draw.rect(core._screen, color, rect, width)
    if core._auto_flip:
        pygame.display.flip()


def polygon(point_list, color=const.COLOR_YELLOW, width=1):
    """
        Нарисовать прямоугольник цветом color
        Координаты вершин передаются в списке point_list
        Толщиной линии width.
        Если width==0 то заполнить цветом
    """
    if not utils._is_all_points(point_list):
        print("'point_list' param must contain only points (x,y,)")
        return
    core._init()
    converted_point_list = [pos.to_screen() for pos in point_list]
    pygame.draw.polygon(core._screen, color, converted_point_list, width)
    if core._auto_flip:
        pygame.display.flip()


def snowflake(center, length=100, color=const.COLOR_WHITE, factor_a=0.6, factor_b=0.35, factor_c=60):
    """
        нарисовать снежинку в точке center с длинной лучей length цветом color
        factor_a - место ответвления лучиков
        factor_b - длина лучиков
        factor_c - угол отклонения лучиков
    """
    assert 0 < factor_a <= 1
    assert 0 < factor_a <= 1
    assert 0 < factor_c < 180
    if core._auto_flip:
        core._auto_flip = False
        restore_auto_flip = True
    else:
        restore_auto_flip = False
    for angle in range(0, 361, 60):
        arm = vector.Vector(center, angle, length)
        arm.draw(color)
        arm.multiply(factor_a)
        left_sub_arm = vector.Vector(arm.end_point, angle + factor_c, length * factor_b)
        left_sub_arm.draw(color)
        right_sub_arm = vector.Vector(arm.end_point, angle - factor_c, length * factor_b)
        right_sub_arm.draw(color)
    if restore_auto_flip:
        pygame.display.flip()
        core._auto_flip = True