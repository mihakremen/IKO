from threading import Thread

import constants
import pygame
import math
import random
import os
import time

screen_size = (400, 400)
screen_center = (int(screen_size[0] / 2), int(screen_size[1] / 2))
screen_radius = (min(screen_center))
angle = 0
ma_angle = 0
width = 105 * math.pi / 360

WIDTH = screen_size[0]
HEIGHT = screen_size[1]

pusk = 0





# COMPAS
co_width = 14  #ширина линии
line_begin = (screen_center[0], 0)
line_end = (screen_center[0], screen_radius* 0.15)

BACK_COL = (0, 138, 41)
LINES_COL = (255, 255, 255)

FPS = 100

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
player_img = pygame.image.load(os.path.join(img_folder, 'aim_1_romb.png'))
meeting_place_img = pygame.image.load(os.path.join(img_folder, 'meeting_place.png'))
rocket_img = pygame.image.load(os.path.join(img_folder, 'rocket.png'))

####################################
####### реальные координты #########
####################################

real_radius = 100000 # реальный радиус обнаружения
aim_real_distance = 75000 # реальная дальность цели
aim_real_speed = 500 # реальная скорость цели
aim_azimut = 10 # азимут цели

aim_distance = (aim_real_distance / real_radius) * screen_radius
aim_x = screen_center[0] + aim_distance * math.cos(aim_azimut)
aim_y = screen_center[1] + aim_distance * math.sin(aim_azimut)
aim_speed = aim_real_speed / real_radius * screen_radius

rocket_speed = 1000 / real_radius * screen_radius


class Rocket (pygame.sprite.Sprite):
    def __init__(self, aim_real_distance, aim_azimut):
        pygame.sprite.Sprite.__init__(self)
        self.image = rocket_img
        self.image = pygame.transform.scale(self.image, (round(WIDTH / 8), round(HEIGHT / 8)))
        self.rect = self.image.get_rect()
        self.image.set_alpha(0)
        self.rect.center = ((WIDTH / 2) - 20, (HEIGHT / 2) - 20)
        self.x = (self.rect.center[0])  # добавлено
        self.y = (self.rect.center[1])  # добавлено
        self.speedx = 0
        self.speedy = 0  # добавлено

    def go(self):  # добавлено
        self.x += self.speedx  # добавлено
        self.y += self.speedy  # добавлено
        self.rect.x = float(self.x)  # добавлено
        self.rect.y = float(self.y)  # добавлено

    def set_speed(self, x, y, speed):  # добавлено
        xs = x - self.x  # добавлено
        ys = y - self.y  # добавлено
        k = speed / math.sqrt(xs * xs + ys * ys)  # добавлено
        self.speedx = xs * k  # добавлено
        self.speedy = ys * k  # добавлено

    def get_distance(self, x, y):  # добавлено
        xs = x - self.x  # добавлено
        ys = y - self.y  # добавлено
        return math.sqrt(xs * xs + ys * ys)  # добавлено


