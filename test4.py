import pygame
import os
import sys
from os import walk


def load_image(name, colorkey=None):  # функция для загрузки изображений
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    # else:
    #     image = image.convert_alpha()
    return image


class MenySpriteCreate(pygame.sprite.Sprite):  # класс для создания спрайтов меню
    def __init__(self, rect_x, rect_y, file_name):
        super().__init__()
        self.image = load_image(file_name)
        self.size = load_image(file_name).get_size()
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y


def main():
    pygame.init()
    size_menu = 1100, 700  # размер меню
    screen = pygame.display.set_mode(size_menu)

    pygame.display.set_caption('The final strike')  # название приложения

    sprite = MenySpriteCreate(100, 100, "prompt_1.png")
    sls = pygame.sprite.Group()
    sls.add(sprite)
    clock = pygame.time.Clock()

    flag = False
    mouse_start = 0, 0
    # mouse_start

    global running
    while running:  # основной цикл игры
        clock.tick(60)
        events = pygame.event.get()
        for EVENT in events:
            if EVENT.type == pygame.QUIT:
                running = False
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[1]:
                    pos = pygame.mouse.get_pos()
                    if sprite.rect.collidepoint(pos):
                        flag = not flag
                        if flag:
                            mouse_start = pos[0] - sprite.rect.x, pos[1] - sprite.rect.y
            if flag:
                sprite.rect.x = pygame.mouse.get_pos()[0] - mouse_start[0]
                sprite.rect.y = pygame.mouse.get_pos()[1] - mouse_start[1]
        pygame.draw.rect(screen, (0, 0, 0),
                         (0, 0, size_menu[0], size_menu[1]))  # (временно) заполнение экрана черным фоном
        sls.draw(screen)
        pygame.display.update()


running = True
main()
