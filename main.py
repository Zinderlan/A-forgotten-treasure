#подключние библиотек
import pygame
import random
import classes


#инициализация pygame
pygame.init()

#создаем экран, название игры и счетчик частоты кадров
win = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Затерянные сокровища")

# Используется для управления скоростью обновления экрана
clock = pygame.time.Clock()

player = pygame.image.load('images/pirats.png')
background = pygame.image.load("images/fon_main_menu.png")
WIDTH = 800
HEIGHT = 600

# Создаем игрока
player = classes.Player()

# Создаем все уровни
level_list = []
level_list.append(classes.Level_01(player))

# Устанавливаем текущий уровень
current_level_no = 0
сurrent_level = level_list[current_level_no]

active_sprite_list = pygame.sprite.Group()
player.level = сurrent_level

player.rect.x = 340
player.rect.y = HEIGHT - player.rect.height
active_sprite_list.add(player)

x = 50
y = 50
speed = 5

#константы-цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)

player.flip()
run = True
while (run):
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key==pygame.K_a:
                player.go_left()
            if event.key == pygame.K_RIGHT or event.key==pygame.K_d:
                player.go_right()
            if event.key == pygame.K_UP or event.key==pygame.K_w or event.key==pygame.K_SPACE:
                player.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.x_speed < 0:
                player.stop()
            if event.key == pygame.K_RIGHT and player.x_speed > 0:
                player.stop()

    active_sprite_list.update()

    сurrent_level.update()

    if player.rect.right > WIDTH:
        player.rect.right = WIDTH
    if player.rect.left < 0:
        player.rect.left = 0
    сurrent_level.draw(win)
    active_sprite_list.draw(win)
    pygame.display.flip()

pygame.quit()
