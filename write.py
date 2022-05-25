# coding=utf-8
import pygame             # отрисовка граф. интерфейса
import math               # исполнение мат. функций
import os
import RPi.GPIO as GPIO   # управление портами GPIO
import time               # системные прерывания
import serial             # подключение UART
import threading
from time import sleep    # для определения sleep

### test git ####

####  задаем переменные  #####

running = 1
angle = math.pi/2                 # угол поворота сектора поиска
width = 105*math.pi/360           # ширина сектора (105)
marker = 1.65                     # положение маркера
angle_prev = 1                    # синхронизация угла сектора
width_prev = 1                    # синхронизация ширины сектора
marker_prev = 1                   # синхронизация маркера
north_angle = math.pi+2*math.pi/3 # положение отметки север
FPS=400                            # частота работы программы

Rotary_counter = 0
Current_A1 = 1
Current_B1 = 1
Current_A2 = 1
Current_B2 = 1
LockRotary = threading.Lock()

####    GPIO  ######

Enc_A1 = 23 #1 нога энкодера сектора
Enc_B1 = 24 #2 нога энкодера сектора
Enc_A2 = 18 #1 нога энкодера маркера
Enc_B2 = 17 #2 нога энкодера маркера
pwr_pin = 7
############    наcтройка изображения    #######################
screen_size = (1280, 1024)                                              # разрешение экрана
screen_center = (int(screen_size[0]/2-150), int(screen_size[1]/2)+40)   # центр экрана
screen_radius = (min(screen_center)-110)                                # радиус радара

BACK_COL = (0, 138, 41)         # цвет фона радара
LINES_COL = (255, 255, 255)     # цвет линий



###########      определение  энкодеров      ###################

def init():
	GPIO.setwarnings(True)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(Enc_A1, GPIO.IN)
	GPIO.setup(Enc_B1, GPIO.IN)
	GPIO.setup(Enc_A2, GPIO.IN)
	GPIO.setup(Enc_B2, GPIO.IN)
	GPIO.setup(pwr_pin, GPIO.IN)
	GPIO.add_event_detect(Enc_A1, GPIO.RISING, callback = rotation_decode_1, bouncetime = 100) # замыкание ноги "а" 1 экнодера
	GPIO.add_event_detect(Enc_B1, GPIO.RISING, callback = rotation_decode_1, bouncetime = 100) # замыкание ноги "б" 1 экнодера
	GPIO.add_event_detect(Enc_A2, GPIO.RISING, callback=rotation_decode_2) # замыкание ноги "а" 2 экнодера
	GPIO.add_event_detect(Enc_B2, GPIO.RISING, callback=rotation_decode_2) # замыкание ноги "б" 2 экнодера
	GPIO.add_event_detect(pwr_pin, GPIO.RISING, callback=turning_off)
	print ("GPIO initialisation succellfull")
	return




#####  обработка сигналов с 1 энкодера  #####
def rotation_decode_1(A1_or_B1):
	print ("rotation_decode_1 is called")
	global angle, Rotary_counter, Current_A1, Current_B1, LockRotary
	sleep(0.002)
	Switch_A1 = GPIO.input(Enc_A1)
	Switch_B1 = GPIO.input(Enc_B1)


	if (Current_A1 == Switch_A1) and (Current_B1 == Switch_B1):		# Same interrupt as before (Bouncing)?
		print ("bouncing interrupt /n")
		return										# ignore interrupt!

	Current_A1 = Switch_A1								# remember new state
	Current_B1 = Switch_B1								# for next bouncing check


	if (Switch_A1 and Switch_B1):			# Оба замкнуты?
		print ("both legs are connected")
		LockRotary.acquire()				# блокировка
		if A1_or_B1 == Enc_B1:				# Последней была замкнута нога Б?
			print ("last connected leg is B1")
			angle += 0.03				# меняем угол поворота в большшую сторону
			angle_send = int(angle*100)		# подготовка переменной для отправки
#			ser.write(("a %d \n"%(angle_send)).encode())	# отправка переменной значения угла
#     	      	        print "angle's change -> ", angle_send
		else:					# Последней была замкнута нога А?
			print ("last connected leg is A1")
			angle -= 0.03
			angle_send = int(angle*100)
#			ser.write(("a %d \n"%(angle_send)).encode)
#                        print "angle's change -> ", angle_send
		LockRotary.release()
	return



#####     обработка сигналов со 2 энкодра   ####

def rotation_decode_2(A2_or_B2):
	global marker, Rotary_counter, Current_A2, Current_B2, LockRotary
	sleep(0.002)
	Switch_A2 = GPIO.input(Enc_A2)
	Switch_B2 = GPIO.input(Enc_B2)


	if (Current_A2 == Switch_A2) and (Current_B2 == Switch_B2):         # Same interrupt as before (Bouncing)?
		return                                                                          # ignore interrupt!

	Current_A2 = Switch_A2                                                         # remember new state
	Current_B2 = Switch_B2                                                          # for next bouncing check


	if (Switch_A2 and Switch_B2):                                           # Both one active? Yes -> end of sequence
		LockRotary.acquire()                                            # get lock
		if A2_or_B2 == Enc_B2:                                                  # Turning direction depends on
			Rotary_counter += 0.05
 #                   	marker_send = int(marker*100)
