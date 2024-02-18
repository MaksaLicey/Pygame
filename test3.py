import pygame.transform

from special import *


class StartMenu:
    def __init__(self):
        self.index = 1
        self.resolution = [(1536, 800), (960, 500), (394, 200), (192, 100), (96, 50)]
        self.size_menu = None
        self.image_for_menu = None
        self.screen = None
        self.running = True
        self.sprite_play_btn = MenySpriteCreate(self.screen, 320, 30, "btn_GamePlay.png", True, 'open_start_menu')
        self.sprite_play_btn2 = MenySpriteCreate(self.screen, 320, 200, "btn_GamePlay.png", True, 'open_start_menu')
        self.sls = [self.sprite_play_btn, self.sprite_play_btn2]
        self.group_1 = pygame.sprite.Group()
        pygame.init()
        self.dictionary = {
            "open_start_menu": self.open_start_menu
        }
        self.create_window()
        self.main_render()

    def open_start_menu(self):
        if self.index == len(self.resolution) - 1:
            self.index = 0
        else:
            self.index += 1
        self.screen = pygame.display.set_mode(self.resolution[self.index])
        for sprit_ in self.sls:
            sprit_.rect.x = sprit_.rect_x_start * self.resolution[self.index][0] // 900
            sprit_.rect.y = sprit_.rect_y_start * self.resolution[self.index][0] // 900
            sprit_.rect[2] = sprit_.image_copy.get_size()[0] * self.resolution[self.index][0] // 900
            sprit_.rect[3] = sprit_.image_copy.get_size()[1] * self.resolution[self.index][0] // 900
            sprit_.image = pygame.transform.scale(sprit_.image_copy, (
                sprit_.image_copy.get_size()[0] * self.resolution[self.index][0] // 900,
                sprit_.image_copy.get_size()[1] * self.resolution[self.index][0] // 900
            ))
        # print(self.resolution[self.index])
        # print(self.sprite_play_btn.rect)

    def create_window(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200, 50)  # задание стартового положения окна
        pygame.init()
        # pygame.mixer.init()
        # pygame.mixer.music.play()
        # pygame.mixer.music.set_volume(0.1)

        self.size_menu = 960, 500  # размер окна меню
        self.screen = pygame.display.set_mode(self.size_menu)
        self.image_for_menu = load_image("test1.png")  # фон для меню
        image_for_icon = load_image("icon_for_game.png")  # изображение для иконки приложения
        pygame.display.set_icon(image_for_icon)
        pygame.display.set_caption('The final strike')  # название приложения

    def main_render(self):
        clock = pygame.time.Clock()
        while self.running:  # основной цикл игры
            clock.tick(60)
            events = pygame.event.get()
            pygame.draw.rect(self.screen, (0, 0, 0),
                             (0, 0, self.size_menu[0], self.size_menu[1]))  # (временно) заполнение экрана черным фоном
            for EVENT in events:
                if EVENT.type == pygame.QUIT:
                    self.running = False
                if EVENT.type == pygame.MOUSEBUTTONUP:
                    for i in self.sls:
                        if i.visible and i.rect.collidepoint(pygame.mouse.get_pos()):
                            m = self.dictionary[i.function]
                            m()
            for i in self.sls:
                if i.visible:
                    self.group_1.add(i)
                elif not i.visible and i in self.group_1:
                    self.group_1.remove(i)
            self.group_1.draw(self.screen)
            pygame.display.update()


m = StartMenu()
