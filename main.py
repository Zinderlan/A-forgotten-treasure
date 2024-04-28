#подключние библиотек
import sys
import pygame as pygame
import main_menu
from main_menu import end
import pause

# Класс для игрока
class Player(pygame.sprite.Sprite):
    # При запуске игрок смотрит вправо, поэтому эта переменная True
    right = True

    # стандартный конструктор класса
    def __init__(self):
        super().__init__()

        # создание изображения и хитбокса для спрайта
        self.image = pygame.image.load('images/pirats.png')
        self.rect = self.image.get_rect()

        # вектор скорости игрока
        self.x_speed = 0
        self.y_speed = 0

    # в этой функции происходит передвижение игрока
    def update(self):
        # установим для него гравитацию
        self.calc_gravity()

        # Передвигаем его на право/лево
        self.rect.x += self.x_speed

        # Следим ударяем ли мы какой-то другой объект
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)

        # Перебираем все возможные объекты, с которыми могли бы столкнуться
        for block in block_hit_list:

            # Если мы идем направо, устанавливает нашу правую сторону на левой стороне предмета, которого мы ударили
            if self.x_speed > 0:
                self.rect.right = block.rect.left

            elif self.x_speed < 0:
                # Если мы движемся влево, то делаем наоборот
                self.rect.left = block.rect.right

        # Передвигаемся вверх/вниз
        self.rect.y += self.y_speed

        # То же самое, вот только уже для вверх/вниз
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)

        for block in block_hit_list:
            # Устанавливаем нашу позицию на основе верхней или нижней части объекта, на который мы попали
            if self.y_speed > 0:
                self.rect.bottom = block.rect.top
            elif self.y_speed < 0:
                self.rect.top = block.rect.bottom

            # Останавливаем вертикальное движение
            self.y_speed = 0

    def calc_gravity(self):
        # Функция для вычисления гравитации

        # Здесь мы вычисляем как быстро объект будет падать на землю под действием гравитации
        if self.y_speed == 0:
            self.y_speed = 1
        else:
            self.y_speed += .95
        # Если уже на земле, то ставим позицию Y как 0
        if self.rect.y >= HEIGHT - self.rect.height and self.y_speed >= 0:
            self.y_speed = 0
            self.rect.y = HEIGHT - self.rect.height

    # Обработка прыжка
    def jump(self):
        # Нам нужно проверять здесь, контактируем ли мы с чем-либо
        # Для этого опускаемся на 10 единиц, проверем соприкосновение и далее поднимаемся обратно
        self.rect.y += 10
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 10

        # Если все нормально прыгаем вверх
        if len(platform_hit_list) > 0 or self.rect.bottom >= HEIGHT:
            self.y_speed = -16

    # Передвижение игрока
    def go_left(self):
        # Двигаем игрока по Х
        self.x_speed = -9

        # Проверяем куда он смотрит и если что, то переворачиваем его
        if (self.right):
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
        # переворот игрока
        self.image = pygame.transform.flip(self.image, True, False)

# Класс для описания платформы
class Platform(pygame.sprite.Sprite):
    all_platforms=[""]

    # Конструктор латформ
    def __init__(self, width, height):
        super().__init__()
        # Проверяем размер платформы, находим нужное изображение и устанавливаем прямоульник
        if width==41:
            self.image = pygame.image.load('images/small_platform.png')
            self.rect = self.image.get_rect()
        elif width==80:
            self.image = pygame.image.load('images/middle_platform.png')
            self.rect = self.image.get_rect()
        else:
            self.image = pygame.image.load('images/big_platform.png')
            self.rect = self.image.get_rect()

# Класс для расстановки платформ на сцене
class Level(object):
    def __init__(self, player):
        # Создаем группу спрайтов куда поместятся различные плтаформы
        self.platform_list = pygame.sprite.Group()
        # Ссылка на основного игрока
        self.player = player

    # Функция для обновления
    def update(self):
        win.fill(WHITE)
        self.platform_list.update()

    # Метод для рисования объектов на сцене
    def draw(self, screen):
        # Отрисовка заднего фона
        screen.blit(background, (0, 0))
        # отрисовка всех спрайтов из группы
        self.platform_list.draw(screen)

# Класс, что описывает где будут находится все платформы
class Level_01(Level):
    def __init__(self, player):

        # Вызываем родительский конструктор
        Level.__init__(self, player)

        # Массив с данными про платформы
        level = [
            [306, 43, 300, 500],
            [80, 30, 140, 200],
            [41, 18, 650, 400],
            [80, 30, 360, 300],
            [41, 18, 750, 200],
            [80, 30, 450, 100],
            [41, 18, 270, 80]
        ]

        # Перебираем массив и добавляем каждую платформу в группу спрайтов - platform_list
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
            win_player()

def win_player():
    pass

def lose_player():
    pass

#проверка main_menu
main_menu.main()
if end:
    pass
else:sys.exit()

#инициализация pygame
pygame.init()

#создаем экран, название игры и счетчик частоты кадров
win = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Затерянные сокровища")

# Используется для управления скоростью обновления экрана
clock = pygame.time.Clock()

#инициализируем 2 фона и созда1м ширину и высоту
background = pygame.image.load("images/fon_game.png")
background_1=pygame.image.load("images/fon_game_over.png")
WIDTH = 800
HEIGHT = 600

# Отключаем музыку из меню и запускаем музыку для игры
pygame.mixer.music.stop()
pygame.mixer.music.load("music/sound_game.mp3")
pygame.mixer.music.play(-1, 28.0)

# Создаем игрока
player = Player()
chest=Chest(752, 166)

# Создаем все уровни
level_list = []
level_list.append(Level_01(player))

# Устанавливаем текущий уровень
current_level_no = 0
сurrent_level = level_list[current_level_no]

active_sprite_list = pygame.sprite.Group()
player.level = сurrent_level

player.rect.x = 350
player.rect.y = 490
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
            sys.exit()

        # Если нажали на стрелки клавиатуры, то двигаем объект
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
            if event.key == pygame.K_RIGHT:
                player.go_right()
            if event.key == pygame.K_UP or event.key==pygame.K_w or event.key==pygame.K_SPACE:
                player.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.x_speed < 0:
                player.stop()
            if event.key == pygame.K_RIGHT and player.x_speed > 0:
                player.stop()
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause.pause()

    # Обновляем игрока и сундук
    active_sprite_list.update()
    # Обновляем объекты на сцене
    сurrent_level.update()
    chest.update()

    # Если игрок приблизится к правой стороне, то дальше его не двигаем
    if player.rect.right > WIDTH:
        player.rect.right = WIDTH

    # Если игрок приблизится к левой стороне, то дальше его не двигаем
    if player.rect.left < 0:
        player.rect.left = 0

    # Рисуем объекты на окне
    сurrent_level.draw(win)
    active_sprite_list.draw(win)

    # Обновляем экран
    pygame.display.flip()
# Корректное закртытие программы
pygame.quit()