#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Библиотека для рисования графических примитивов
    v 2.4
"""

from .constants import *
from .core import (
    set_screen_size, user_want_exit, sleep, clear_screen, start_drawing, finish_drawing, get_mouse_state, pause)
from .primitives import (
    line, lines, circle, ellipse, polygon, rectangle, square, snowflake)
from .point import get_point, Point
from .vector import get_vector, vector, Vector
from .utils import random_color, random_point, random_number

