import pygame
import os
from os import walk


# вспомогательный файл с функциями и классами


def load_image(name, screen=None, colorkey=None):  # функция для загрузки изображений
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        if name != '': print(f"Файл с изображением '{fullname}' не найден")
        # sys.exit()
        fullname = os.path.join('data', "non_img.png")
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    elif not (screen is None):
        image = image.convert_alpha()
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


class MenySpriteCreate(pygame.sprite.Sprite):  # класс для создания спрайтов начального меню
    def __init__(self, scree=None, rect_x=0, rect_y=0, file_name="", visible_s=False, fuction_s='', promt=''):
        super().__init__()
        self.image = load_image(file_name, scree)
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.image_copy = self.image  # исходное изображение
        self.rect_x_start, self.rect_y_start = rect_x, rect_y  # начальное положение спрайта
        self.visible = visible_s  # видимость спрайта
        self.function = fuction_s  # функция по нажатию
        self.prompt = promt  # название картинки из data, которая должна высветиться при наведении
        #  курсором на спрайт, если подсказка не нужна передать ''


class GameSprite(pygame.sprite.Sprite):  # класс для создания спрайтов игры (в основном для меню)
    def __init__(self, screen, rect_x, rect_y, file_name, visible_s=True, function=''):
        super().__init__()
        self.image = load_image(file_name, screen)
        self.image_copy = self.image
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.rect_x_start, self.rect_y_start = rect_x, rect_y
        self.visible = visible_s
        self.function = function  # название картинки из data, которая должна высветиться при наведении
        #  курсором на спрайт, если подсказка не нужна передать ''


class Countries:  # класс владельцев провинций
    def __init__(self, name, color, money, duty, flag, bot, health_costs, army_costs, political_costs, education_costs,
                 finansical_costs, police_costs, income_tax_1, income_tax_2, holder_army, diplomacy):
        self.name = name
        self.color = color
        self.control_id = []
        self.money = float(money)  # текущий баланс
        self.duty = float(duty)  # внешний долг государства
        # print(name, color, money, duty, flag, bot1, holder_army)
        self.bot = True if bot == "True" else False  # бот или игрок?
        self.flag = flag  # название файла флага страны из data\flags
        self.health_costs = int(health_costs)  # доля ВВП на финансирование здравоохранения
        self.army_costs = int(army_costs)  # процент ВВП на содержание армии
        self.political_costs = int(political_costs)  # расходы на содержание гос аппарата
        self.education_costs = int(education_costs)  # доля ВВП на финансирование образования
        self.finansical_costs = int(finansical_costs)  # доля ВВП на финансирование предпринимательства
        self.police_costs = int(police_costs)  # доля ВВП на финансирование полиции
        self.income_tax_1 = int(income_tax_1)  # ставка подоходного налога на физических лиц
        self.income_tax_2 = int(income_tax_2)  # ставка подоходного налога на компании

        self.army = {}
        for id in holder_army:
            self.army[int(id)] = [[int(s) for s in holder_army[id][0]], [int(s) for s in holder_army[id][1]]]
        # словарь войск (ID провинции: число пехоты, число вспомогательных соединений пехоты(отряды БМП и БТР),
        # число артиллерийских расчетов, количество танковых соединений, самолеты превосходства в воздухе (истребители),
        # самолеты земной поддержки (штурмовики, стратегические бомбардировщики)
        # затем также через точку приказы для артиллерии, авиации, наземных войск
        self.diplomacy = diplomacy


