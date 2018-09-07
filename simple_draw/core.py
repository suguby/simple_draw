# -*- coding: utf-8 -*-
import time

import pygame
from pygame import locals as pgl

from .point import Point
from . import constants

_is_inited = False
_screen = None
_background = None
_exit_performed = False
_auto_flip = True


def _init():
    """
        Инициализация экрана для рисования
    """
    global _screen, _background, _is_inited
    if not _is_inited:
        pygame.init()
        screen_rectangle = pgl.Rect((0, 0), constants.resolution)
        _screen = pygame.display.set_mode(screen_rectangle.size)
        pygame.display.set_caption(constants.caption)
        _background = pygame.Surface(_screen.get_size())  # и ее размер
        _background = _background.convert()
        _background.fill(constants.background_color)  # заполняем цветом
        _screen.blit(_background, (0, 0))
        pygame.display.flip()
        _is_inited = True


def _to_screen(x, y):
    """
        Преобразовать координаты к экранным
    """
    return int(x), constants.resolution[1] - int(y)


def _to_screen_rect(left_bottom, right_top):
    """
        Получить прямоуголник в экранных координатах, готовый к отрисовке
    """
    width_height = (right_top.x - left_bottom.x, right_top.y - left_bottom.y)
    return pgl.Rect((left_bottom.x, constants.resolution[1] - right_top.y), width_height)


def set_screen_size(width=600, height=600):
    constants.resolution = (width, height)


def user_want_exit(sleep_time=0):
    """
        проверка ввода от пользователя
    """
    global _exit_performed
    if _exit_performed:
        return True
    if sleep_time:
        sleep(sleep_time)
    try:
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


def start_drawing():
    """
        Начать рисование на экране без автоматического отображения
    """
    global _auto_flip
    _auto_flip = False


def finish_drawing():
    """
        Закончить рисование на экране и отобразить нарисованное
    """
    global _auto_flip
    _auto_flip = True
    pygame.display.flip()


def sleep(seconds=0):
    """
        Замереть на N секунд
    """
    time.sleep(seconds)


def clear_screen():
    """
        очистить экран
    """
    if _background:
        _background.fill(constants.background_color)  # заполняем цветом
        _screen.blit(_background, (0, 0))
        pygame.display.flip()


def get_mouse_state():
    """
        получить состояние мыши - координаты и нажатую кнопку
    """
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    mouse_pos_x, mouse_pos_y = _to_screen(x=mouse_pos_x, y=mouse_pos_y)
    mouse_pos = Point(x=mouse_pos_x, y=mouse_pos_y)
    # точка на экране, где находится мышь

    mouse_buttons = pygame.mouse.get_pressed()
    # кортеж вида (1,0,0) где числа значат: (левая кнопка нажата, средня кнопка нажата, правая кнопка нажата)

    return mouse_pos, mouse_buttons