import pygame
import math

screen_size = (400, 400)
screen_center = (int(screen_size[0]/2), int(screen_size[1]/2))
screen_radius = (min(screen_center))
angle = 0
ma_angle = 0
width = 105*math.pi/360

#COMPAS
co_width = 14
line_begin = (screen_center[0], 0)
line_end = (screen_center[0], screen_radius*0.15)

BACK_COL = (0, 138, 41)
LINES_COL = (255, 255, 255)

FPS=60

pygame.init()

screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()



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

