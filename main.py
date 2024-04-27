#подключние библиотек
import pygame
import random
import classe

class Player(pygame.sprite.Sprite):
    # При запуске игрок смотрит вправо, поэтому эта переменная True
    right = True

    def __init__(self):
        super().__init__()

        # создание изображения и хитбокса для спрайта
        self.image = pygame.image.load('images/pirats.png')

        self.rect = self.image.get_rect()

        self.x_speed = 0
        self.y_speed = 0

    def update(self):
        self.calc_gravity()

        self.rect.x += self.x_speed

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)

        for block in block_hit_list:
            # Если мы идем направо, устанавливает нашу правую сторону на левой стороне предмета, которого мы ударили
            if self.x_speed > 0:
                self.rect.right = block.rect.left
            elif self.x_speed < 0:
                # Если мы движемся влево, то делаем наоборот
                self.rect.left = block.rect.right

        self.rect.y += self.y_speed

        # То же самое, вот только уже для вверх/вниз
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)

        for block in block_hit_list:
            # Устанавливаем нашу позицию на основе верхней / нижней части объекта, на который мы попали
            if self.y_speed > 0:
                self.rect.bottom = block.rect.top
            elif self.y_speed < 0:
                self.rect.top = block.rect.bottom

            # Останавливаем вертикальное движение
            self.y_speed = 0

    def calc_gravity(self):
        if self.y_speed == 0:
            self.y_speed = 1
        else:
            self.y_speed += .95
        if self.rect.y >= HEIGHT - self.rect.height and self.y_speed >= 0:
            self.y_speed = 0
            self.rect.y = HEIGHT - self.rect.height

    def jump(self):
        self.rect.y += 10
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 10

        if len(platform_hit_list) > 0 or self.rect.bottom >= HEIGHT:
            self.y_speed = -16

    # Передвижение игрока
    def go_left(self):
        self.x_speed = -9
        if (self.right):  # Проверяем куда он смотрит и если что, то переворачиваем его
            self.flip()
            self.right = False

    def go_right(self):
        # то же самое, но вправо
        self.x_speed = 9
        if (not self.right):
            self.flip()
            self.right = True

    def stop(self):
        # вызываем этот метод, когда не нажимаем на клавиши
        self.x_speed = 0

    def flip(self):
        # переворот игрока (зеркальное отражение)
        self.image = pygame.transform.flip(self.image, True, False)


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.image.load('images/middle_platform.png')
        self.rect = self.image.get_rect()


class Level(object):
    def __init__(self, player):
        # Создаем группу спрайтов куда поместятся различные плтаформы
        self.platform_list = pygame.sprite.Group()
        # Ссылка на основного игрока и сундук
        self.player = player

    # Функция для обновления
    def update(self):
        win.fill(WHITE)
        self.platform_list.update()

    #
    def draw(self, screen):
        # Отрисовка заднего фона
        screen.blit(background, (0, 0))
        # отрисовка всех спрайтов из группы
        self.platform_list.draw(screen)


class Level_01(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        level = [
            [42, 16, 500, 500],
            [42, 16, 200, 400],
            [42, 16, 600, 300]]
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/sunduck.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Проверить, соприкоснулся ли сундук с игроком
        if pygame.sprite.collide_rect(self, player):
            # Вывести сообщение "YOU WIN"
            print("YOU WIN")

#инициализация pygame
pygame.init()

#создаем экран, название игры и счетчик частоты кадров
win = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Затерянные сокровища")

# Используется для управления скоростью обновления экрана
clock = pygame.time.Clock()

background = pygame.image.load("images/fon_game.png")
WIDTH = 800
HEIGHT = 600

# Создаем игрока
player = Player()
chest=Chest(520, 520)

# Создаем все уровни
level_list = []
level_list.append(Level_01(player))

# Устанавливаем текущий уровень
current_level_no = 0
сurrent_level = level_list[current_level_no]

active_sprite_list = pygame.sprite.Group()
player.level = сurrent_level

player.rect.x = 340
player.rect.y = HEIGHT - player.rect.height
active_sprite_list.add(player)
active_sprite_list.add(chest)

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
    chest.update()

    if player.rect.right > WIDTH:
        player.rect.right = WIDTH
    if player.rect.left < 0:
        player.rect.left = 0
    сurrent_level.draw(win)
    active_sprite_list.draw(win)

    pygame.display.flip()

pygame.quit()
