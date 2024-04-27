#подключние бибилиотек
import pygame
import random

#инициализация Pygame
pygame.init()

# Класс для игрока
class Player(pygame.sprite.Sprite):
    # При запуске игрок смотрит вправо, поэтому эта переменная True
    right = True

    def __init__(self):
        super().__init__()

        # создание изображения и хитбокса для спрайта
        self.image = pygame.image.load('pirats.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x_speed=0
        self.y_speed=0

    def update(self):
        self.calc_gravity()

        self.rect.x += self.x_speed

        self.rect.y += self.y_speed

    def calc_gravity(self):
        if self.y_speed==0:
            self.y_speed=1
        else:
            self.y_speed+= .95
        if self.rect.y >= HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = HEIGHT - self.rect.height

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


#создаем экран и счетчик частоты кадров
win = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Затерянные сокровища")
clock = pygame.time.Clock()
player=pygame.image.load("pirats.png")
background=pygame.image.load("fon_main_menu.png")
WIDTH = 800
HEIGHT = 600

Plat=pygame.Surface((50, 20))

x=50
y=50
speed=5

#константы-цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)


run=True
while(run):
    clock.tick(30)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False

    keys = pygame.key.get_pressed()
    win.fill(WHITE)
    win.blit(background, (0, 0))
    win.blit(player, (x, y))
    win.blit(Plat, (120, 530))

    if keys[pygame.K_LEFT]:
        x-=speed
    elif keys[pygame.K_RIGHT]:
        x+=speed
    elif keys[pygame.K_UP]:
        y-=speed
    elif keys[pygame.K_DOWN]:
        y+=speed
    pygame.display.update()

pygame.quit()



"""
class Player(pygame.sprite.Sprite):

        #переменная-флаг для отслеживания в прыжке ли спрайт
        self.on_ground = False
"""