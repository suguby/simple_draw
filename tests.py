import os
import shutil

import simple_draw as sd

# TAKE_SNAPSHOTS = False
TAKE_SNAPSHOTS = True
SNAPSHOTS_PATH = 'tmp'


def zero_screen():
    """test pygame init without any figures"""
    sd.start_drawing()
    sd.finish_drawing()


def first_screen():
    points = [
        sd.Point(x=230, y=450),
        sd.Point(x=240, y=460),
        sd.Point(x=230, y=470),
        sd.Point(x=240, y=480),
    ]
    sd.polygon(point_list=points)
    points2 = [sd.Point(p.x + 20, p.y + 20) for p in points]
    sd.lines(point_list=points2, color=sd.COLOR_DARK_ORANGE, width=2)
    sd.line(start_point=sd.Point(x=20, y=20), end_point=sd.Point(x=40, y=300), width=2)
    sd.square(left_bottom=sd.Point(400, 300, ), side=100, width=2)
    sd.rectangle(
        left_bottom=sd.Point(x=200, y=200),
        right_top=sd.Point(x=300, y=300),
        color=sd.COLOR_DARK_GREEN,
        width=2,
    )
    sd.rectangle(
        left_bottom=sd.Point(x=400, y=300),
        right_top=sd.Point(x=300, y=400),
        color=sd.COLOR_DARK_GREEN,
        width=2,
    )
    if TAKE_SNAPSHOTS:
        sd.take_snapshot(path=SNAPSHOTS_PATH)


def second_screen():
    sd.start_drawing()
    sd.vector(start=sd.Point(x=230, y=260), angle=70, length=200, color=sd.COLOR_PURPLE, width=2)
    for i in range(10):
        point = sd.random_point()
        color = sd.random_color()
        radius = sd.random_number(20, 60)
        sd.circle(center_position=point, radius=radius, color=color, width=0)
    sd.finish_drawing()
    if TAKE_SNAPSHOTS:
        sd.take_snapshot(file_name='second_screen.png', path=SNAPSHOTS_PATH)


def third_screen():
    for i in range(10):
        point = sd.random_point()
        color = sd.random_color()
        dx = sd.random_number(30, 100)
        dy = sd.random_number(30, 100)
        right_top = sd.Point(x=point.x + dx, y=point.y + dy)
        sd.ellipse(left_bottom=point, right_top=right_top, color=color)
    v3 = sd.Vector(start_point=sd.Point(0, 0), direction=90, length=50)
    for direction in range(0, 181, 20):
        v = sd.Vector(start_point=sd.Point(x=300, y=300), direction=direction, length=100)
        v.draw(width=3)
        v2 = sd.Vector(start_point=v.end_point, direction=direction + 30, length=50)
        v2.draw(color=sd.COLOR_GREEN, width=2)
        v2.add(v3)
        v2.draw(color=sd.COLOR_ORANGE)
    sd.snowflake(center=sd.Point(), length=60, factor_b=0.2, factor_c=100)
    if TAKE_SNAPSHOTS:
        sd.take_snapshot(path=SNAPSHOTS_PATH)


def snowfall():
    for k in range(2):
        y = 500
        for i in range(10):
            sd.clear_screen()
            y -= 30
            for x in [100, 200, 300, 400, 500]:
                radius = sd.random_number(30, 50)
                point = sd.Point(x=x, y=y)
                sd.snowflake(center=point, length=radius)
                mouse_point, mouse_buttons = sd.get_mouse_state()
                print("mouse_state is {} + {}".format(mouse_point, mouse_buttons))
            if sd.user_want_exit(sleep_time=0.1):
                break
        if sd.user_want_exit(0):
            break


class Snowflake:

    def __init__(self, x=None, y=None, length=None):
        self.x = sd.random_number(0, sd.resolution[0]) if x is None else x
        self.y = sd.random_number(300, sd.resolution[1]) if y is None else y
        self.length = sd.random_number(10, 30) if length is None else length
        self.delta_y = sd.random_number(10, 20)

    def draw(self, color):
        if self.y > self.length:
            sd.snowflake(center=sd.Point(self.x, self.y), length=self.length, color=color)

    def move(self):
        if self.y > self.length:
            self.y -= self.delta_y
            if self.y <= self.length:
                return True
            self.x += sd.random_number(-10, +10)
        return False


def massive_snowfall():
    flakes = [Snowflake() for _ in range(100)]

    while True:
        sd.start_drawing()
        for flake in flakes:
            flake.draw(color=sd.background_color)
        fallen_count = 0
        for flake in flakes:
            if flake.move():
                fallen_count += 1
        for flake in flakes:
            flake.draw(color=sd.COLOR_WHITE)
        for _ in range(fallen_count):
            flakes.append(Snowflake())
        sd.finish_drawing()
        if TAKE_SNAPSHOTS:
            sd.take_snapshot(path=SNAPSHOTS_PATH)
        mouse_point, mouse_buttons = sd.get_mouse_state()
        print("mouse_state is {} + {}".format(mouse_point, mouse_buttons))
        if sd.user_want_exit(sleep_time=0.1):
            break


def branch(start, angle, length):
    if length < 10:
        return
    vect = sd.get_vector(start_point=start, angle=angle, length=length)
    vect.draw(width=int(length / 10))
    branch(vect.end_point, angle + sd.random_number(20, 30), length * sd.random_number(75, 85) / 100)
    branch(vect.end_point, angle - sd.random_number(20, 30), length * sd.random_number(75, 85) / 100)


def draw_fractal_tree():
    start = sd.get_point(sd.resolution[0] // 2, 0)
    branch(start, 90, 100)


def main():
    sd.set_screen_size(600, 700)
    zero_screen()
    first_screen()
    sd.sleep(2)
    sd.clear_screen()
    second_screen()
    sd.sleep(2)
    sd.clear_screen()
    third_screen()
    sd.sleep(2)
    snowfall()


if __name__ == '__main__':
    if TAKE_SNAPSHOTS:
        shutil.rmtree(SNAPSHOTS_PATH, ignore_errors=True)
        os.mkdir(SNAPSHOTS_PATH)
    main()
    draw_fractal_tree()
    sd.sleep(2)
    massive_snowfall()

