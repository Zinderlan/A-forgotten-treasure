import pygame
import main
# Класс для игрока
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
        if self.rect.y >= main.HEIGHT - self.rect.height and self.y_speed >= 0:
            self.y_speed = 0
            self.rect.y = main.HEIGHT - self.rect.height

    def jump(self):
        self.rect.y += 10
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 10

        if len(platform_hit_list) > 0 or self.rect.bottom >= main.HEIGHT:
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
        self.image = pygame.image.load('images/platforms.png')
        self.rect = self.image.get_rect()


class Level(object):
    def __init__(self, player):
        # Создаем группу спрайтов куда поместятся различные плтаформы
        self.platform_list = pygame.sprite.Group()
        # Ссылка на основного игрока и сундук
        self.player = player

    # Функция для обновления
    def update(self):
        main.win.fill(main.WHITE)
        self.platform_list.update()

    #
    def draw(self, screen):
        # Отрисовка заднего фона
        screen.blit(main.background, (0, 0))
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
        if pygame.sprite.collide_rect(self, main.player):
            # Вывести сообщение "YOU WIN"
            print("YOU WIN")