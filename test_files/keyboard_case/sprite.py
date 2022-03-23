# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
import os




WIDTH = 800
HEIGHT = 650
FPS = 30

offset = 0

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 8)
        
        
    def update(self):
        global offset
        offset += (2/(0.5*HEIGHT-0.125*HEIGHT))*(0.5*HEIGHT-self.rect.bottom)          #изменение скорости в зависимости от координаты. Начальная скорость = 2
        if offset >= 1:                                                                #занчение смещения записывается в формате float в переменную offset
            self.rect.y += round(offset)                                               #т.к. спрайт может сдвигаться только на целое значение пикселей,
            offset = 0                                                                 #смещение производится по достижении занчения offset хотя бы 1    
                                                                                        
                                                                                       


# Создаем игру и окно
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
player_img = pygame.image.load(os.path.join(img_folder, 'aim_1.png'))
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()
    
    # Рендеринг
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()