import pygame
import os
import sys
from os import walk


class SpriteCreate(pygame.sprite.Sprite):  # класс для создания спрайтов
    def __init__(self, rect_x, rect_y, file_name, visible_s, fuction_s, promt):
        super().__init__()
        # self.image = image
        self.image = load_image(file_name)
        self.size = load_image(file_name).get_size()
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.visible = visible_s
        self.function = fuction_s
        self.prompt = promt


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


def get_files_list():
    f = []
    for (dirpath, dirnames, filenames) in walk("saves"):
        f.extend(filenames)
        break
    return f
