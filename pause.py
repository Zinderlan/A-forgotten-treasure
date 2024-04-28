import pygame
import main
import sys
import main_menu

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
            #button_click_sound.play()
#button_click_sound = pygame.mixer.Sound("button_click.wav")

pygame.init()
def pause():
    WIDTH = 800
    HEIGHT = 600
    main.background=pygame.image.load("images/fon_pause_game.png")
    back_button_image = pygame.image.load("images/but_back.png")
    exit_button_image = pygame.image.load("images/but_exit.png")
    settings_icon_image = pygame.image.load("images/settings.png")
    music_icon_image = pygame.image.load("images/music_on.png")
    music_icon_image_muted = pygame.image.load("images/music_off.png")
    pause_background_image = pygame.image.load("images/but_pause.png")

    main.player.x_speed = 0
    main.player.y_speed = 0


    # Создать кнопки
    back_button = Button(WIDTH // 2 - back_button_image.get_width() // 2,
                         HEIGHT // 2 - back_button_image.get_height() // 2, back_button_image, 1)
    pause_button=Button(WIDTH // 2 - pause_background_image.get_width() // 2, HEIGHT // 2 - pause_background_image.get_height() //2, pause_background_image, 1)
    exit_button = Button(WIDTH // 2 - exit_button_image.get_width() // 2,
                         HEIGHT // 2 + exit_button_image.get_height() // 2, exit_button_image, 1)
    settings_icon = Button(WIDTH - settings_icon_image.get_width() - 10, 10, settings_icon_image, 0.5)
    music_icon = Button(WIDTH - music_icon_image.get_width() - 10, HEIGHT - music_icon_image.get_height() - 10,
                        music_icon_image, 0.5)

    # Переменная для отслеживания состояния музыки
    music_on = True
    # Переменная для отслеживания состояния паузы
    paused = False

    run = True
    while run:
        main.player.x_speed = 0
        main.player.y_speed = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                back_button.check_click(mouse_pos)
                exit_button.check_click(mouse_pos)
                settings_icon.check_click(mouse_pos)
                music_icon.check_click(mouse_pos)
        if not paused: break
        main.win.blit(main.background, (0, 0))
        back_button.draw(main.win)
        exit_button.draw(main.win)
        pause_button.draw(main.win)
        settings_icon.draw(main.win)
        if music_on:
            music_icon.image = music_icon_image
        else:
            music_icon.image = music_icon_image_muted
        music_icon.draw(main.win)
        if back_button.clicked:
            # Вернуться к игре
            run = False
        if exit_button.clicked:
            main_menu.main()
        if music_icon.clicked:
            # Переключить состояние музыки
            music_on = not music_on
        pygame.display.update()
    win = pygame.display.set_mode((800, 600))


