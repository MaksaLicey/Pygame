import pygame
import os
import sys
from os import walk


# вспомогательный файл с функциями и классами


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


class MenySpriteCreate(pygame.sprite.Sprite):  # класс для создания спрайтов меню
    def __init__(self, rect_x, rect_y, file_name, visible_s, fuction_s='', promt=''):
        super().__init__()
        self.image = load_image(file_name)
        self.size = load_image(file_name).get_size()
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.visible = visible_s
        self.function = fuction_s
        self.prompt = promt  # название картинки из data, которая должна высветиться при наведении
        #  курсором на спрайт, если подсказка не нужна передать ''


class GameSprite(pygame.sprite.Sprite):  # класс для создания спрайтов игры
    def __init__(self, rect_x, rect_y, file_name, visible_s=True, function=''):
        super().__init__()
        self.image = load_image(file_name)
        self.size = load_image(file_name).get_size()
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.visible = visible_s
        self.function = function  # название картинки из data, которая должна высветиться при наведении
        #  курсором на спрайт, если подсказка не нужна передать ''


class Countries:  # класс владельцев провинций
    def __init__(self, name, color, money, duty, flag, holder_army):
        self.name = name
        self.color = color
        self.control_id = []
        self.army = holder_army
        self.money = money  # текущий баланс
        self.duty = duty  # внешний долг государства
        self.flag = flag  # название файла флага страны из data\flags


class SpritesCreateForMap(pygame.sprite.Sprite):  # класс для создания спрайтов карты
    def __init__(self, id_province, name, rect_x, rect_y, file_name_img, holder, color,
                 population, tension, support_government, our_support, neighbours, town_list, function):
        super().__init__()
        self.update = self.update  # функция для обновления цвета
        self.id_province = id_province  # номер клетки
        self.name = name  # имя провинции
        self.image_start = load_image(file_name_img)  # сохранения первоначального изображения
        self.color = (int(color[0]), int(color[1]), int(color[2]))  # цвет, полученный от текущего владельца
        self.image = change_color(self.image_start, self.color)  # задание цвета (нужно только во время создания)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)  # маска спрайта
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.holder = holder  # имя текущего владельца
        self.population = int(population)  # количество населения в регионе
        self.tension = tension  # уровень напряженности в регионе
        self.support_government = int(support_government)  # поддержка текущего правительства
        self.our_support = our_support  # поддержка партии игрока в этом регионе
        self.neighbours = neighbours  # соседние регионы легче вручную расписать для каждой провинции
        self.town_list = town_list
        self.function = function  # хз скорей всего потом уберу

    def update(self, color):  # обновление цвета провинции (к примеру, после захвата)
        self.color = (int(color[0]), int(color[1]), int(color[2]))
        self.image = change_color(self.image_start, self.color)


def file_reader(file_name):  # чтение файла
    color = ''
    file = open(os.path.join("saves", file_name), mode="r+", encoding="utf-8")
    file_strings = file.readlines()
    sls_for_sprite_info = []  # список параметров игры
    sls_for_file_info, list_of_sprite = [], []  # список параметров читаемого спрайта, которые передаются
    # в SpritesCreateForMap и лист для самих спрайтов соответственно
    holder_info_list, list_of_holders = [], []  # список для информации о читаемом владельце и список
    # всех владельцев соответственно
    string_num = 0  # номер читаемой строки
    # Т.к. класс SpritesCreateForMap и Countries никак не связаны, каждый, что определить
    sprite_bildings = {}
    holder_army = {}

    while file_strings[string_num].split()[0] != "holder(":  # чтение информации об игре (все строки до "holder(")
        sls_for_file_info.append(file_strings[string_num].split()[2])  # чтобы потом обратиться к какому-либо
        # параметру необходимо знать его индекс в списке (просто в файле посмотреть номер строки)
        string_num += 1
    string_num += 1
    while file_strings[string_num].split()[0] != ")":  # чтение владельцев и информации о них
        if file_strings[string_num].split()[0] != '|' and file_strings[string_num].split()[0] != ')':
            if file_strings[string_num].split()[1] == "army_in_it":
                holder_army[file_strings[string_num].split()[2].split('.')[0]] = file_strings[string_num].split()[
                                                                                     2].split('.')[1:]
            else:
                holder_info_list.append(file_strings[string_num].split()[2])
        else:
            army2 = holder_army.copy()
            list_of_holders.append(
                Countries(holder_info_list[0], holder_info_list[1], holder_info_list[2], holder_info_list[3],
                          os.path.join("flags", holder_info_list[4]), army2))
            # list_of_holders.append(Countries(holder_info_list[0], holder_info_list[1], holder_army))
            holder_info_list.clear()
            holder_army.clear()
        string_num += 1
    string_num += 2

    index = 10
    while file_strings[string_num].split()[0] != ")":  # чтение владельцев и информации о них
        if file_strings[string_num].split()[0] != '|' and file_strings[string_num].split()[0] != ')':
            if file_strings[string_num].split()[1] == "objects":
                index += 1
                sprite_bildings[file_strings[string_num].split()[2].split('.')[0] + str(index)] = \
                    file_strings[string_num].split()[2].split('.')[1:-2], \
                        file_strings[string_num].split()[2].split('.')[-2], \
                        file_strings[string_num].split()[2].split('.')[
                            -1]
            else:
                sls_for_sprite_info.append(file_strings[string_num].split()[2])
        else:
            for i in list_of_holders:  # изменение цвета в соответствии с цветом страны
                if sls_for_sprite_info[5] == i.name:
                    color = i.color.split('.')
                    i.control_id.append(sls_for_sprite_info[0])
                else:
                    if sls_for_sprite_info[0] in i.control_id:
                        i.control_id.remove(sls_for_sprite_info[0])
            # print(sprite_bildings)
            sprite_bildings_copy = sprite_bildings.copy()
            list_of_sprite.append(  # добавление спрайта - провинции в список
                SpritesCreateForMap(sls_for_sprite_info[0], sls_for_sprite_info[1], int(sls_for_sprite_info[2]),
                                    int(sls_for_sprite_info[3]), sls_for_sprite_info[4], sls_for_sprite_info[5], color,
                                    sls_for_sprite_info[6], sls_for_sprite_info[7], sls_for_sprite_info[8],
                                    sls_for_sprite_info[9], sls_for_sprite_info[10].split('.'), sprite_bildings_copy,
                                    "open_region_info"))
            sls_for_sprite_info.clear()
            sprite_bildings.clear()
        string_num += 1
    file.close()
    list_for_return = [list_of_sprite, sls_for_file_info, list_of_holders]
    return list_for_return
