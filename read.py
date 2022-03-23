# coding=utf-8
import pygame               # отрисовка граф. интерфейса
import math                 # исполнение мат. функций
import RPi.GPIO as GPIO     # управление портами GPIO
import time                 # системные прерывания
import serial               # подключение UART
import os


running = 1                 # маркер положения НВО
angle = math.pi/2           # угол поворота сектора поиска
width = 105*math.pi/360     # ширина сектора поиска
marker = 1.65               # положение маркера
angle_prev = 1              # синх. угол поворота сектора поиска
width_prev = 1              # синх.ширина сектора поиска
marker_prev = 1             # синх. положение маркера
running_prev = 1            # синх. маркер положения НВО
north_angle = (math.pi+math.pi/6)   #положение отметки север
FPS=60                      # кол-во кадров в секунду
r_value=0                   # переменная для получения значения по UART
pwr_pin = 7



##########################     настройка дисплея ###############################
#screen_size = (1280, 1024)
#screen_center = (int(screen_size[0]/2+120), int(screen_size[1]/2)+20)
#screen_radius = (min(screen_center)-50)

screen_size = (1024, 768)                                                           # разрешение экрана
screen_center = (int(screen_size[0]/2+110), int(screen_size[1]/2)+10)               # центр экрана
screen_radius = (min(screen_center)-20)                                             # радиус радара

BACK_COL = (0, 138, 41)                     # цвет фона
LINES_COL = (255, 255, 255)                 # цвет линии

############   �##########################
def init():
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pwr_pin, GPIO.IN)
    GPIO.add_event_detect(pwr_pin, GPIO.RISING, callback=turning_off)
    return
############   ###########################

##########  ##############
def turning_off(pwr_pin):
        print 'System shuts down'
        GPIO.cleanup()
        #os.system("sudo reboot")
        os.system("sudo shutdown -h now")
        sleep(1)
############   #################
init()

pygame.init()                               # подклюение системы отрисовки


screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)          # указание дисплея
clock = pygame.time.Clock()                                               # метод clock для частоты экрана
pygame.mouse.set_visible(False)                                           # отключение курсора

x_pos_north = screen_radius*math.cos(north_angle)                         # x положения севера
y_pos_north = screen_radius*math.sin(north_angle)                         # y положения севера


#################   serial is defined here   ######################################
ser = serial.Serial(
        port='/dev/ttyAMA0',                #указание порта

        baudrate = 38400,                   # скорость обмена данными
        parity=serial.PARITY_NONE,          # равенство порта
        stopbits=serial.STOPBITS_ONE,       # размерность байта
        bytesize=serial.EIGHTBITS,          # число бит информации
        timeout=0.1                         # задержка в чтении порта
)


#######################################################
###########     основной цикл        ##################
#######################################################

while True:
# ???    sleep(0.06)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       #закрытие окна
            raise SystemExit

######   получение данных UART  ########

    got_str = ser.readline()  #получение отправленных данных

    splitting = got_str.split() #разделяем полученную строку
    res = []  # список для числа
    word = [] # список для слова

######   вычисляем опред. слово и числ. значение
    for r_value in splitting:
           try:
                   res.append(float(r_value))
           except ValueError:
                   continue
    [float(r_value) for r_value in res]
    value = (r_value / 100) # получили число

    for x in range(len(splitting)):
         if splitting[x].isalpha():
                word = splitting[x] # получили слово


    if (word == 'a'): #опрделяем угол поворота сектора
        angle = value
    if (word == 'm'): #определяем положение маркера
        marker = value


###############  расчет координат элементов   ###################


    x_pos_left = screen_radius*math.cos(angle+width-(math.pi/2)) # х левого отрезка
    y_pos_left = screen_radius*math.sin(angle+width-(math.pi/2)) # у левого отрезка

    x_pos_right = screen_radius*math.cos(angle-width-(math.pi/2)) # х правого отрезка
    y_pos_right = screen_radius*math.sin(angle-width-(math.pi/2)) # у правого отрезка

    x_pos_add = screen_radius*math.cos(marker-(math.pi/2)) # x маркера
    y_pos_add = screen_radius*math.sin(marker-(math.pi/2)) # y маркера

    x_pos_running = screen_radius*math.cos(running)         # х маркер вращения НВО
    y_pos_running = screen_radius*math.sin(running)         # у маркер вращения НВО

################   отрисовка геометрии   #################################

    #screen.fill(BACK_COL)           #снять коммент., если нужна заливка всего экрана

    # фон радара
    bkgnd = pygame.draw.circle(screen, (BACK_COL), (screen_center), screen_radius, 0)

    # край радара
    pygame.draw.circle(screen, (LINES_COL), (screen_center), screen_radius, 2)

    # отметка север
    pygame.draw.line(screen, (LINES_COL), (screen_center[0]+x_pos_north/1.15, screen_center[1]+y_pos_north/1.15), (screen_center[0]+x_pos_north, screen_center[1]+y_pos_north), 4)

    # левая линия сектора
    pygame.draw.line(screen, (LINES_COL), (screen_center[0], screen_center[1]), (screen_center[0]+x_pos_left, screen_center[1]+y_pos_left), 2)

    # правая линия сектора
    pygame.draw.line(screen, (LINES_COL), (screen_center[0], screen_center[1]), (screen_center[0]+x_pos_right, screen_center[1]+y_pos_right), 2)

    # маркер
    pygame.draw.line(screen, (LINES_COL), (screen_center[0]+x_pos_add/1.25, screen_center[1]+y_pos_add/1.25), (screen_center[0]+x_pos_add, screen_center[1]+y_pos_add), 4)

    # маркер положения НВО
    runner = pygame.draw.line(screen, (LINES_COL), (screen_center[0]+x_pos_running/1.15, screen_center[1]+y_pos_running/1.15), (screen_center[0]+x_pos_running, screen_center[1]+y_pos_running), 12)
    running = running + math.pi/16
    if (running >= 2*math.pi):          # ограничение значения маркера положение НВО
        running = 0

############        сихронизация положений элементов      #################
    if running != running_prev:
         pygame.display.update(bkgnd)
         pygame.display.update(runner)
    if angle != angle_prev or width != width_prev or marker != marker_prev:
         pygame.display.update()
         angle_prev = angle
         width_prev = width
         marker_prev = marker   #lul

