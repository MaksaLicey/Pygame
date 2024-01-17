import pygame
import os
import sys
from os import walk


# вспомогательный файл с функциями и классами

class SpriteCreate(pygame.sprite.Sprite):  # класс для создания спрайтов меню
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
        self.prompt = promt  # название файла из data, который должен высветиться при наведении
        #  курсором на спрайт, если подсказка не нужна передать ''


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


class SpritesCreateForMap(pygame.sprite.Sprite):  # создание спрайтов карты
    def __init__(self, rect_x, rect_y, file_name):
        super().__init__()
        self.image_start = load_image(file_name)
        self.image = change_color(self.image_start, (255, 0, 255))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = rect_x
        self.rect.y = rect_y


start_file = 0  # переменные для указания границ среза списка файлов из save
max_file_show = 7  # максимум позиций в списке файлов
end_file = max_file_show  # необходимо, чтоб лист отображения файлов не вылез за меню


def get_files_list(app=0):
    global end_file
    global start_file
    global max_file_show
    show_list = []
    # print(start_file, end_file)
    for (dirpath, dirnames, filenames) in walk("saves"):
        show_list.extend(filenames)
        break
    full_list = show_list
    if ((start_file > 0 or app > 0) and (start_file < end_file or app < 0) and
            (end_file > max_file_show or app > 0) and (end_file < len(show_list) or app < 0)):
        start_file += app
        end_file += app
    if len(show_list) >= max_file_show:
        return show_list[start_file:end_file], full_list
    else:
        return show_list, full_list


def change_color(image, color):
    coloured_image = pygame.Surface(image.get_size())
    coloured_image.fill(color)

    final_image = image.copy()
    final_image.blit(coloured_image, (0, 0), special_flags=pygame.BLEND_MULT)
    return final_image


def file_reader(file_name):
    print(file_name)