#                    	ser.write("m %d \n"%(marker_send))
#                    	print "marker pos -> ", marker_send                   # which input gave last in$
			LockRotary.release()
			sleep (0.3)
		else:                                                                           # so depending on direction either
			Rotary_counter -= 0.05
#		    	marker_send = int(marker*100)
#                   	print "marker pos <- ", marker_send
#		    	ser.write("m %d \n"%(marker_send))
			LockRotary.release()
			sleep (0.3)
	return                                                                                  # THAT'S IT

##### функция выключения raspberry с кнопки "РУ"  ########

def turning_off(pwr_pin):
	print ('System shuts down')
	GPIO.cleanup()
        #os.system("sudo reboot")
	os.system("sudo shutdown -h now")
	sleep(1)


init()

pygame.init()                                                        # подклюение системы отрисовки

screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)     # полный экран
clock = pygame.time.Clock()                                          # метод clock для частоты экрана
pygame.mouse.set_visible(False)                                      # скрыть курсор

x_pos_north = screen_radius*math.cos(north_angle) # х координата метки север
y_pos_north = screen_radius*math.sin(north_angle) # у координата метки север



######    открытие порта serial     ########

ser = serial.Serial(
	port='/dev/ttyAMA0',            # указание порта
	baudrate = 38400,               # скорость обмена данными
	parity=serial.PARITY_NONE,      # равенство порта
	stopbits=serial.STOPBITS_ONE,   # размерность байта
	bytesize=serial.EIGHTBITS,      # число бит информации
	timeout=1                       # ??? задержка в чтении порта
)

#######################################################
###########     основной цикл        ##################
#######################################################

while True:
#	sleep(0.06)
	clock.tick(FPS)
	LockRotary.acquire()                                    # get lock for rotary swit$
	NewCounter = Rotary_counter                     # get counter value
	Rotary_counter = 0                                              # RESET IT TO 0
	LockRotary.release()
	if (NewCounter !=0):
		marker = marker + NewCounter
		marker_send = ("m %d /n"%(int(marker*100)))
		ser.write ((marker_send).encode('utf-8'))
#		print ("Direction  ", NewCounter, "marker pos ", marker_send)                   # which input gave l$

	for event in pygame.event.get():
		if event.type == pygame.QUIT:       #закрытие окна
			raise SystemExit
#       	buttonIn = GPIO.input(26)
#        if buttonIn == True:
#        	print 'System shuts down'
#        	GPIO.cleanup()
        	#os.system("sudo reboot")
#        	os.system("sudo shutdown -h now")
#        	break
#        sleep(1)
    ######      расчет координат      ####

	x_pos_center = screen_radius*math.cos(angle) # х середины сектора
	y_pos_center = screen_radius*math.sin(angle) # y середины сектора

	x_pos_left = screen_radius*math.cos(angle+width) # х левого отрезка
	y_pos_left = screen_radius*math.sin(angle+width) # y левого отрезка

	x_pos_right = screen_radius*math.cos(angle-width) # х правого отрезка
	y_pos_right = screen_radius*math.sin(angle-width) # y правого отрезка

	x_pos_add = screen_radius*math.cos(marker) # х маркера
	y_pos_add = screen_radius*math.sin(marker) # y маркера

   ##########           отрисовка геометрии         #################

    #screen.fill(BACK_COL)           #снять коммент., если нужна заливка всего экрана

    # фон радара
	pygame.draw.circle(screen, (BACK_COL), (screen_center), screen_radius, 0)

    # край радара
	pygame.draw.circle(screen, (LINES_COL), (screen_center), screen_radius, 2)

    # компас
	pygame.draw.line(screen, (LINES_COL), (screen_center[0]+x_pos_north/1.15, screen_center[1]+y_pos_north/1.15), (screen_center[0]+x_pos_north, screen_center[1]+y_pos_north), 4)

    # центр. линия сектора
	pygame.draw.line(screen, (LINES_COL), (screen_center[0]+x_pos_center/2, screen_center[1]+y_pos_center/2), (screen_center[0]+x_pos_center, screen_center[1]+y_pos_center), 2)    #central line

    # левая линия сектора
	pygame.draw.line(screen, (LINES_COL), (screen_center[0], screen_center[1]), (screen_center[0]+x_pos_left, screen_center[1]+y_pos_left), 2)

    # правая линия сектора
	pygame.draw.line(screen, (LINES_COL), (screen_center[0], screen_center[1]), (screen_center[0]+x_pos_right, screen_center[1]+y_pos_right), 2)

    # маркер
	pygame.draw.line(screen, (LINES_COL), (screen_center[0]+x_pos_add/1.25, screen_center[1]+y_pos_add/1.25), (screen_center[0]+x_pos_add, screen_center[1]+y_pos_add), 4)


############        сихронизация положений элементов      #################
	if angle != angle_prev or width != width_prev or marker != marker_prev:
		pygame.display.update()
		angle_prev = angle
		width_prev = width
		marker_prev = marker
	pygame.display.flip()
pygame.quit()
