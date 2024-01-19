import pygame
import os
import sys
from os import walk


# вспомогательный файл с функциями и классами

class SpriteCreate(pygame.sprite.Sprite):  # класс для создания спрайтов меню
    def __init__(self, rect_x, rect_y, file_name, visible_s, fuction_s='', promt=''):
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


start_file = 0  # переменные для указания границ среза списка файлов из save
max_file_show = 7  # максимум позиций в списке файлов
end_file = max_file_show  # необходимо, чтоб лист отображения файлов не вылез за меню


def get_files_list(app=0):  # функция для получения списка файлов из
    global end_file  # saves, длинной max_file_show
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


def change_color(image, color):  # функция смены цвета спрайта
    coloured_image = pygame.Surface(image.get_size())
    coloured_image.fill(color)

    final_image = image.copy()
    final_image.blit(coloured_image, (0, 0), special_flags=pygame.BLEND_MULT)
    return final_image


class Countries():
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.control_id = []


class SpritesCreateForMap(pygame.sprite.Sprite):  # создание спрайтов карты
    def __init__(self, id_province, name, rect_x, rect_y, file_name_img, holder, color):
        super().__init__()
        self.image_start = load_image(file_name_img)
        self.color = (int(color[0]), int(color[1]), int(color[2]))
        self.image = change_color(self.image_start, self.color)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.id_province = id_province
        self.name = name
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.holder = holder


def file_reader(file_name):  # чтение файла
    color = ''
    file = open(os.path.join("saves", file_name), mode="r+", encoding="utf-8")
    file_strings = file.readlines()
    sls_for_sprite_info = []  # список параметров игры
    sls_for_file_info = []  # список параметров спрайта, которые передаются в SpritesCreateForMap
    list_of_sprite = []  # список спрайтов
    list_of_holders, holder_info_list = [], []
    # print(file_strings)
    string_num = 0
    # первые строки до map(...) параметеры игры
    while file_strings[string_num].split()[0] != "holder(":
        sls_for_file_info.append(file_strings[string_num].split()[2])
        string_num += 1
    string_num += 1
    while file_strings[string_num].split()[0] != ")":
        if file_strings[string_num].split()[0] != '|' and file_strings[string_num].split()[0] != ')':
            holder_info_list.append(file_strings[string_num].split()[2])
        else:
            list_of_holders.append(Countries(holder_info_list[0], holder_info_list[1]))
            holder_info_list.clear()
        string_num += 1
    string_num += 2
    while True:
        if file_strings[string_num].split()[0] == "(":  # каждый спрайт - отдельная провинция, со своими параметрами
            # сама карта "рисуется" через файлы из папки starts_file
            # каждому спрайта указываются все необходимые данные, помещаемые в (id = 0,...)
            # id соответствует индексу спрайта в list_of_sprite
            while file_strings[string_num].split()[0] != ")":
                string_num += 1
                if file_strings[string_num].split()[0] != ")":
                    sls_for_sprite_info.append(file_strings[string_num].split()[2])  # добавления спрайта и в список
            for i in list_of_holders:  # изменение цвета в соответствии с цветом страны
                if sls_for_sprite_info[5] == i.name:
                    color = i.color.split('.')
                    i.control_id.append(sls_for_sprite_info[0])
                else:
                    if sls_for_sprite_info[0] in i.control_id:
                        i.control_id.remove(sls_for_sprite_info[0])
            list_of_sprite.append(  # добавление спрайта - провинции в список
                SpritesCreateForMap(sls_for_sprite_info[0], sls_for_sprite_info[1], int(sls_for_sprite_info[2]),
                                    int(sls_for_sprite_info[3]), sls_for_sprite_info[4], sls_for_sprite_info[5], color))
            sls_for_sprite_info.clear()
        if file_strings[string_num].split()[0] != "end":
            string_num += 1
        else:
            break
    return list_of_sprite, sls_for_file_info, list_of_holders
