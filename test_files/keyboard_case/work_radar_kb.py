import pygame
import math
import random
import os

screen_size = (400, 400)
screen_center = (int(screen_size[0]/2), int(screen_size[1]/2))
screen_radius = (min(screen_center))
angle = 0
ma_angle = 0
width = 105*math.pi/360

WIDTH = 400
HEIGHT = 400
offset_Player = 0
offset_Meeting = 0
offset_Rocket = 0
pusk = 0

#COMPAS
co_width = 14
line_begin = (screen_center[0], 0)
line_end = (screen_center[0], screen_radius*0.15)

BACK_COL = (0, 138, 41)
LINES_COL = (255, 255, 255)

FPS=60




class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image = pygame.transform.scale(self.image, (round(WIDTH/6), round(HEIGHT/6)))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 8)
        
        
    def update(self):
        global offset_Player
        #global offset_timer
        offset_Player += 1
        #offset += (2/(0.5*HEIGHT-0.125*HEIGHT))*(0.5*HEIGHT-self.rect.bottom)
                                                                                      #изменение скорости в зависимости от координаты. Начальная скорость = 2
    # if offset >= 1:
        if offset_Player == 120:                                                                                        # #занчение смещения записывается в формате float в переменную offset
            #self.rect.y += round(offset)                                                                 #т.к. спрайт может сдвигаться только на целое значение пикселей,
            print("offset_Player", offset_Player)
            self.rect.y += 2
            offset_Player = 0


class Meeting_place(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meeting_place_img
        self.image = pygame.transform.scale(self.image, (round(WIDTH / 6), round(HEIGHT / 6)))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 4)

    def update(self):
        global offset_Meeting
        #global offset_timer
        offset_Meeting += 1
        # offset += (2/(0.5*HEIGHT-0.125*HEIGHT))*(0.5*HEIGHT-self.rect.bottom)
          # изменение скорости в зависимости от координаты. Начальная скорость = 2
        # if offset >= 1:
        if offset_Meeting == 120:  # #занчение смещения записывается в формате float в переменную offset
            # self.rect.y += round(offset)                                                                 #т.к. спрайт может сдвигаться только на целое значение пикселей,
            print("offset_Meeting", offset_Meeting)
            self.rect.y += 1
            offset_Meeting = 0

#def pusk(rocket_img, offset_Rocket):
class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = rocket_img
        self.image = pygame.transform.scale(self.image, (round(WIDTH / 6), round(HEIGHT / 6)))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        global offset_Rocket
        global pusk

        if (pusk == 1):  # #занчение смещения записывается в формате float в переменную offset
            offset_Rocket += 1
            print("offset_Rocket", offset_Rocket)
            if offset_Rocket == 120:
                # self.rect.y += round(offset)                                                                 #т.к. спрайт может сдвигаться только на целое значение пикселей,
                print("offset_Rocket", offset_Rocket)
                self.rect.y -= 3
                offset_Rocket = 0

pygame.init()

screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
player_img = pygame.image.load(os.path.join(img_folder, 'aim_1_romb.png'))
meeting_place_img = pygame.image.load(os.path.join(img_folder, 'meeting_place.png'))
rocket_img = pygame.image.load(os.path.join(img_folder, 'rocket.png'))


all_sprites = pygame.sprite.Group()
player = Player()
meeting_place = Meeting_place()
rocket = Rocket()
all_sprites.add(player, meeting_place, rocket)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       #закрытие окна
            raise SystemExit
    clock.tick(FPS)   
    #обработка нажатия клавиш    
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

    
    all_sprites.update()

    #расчет координат
    x_pos_center = screen_radius*math.cos(angle)
    y_pos_center = screen_radius*math.sin(angle)
    
    x_pos_left = screen_radius*math.cos(angle+width)
    y_pos_left = screen_radius*math.sin(angle+width)

    x_pos_right = screen_radius*math.cos(angle-width)
    y_pos_right = screen_radius*math.sin(angle-width)

    x_pos_marker = screen_radius*math.cos(ma_angle)
    y_pos_marker = screen_radius*math.sin(ma_angle)

    #x_pos_compas = screen_radius*math.cos(co_angle)
    #y_pos_compas = screen_radius*math.sin(co_angle)

    #отрисовка геометрии

    #screen.fill(BACK_COL)           #снять коммент., если нужна заливка всего экрана
    pygame.draw.circle(screen, (BACK_COL), (screen_center), screen_radius, 0)
    
    pygame.draw.circle(screen, (LINES_COL), (screen_center), screen_radius, 2)

    pygame.draw.line(screen, (LINES_COL), (screen_center[0]+x_pos_center/2, screen_center[1]+y_pos_center/2), (screen_center[0]+x_pos_center, screen_center[1]+y_pos_center), 2)    #central line
    pygame.draw.line(screen, (LINES_COL), (screen_center[0]+x_pos_marker/1.5, screen_center[1]+y_pos_marker/1.5),(screen_center[0]+x_pos_marker, screen_center[1]+y_pos_marker), 6) #marker
    pygame.draw.line(screen, (LINES_COL), (line_begin), (line_end), co_width)                                                                        # compas
    pygame.draw.line(screen, (LINES_COL), (screen_center[0], screen_center[1]), (screen_center[0]+x_pos_left, screen_center[1]+y_pos_left), 2)                                      #left line
    pygame.draw.line(screen, (LINES_COL), (screen_center[0], screen_center[1]), (screen_center[0]+x_pos_right, screen_center[1]+y_pos_right), 2)                                    #right line
    #pygame.draw.line(screen, (255, 0, 0), (screen_center[0], screen_center[1]), (screen_center[0]+x_pos_right, screen_center[1]+y_pos_right), 2)                                    #compas
    #pygame.display.update()

    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()