class SpritesCreateForMap(pygame.sprite.Sprite):  # класс для создания спрайтов карты
    def __init__(self, id_province, name, rect_x, rect_y, file_name_img, holder, color,
                 population, tension, support_government, our_support, neighbours, town_list, function, screen_):
        super().__init__()
        self.update = self.update  # функция для обновления цвета
        self.id = int(id_province)  # номер клетки
        self.name = name  # имя провинции
        self.image_copy = load_image(file_name_img, screen_)  # сохранения первоначального изображения
        self.color = (int(color[0]), int(color[1]), int(color[2]))  # цвет, полученный от текущего владельца
        self.image = change_color(self.image_copy, self.color)  # задание цвета (нужно только во время создания)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)  # маска спрайта
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.rect_x_start, self.rect_y_start = rect_x, rect_y
        self.holder = holder  # имя текущего владельца
        self.population = int(population)  # количество населения в регионе
        self.tension = tension  # уровень напряженности в регионе
        self.support_government = int(support_government)  # поддержка текущего правительства
        self.our_support = int(our_support)  # поддержка партии игрока в этом регионе
        self.neighbours = neighbours  # соседние регионы легче вручную расписать для каждой провинции
        self.town_list = town_list
        self.function = function  # хз скорей всего потом уберу

    def update(self, color, koff=1):
        # обновление цвета провинции и маски (к примеру, после захвата или изменения разрешения)
        self.color = (int(color[0]), int(color[1]), int(color[2]))
        self.image = change_color(pygame.transform.scale(self.image_copy, (
            self.image_copy.get_size()[0] * koff, self.image_copy.get_size()[1] * koff)), self.color)
        self.mask = pygame.mask.from_surface(self.image)  # маска спрайта


def file_reader(file_name, screen_):  # чтение файла
    color = ''
    file = open(os.path.join("saves", file_name), mode="r+", encoding="utf-8")
    file_strings = file.readlines()
    sls_for_sprite_info = []  # список параметров игры
    sls_for_file_info, list_of_sprite = [], []  # список параметров читаемого спрайта, которые передаются
    # в SpritesCreateForMap и лист для самих спрайтов соответственно
    holder_info_list, list_of_holders = [], []  # список для информации о читаемом владельце и список
    # всех владельцев соответственно
    string_num = 0  # номер читаемой строки
    sprite_bildings = {}
    holder_army = {}
    diplomacy = {}

    while file_strings[string_num].split()[0] != "holder(":  # чтение информации об игре (все строки до "holder(")
        sls_for_file_info.append(file_strings[string_num].split()[2])  # чтобы потом обратиться к какому-либо
        # параметру необходимо знать его индекс в списке (просто в файле посмотреть номер строки)
        string_num += 1
    string_num += 1
    while file_strings[string_num].split()[0] != ")":  # чтение владельцев и информации о них
        if file_strings[string_num].split()[0] != '|' and file_strings[string_num].split()[0] != ')':
            if file_strings[string_num].split()[1] == "army_in_it":
                holder_army[file_strings[string_num].split()[2].split('.')[0]] = [
                    file_strings[string_num].split()[2].split('.')[1:],
                    file_strings[string_num].split()[3].split('.')]
            elif file_strings[string_num].split()[0] == "diplomacy:":
                diplomacy[file_strings[string_num].split()[1]] = [file_strings[string_num].split()[2],
                                                                  file_strings[string_num].split()[3]]
            else:
                holder_info_list.append(file_strings[string_num].split()[2])
        else:
            army2 = holder_army.copy()
            list_of_holders.append(
                Countries(holder_info_list[0], holder_info_list[1], holder_info_list[2], holder_info_list[3],
                          os.path.join("flags", holder_info_list[4]), holder_info_list[5], holder_info_list[6],
                          holder_info_list[7], holder_info_list[8], holder_info_list[9], holder_info_list[10],
                          holder_info_list[11], holder_info_list[12], holder_info_list[13], army2, diplomacy))
            # list_of_holders.append(Countries(holder_info_list[0], holder_info_list[1], holder_army))
            holder_info_list.clear()
            holder_army.clear()
        string_num += 1
    string_num += 2

    index = 10
    while file_strings[string_num].split()[0] != ")":  # чтение спрайтов регионов
        if file_strings[string_num].split()[0] != '|' and file_strings[string_num].split()[0] != ')':
            if file_strings[string_num].split()[1] == "objects":
                index += 1
                sprite_bildings[file_strings[string_num].split()[2].split('.')[0] + str(index)] = \
                    [file_strings[string_num].split()[2].split('.')[1:-2], \
                        file_strings[string_num].split()[2].split('.')[
                            -2], file_strings[string_num].split()[2].split('.')[-1]]
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
                                    sls_for_sprite_info[9], sls_for_sprite_info[10].split('.'),
                                    sprite_bildings_copy, "open_region_info", screen_))
            sls_for_sprite_info.clear()
            sprite_bildings.clear()
        string_num += 1
    file.close()
    list_for_return = [list_of_sprite, sls_for_file_info, list_of_holders]
    return list_for_return
