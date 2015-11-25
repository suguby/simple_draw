#!/usr/bin/env python
# -*- coding: utf-8 -*-

from simple_draw import Point, polygon, lines, COLOR_DARK_ORANGE, line, square, rectangle, COLOR_DARK_GREEN, sleep, \
    clear_screen, vector, COLOR_PURPLE, random_point, random_color, random_number, circle, ellipse, Vector, COLOR_GREEN, \
    COLOR_ORANGE, snowflake, get_mouse_state, user_want_exit, end


def main():
    points = [Point(x=230, y=450), Point(x=240, y=460), Point(x=230, y=470), Point(x=240, y=480)]
    polygon(point_list=points)
    points2 = [Point(p.x + 20, p.y + 20) for p in points]
    lines(point_list=points2, color=COLOR_DARK_ORANGE)
    line(start_point=Point(x=20, y=20), end_point=Point(x=40, y=300))
    square(left_bottom=Point(400, 300, ), side=100)
    rectangle(
        left_bottom=Point(x=200, y=200),
        right_top=Point(x=300, y=300),
        color=COLOR_DARK_GREEN
    )
    rectangle(
        left_bottom=Point(x=400, y=300),
        right_top=Point(x=300, y=400),
        color=COLOR_DARK_GREEN
    )
    sleep(2)
    clear_screen()
    vector(start=Point(x=230, y=260), angle=70, length=200, color=COLOR_PURPLE)
    for i in range(10):
        point = random_point()
        color = random_color()
        radius = random_number(20, 60)
        circle(center_position=point, radius=radius, color=color, width=0)
    sleep(2)
    clear_screen()
    for i in range(10):
        point = random_point()
        color = random_color()
        dx = random_number(30, 100)
        dy = random_number(30, 100)
        right_top = Point(x=point.x + dx, y=point.y + dy)
        ellipse(left_bottom=point, right_top=right_top, color=color)
    v3 = Vector(start_point=Point(0, 0), direction=45, length=50)
    for direction in range(0, 181, 20):
        v = Vector(start_point=Point(x=300, y=300), direction=direction, length=100)
        v.draw()
        v2 = Vector(start_point=v.end_point, direction=direction + 30, length=50)
        v2.draw(color=COLOR_GREEN)
        v2.add(v3)
        v2.draw(color=COLOR_ORANGE)
    snowflake(center=Point(), length=60, factor_b=0.2, factor_c=100)
    sleep(2)
    while True:
        y = 500
        for i in range(10):
            clear_screen()
            y -= 30
            for x in [100, 200, 300, 400, 500]:
                radius = random_number(30, 50)
                point = Point(x=x, y=y)
                snowflake(center=point, length=radius)
                mouse_point, mouse_buttons = get_mouse_state()
                print("mouse_state is {} + {}".format(mouse_point, mouse_buttons))
            if user_want_exit(sleep_time=0.1):
                break
        if user_want_exit(0):
            break
    end()


if __name__ == '__main__':
    main()