class Aim(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image = pygame.transform.scale(self.image, (int(WIDTH / 8), int(HEIGHT / 8)))
        self.rect = self.image.get_rect() #определяем
        self.rect.center = (aim_x, aim_y)  # начальные координаты
        self.x = int(self.rect.center[0])  # добавлено
        self.y = int(self.rect.center[1])  # добавлено
        self.speedx = 0
        self.speedy = 0  # добавлено

    def go(self):  # добавлено
        self.x += self.speedx  # добавлено
        self.y += self.speedy  # добавлено
        self.rect.x = int(self.x)  # добавлено
        self.rect.y = int(self.y)  # добавлено

    def set_speed(self, x, y, speed):  # добавлено
        xs = x - self.x  # добавлено
        ys = y - self.y  # добавлено
        k = speed / math.sqrt(xs * xs + ys * ys)  # добавлено
        self.speedx = xs * k  # добавлено
        self.speedy = ys * k  # добавлено

    def get_distance(self, x, y):  # добавлено
        xs = x - self.x  # добавлено
        ys = y - self.y  # добавлено
        return math.sqrt(xs * xs + ys * ys)  # добавлено


class Meeting_place(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = meeting_place_img
        self.image = pygame.transform.scale(self.image, (round(WIDTH / 6), round(HEIGHT / 6)))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.x = (self.rect.center[0])  # добавлено
        self.y = (self.rect.center[1])  # добавлено
        self.speedx = 0
        self.speedy = 0  # добавлено

    def go(self):  # добавлено
        self.x += self.speedx  # добавлено
        self.y += self.speedy  # добавлено
        self.rect.x = int(self.x)  # добавлено
        self.rect.y = int(self.y)  # добавлено

    def set_speed(self, x, y, speed):  # добавлено
        xs = x - self.x  # добавлено
        ys = y - self.y  # добавлено
        k = speed / math.sqrt(xs * xs + ys * ys)  # добавлено
        self.speedx = xs * k  # добавлено
        self.speedy = ys * k  # добавлено

    def get_distance(self, x, y):  # добавлено
        xs = x - self.x  # добавлено
        ys = y - self.y  # добавлено
        return math.sqrt(xs * xs + ys * ys)  # добавлено


pygame.init()

screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

meeting_place = Meeting_place()
# куда лететь, с какой скоростью

aim = Aim()

rocket = Rocket(aim_real_distance, aim_azimut)
# rocket.set_speed(player.rect.x, player.rect.y, 0.75)

all_sprites = pygame.sprite.Group()

all_sprites.add(meeting_place, rocket, aim)

inGame = True
while inGame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # закрытие окна
            raise SystemExit
    clock.tick(FPS)
    # обработка нажатия клавиш
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        angle += 0.01
        pygame.display.update()
    elif keys[pygame.K_LEFT]:
        angle -= 0.01
        pygame.display.update()
    elif keys[pygame.K_0]:
        width += 0.005
        pygame.display.update()
    elif keys[pygame.K_9]:
        width -= 0.005
        pygame.display.update()
    elif keys[pygame.K_4]:
        ma_angle += 0.01
        pygame.display.update()
    elif keys[pygame.K_6]:
        ma_angle -= 0.01
        pygame.display.update()
    elif keys[pygame.K_5]:
        pusk = 1
        print("key 5 pressed, pusk = ", pusk)

    #   if meeting_place.get_distance((screen_size[0] / 2), (screen_size[1] / 2)) <= 10:
    #       print('STOP')
    #   else:

    # print(rocket.rect.move())
    rocket.set_speed(aim.x, aim.y, 0)
    if pusk == 1:
        rocket.image.set_alpha(255)
        rocket.set_speed(aim.x, aim.y, rocket_speed / 120)
        rocket.go()

    aim.set_speed(screen_center[0] - 10, screen_center[1] - 10, aim_speed/120)
    aim.go()

    meeting_place.x = ((aim.x + rocket.x) / 2) - 10
    meeting_place.y = ((aim.y + rocket.y) / 2) - 10

    # meeting_place.set_speed((player.x + rocket.x) / 2, (player.y + rocket.y) / 2, 0.5)
    meeting_place.go()

    all_sprites.update()

###############################################################
#################### РАСЧЕТ КООРДИНАТ #########################
###############################################################

    #####    координаты сектора 105     ########

    x_pos_center = screen_radius * math.cos(angle)
    y_pos_center = screen_radius * math.sin(angle)

    x_pos_left = screen_radius * math.cos(angle + width)
    y_pos_left = screen_radius * math.sin(angle + width)

    x_pos_right = screen_radius * math.cos(angle - width)
    y_pos_right = screen_radius * math.sin(angle - width)

    x_pos_marker = screen_radius * math.cos(ma_angle)
    y_pos_marker = screen_radius * math.sin(ma_angle)

    # x_pos_compas = screen_radius*math.cos(co_angle)
    # y_pos_compas = screen_radius*math.sin(co_angle)





    # отрисовка геометрии

    # screen.fill(BACK_COL)           #снять коммент., если нужна заливка всего экрана
    pygame.draw.circle(screen, (BACK_COL), (screen_center), screen_radius, 0)

    pygame.draw.circle(screen, (LINES_COL), (screen_center), screen_radius, 2)

    pygame.draw.line(screen, (LINES_COL), (screen_center[0] + x_pos_center / 2, screen_center[1] + y_pos_center / 2),
                     (screen_center[0] + x_pos_center, screen_center[1] + y_pos_center), 2)  # central line
    pygame.draw.line(screen, (LINES_COL),
                     (screen_center[0] + x_pos_marker / 1.5, screen_center[1] + y_pos_marker / 1.5),
                     (screen_center[0] + x_pos_marker, screen_center[1] + y_pos_marker), 6)  # marker
    pygame.draw.line(screen, (LINES_COL), (line_begin), (line_end), co_width)  # compas
    pygame.draw.line(screen, (LINES_COL), (screen_center[0], screen_center[1]),
                     (screen_center[0] + x_pos_left, screen_center[1] + y_pos_left), 2)  # left line
    pygame.draw.line(screen, (LINES_COL), (screen_center[0], screen_center[1]),
                     (screen_center[0] + x_pos_right, screen_center[1] + y_pos_right), 2)  # right line
    # pygame.draw.line(screen, (255, 0, 0), (screen_center[0], screen_center[1]), (screen_center[0]+x_pos_right,
    # screen_center[1]+y_pos_right), 2)
    # #compas pygame.display.update()

    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран

    pygame.display.flip()
pygame.quit()
