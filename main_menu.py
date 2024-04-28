import pygame
import sys

class Button:

    def __init__(self, x, y, image, scale):
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.clicked = True
            # button_click_sound.play()

def main():

    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    WIDTH = 800
    HEIGHT = 600

    end=True
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    play_button_image = pygame.image.load("images/but_play.png")
    exit_button_image = pygame.image.load("images/but_exit.png")
    settings_icon_image = pygame.image.load("images/settings.png")
    music_icon_image = pygame.image.load("images/music_on.png")
    music_icon_image_muted=pygame.image.load("images/music_off.png")

    background = pygame.image.load("images/fon_main_menu.png")

    pygame.mixer.music.load("music/main_menu.mp3")
    pygame.mixer.music.play(-1, 2.0)

    background_rect=background.get_rect(center = (WIDTH//2, HEIGHT//2))


# button_click_sound = pygame.mixer.Sound("button_click.wav")

    # Создать кнопки
    play_button = Button(WIDTH // 2 - play_button_image.get_width() // 2-125, HEIGHT // 2 - play_button_image.get_height() // 2 + 50,
                     play_button_image, 2)
    exit_button = Button(WIDTH // 2 - exit_button_image.get_width() // 2-125, HEIGHT // 2 + exit_button_image.get_height() // 2 + 100,
                     exit_button_image, 2)
    settings_icon = Button(WIDTH - settings_icon_image.get_width() - 10, 10, settings_icon_image, 1)
    music_icon = Button(WIDTH - music_icon_image.get_width() - 10, HEIGHT - music_icon_image.get_height() - 10,
                    music_icon_image, 1)
    music_icon_off=Button(WIDTH - music_icon_image.get_width() - 10, HEIGHT - music_icon_image.get_height() - 10,
                    music_icon_image, 1)

    # Переменная для отслеживания состояния музыки
    music_on = True

    # Цикл главного меню
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                end=False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                play_button.check_click(mouse_pos)
                exit_button.check_click(mouse_pos)
                settings_icon.check_click(mouse_pos)
                music_icon.check_click(mouse_pos)

        # Обновление экрана
        screen.blit(background, background_rect)

        # Отрисовка кнопок
        play_button.draw(screen)
        exit_button.draw(screen)
        settings_icon.draw(screen)
        music_icon.draw(screen)

        # Логика кнопок
        if play_button.clicked:
            # Стереть область рисования и запустить игру
            screen.fill(BLACK)
            run=False
            end=True

        if exit_button.clicked:
            sys.exit()

        if music_icon.clicked:
            # Переключить состояние музыки
            music_on = not music_on
            if music_on:
                music_icon.image = music_icon_image
            else:
                music_icon.image = music_icon_image_muted
            music_icon.draw(screen)

        if settings_icon.clicked:
            print(23)

        # Обновление экрана
        pygame.display.update()

end=True