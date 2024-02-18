from special import *
from setting_file import render_setting, open_settings, setting_event


# главный файл игры

class MainGameClass:
    def __init__(self, filename):

        # параметры окна игры
        self.size_menu = None
        self.screen_main = None
        self.create_window()

        # объявление спрайтов игры, экземпляров класса GameSprite из special.py
        self.sprite_province_info = GameSprite(self.screen_main, 500, 10,
                                               os.path.join("game_sprites", "province_info.png"),
                                               False,
                                               "move_region_menu")  # спрайт взаимодействия с регионом
        self.sprite_country_info = GameSprite(self.screen_main, 500, 500,
                                              os.path.join("game_sprites", "country_info.png"), False,
                                              "move_region_menu")  # спрайт для взаимодействия с регионом

        self.sprite_open_menu = GameSprite(self.screen_main, 1400, 10, os.path.join("game_sprites", "menu_game.png"),
                                           True,
                                           "menu_click")
        self.sprite_menu = GameSprite(self.screen_main, 400, 200, os.path.join("game_sprites", "menu.png"), False,
                                      "")
        self.sprite_open_setting = GameSprite(self.screen_main, self.sprite_menu.rect.x + 50,
                                              self.sprite_menu.rect.y + 50,
                                              "setting_btn_img.png", False, "open_settings")
        self.sprite_return_menu = GameSprite(self.screen_main, self.sprite_menu.rect.x + 50,
                                             self.sprite_menu.rect.y + 200,
                                             os.path.join("game_sprites", "return_start_menu.png"), False,
                                             "return_start_menu")
        self.top_panel = GameSprite(self.screen_main, 0, 0, os.path.join("game_sprites", "top_panel.png"), True, "")

        # "глобальные" переменные класса MainGameClass
        self.running_2 = True
        self.file_name = filename
        self.selected_map_sprite_2 = None
        self.selected_map_sprite = None

        # список для определенных спрайтов(меню региона, меню владельца)
        self.special_sprite_list = [self.sprite_province_info, self.sprite_country_info]
        self.single_group_1 = pygame.sprite.GroupSingle(
            self.sprite_province_info)  # одиночная группа для sprite_province_info
        self.single_group_2 = pygame.sprite.GroupSingle(
            self.sprite_country_info)  # одиночная группа для sprite_country_info
        self.interface_sprite_list = [self.top_panel, self.sprite_open_menu]  # лист для спрайтов интерфейса 1
        self.menus_sprite_list1 = [self.sprite_menu, self.sprite_return_menu,
                                   self.sprite_open_setting]  # лист для спрайтов интерфейса 2
        self.group_interface = pygame.sprite.Group()  # и группа для них
        self.group_buildings_icons = pygame.sprite.Group()  # группа для иконок при отображении информации о регионе
        info_list_from_file = file_reader(self.file_name, self.screen_main)  # получение информации из файла
        self.sprite_map_list = info_list_from_file[0]  # список спрайтов карты
        self.group_map_sprite = pygame.sprite.Group()  # и группа спрайтов для них
        self.file_info_list = info_list_from_file[1]  # список с информацией об игре (время, сложность и тд)
        self.country_list = info_list_from_file[2]  # список стран (возможных владельцев)
        self.sprite_move_now = self.special_sprite_list[0]
        self.flag_move_1 = False  # флаг перемещения спрайта взаимодействия с регионом
        self.mouse_start = 0, 0  # позиции мыши в начале перемещения
        self.click_r_1 = False  # флаг (если выключен, спрайт не сможет выйти за границы экрана)
        self.next_window = True
        self.functions = {
            # наконец решил оформить код, исполняемый при нажатии
            # на спрайт в отдельные функции и поместить их в словарь...
            "open_region_info": self.open_sprite_list,  # вызывается при нажатии лкм на регион
            "open_region_info_2": self.open_sprite_list_2,  # вызывается при нажатии пкм на регион
            "move_region_menu": self.move_region_menu,  # вызывается, если пкм зажата на объекте из special_sprite_list
            "menu_click": self.menu_click,  # вызывается при нажатии special_sprite_list
            "open_settings": open_settings,  # вызов окна настроек, функции из special_2.py
            "return_start_menu": self.return_start_menu
        }
        self.main_render()

    def create_window(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 30)
        pygame.init()
        self.size_menu = 1536, 800  # размер окна
        self.screen_main = pygame.display.set_mode(self.size_menu)
        # self.screen_main = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        image_for_icon = load_image("icon_for_game.png")  # изображение для иконки приложения
        pygame.display.set_icon(image_for_icon)
        pygame.display.set_caption('The final strike')  # название приложения

    def fake__init__(self):
        pygame.quit()
        self.running_2 = True
        for spr_ in self.menus_sprite_list1:
            spr_.visible = False
        pygame.init()
        self.create_window()
        self.main_render()

    def return_start_menu(self):
        open_settings(True)
        self.running_2 = False
        self.next_window = True

    def move_region_menu(self, flag, mouse_start_pos, flag2=False):  # функция для перемещения спрайта
        delta_x = pygame.mouse.get_pos()[0] - mouse_start_pos[0]  # изменение координат по x
        delta_y = pygame.mouse.get_pos()[1] - mouse_start_pos[1]  # изменение координат по y
        if flag:  # True, если левая кнопка мыши зажата на спрайте
            self.sprite_move_now.rect.x = delta_x
            self.sprite_move_now.rect.y = delta_y
        if self.sprite_move_now.rect.y + self.sprite_move_now.rect[2] - 450 > self.size_menu[1]:
            self.sprite_move_now.rect.y -= 3
        elif self.sprite_move_now.rect.y < -350:
            self.sprite_move_now.rect.y += 3
        if self.sprite_move_now.rect.x > self.size_menu[0] - 50:
            self.sprite_move_now.rect.x -= 3
        elif self.sprite_move_now.rect.x + self.sprite_move_now.rect[3] < -50:
            self.sprite_move_now.rect.x += 3
        if flag2:
            if self.sprite_move_now.rect.y + self.sprite_move_now.rect[1] > self.size_menu[1]:
                self.sprite_move_now.rect.y -= 3
            elif self.sprite_move_now.rect.y + self.sprite_move_now.rect[1] < 0:
                self.sprite_move_now.rect.y += 3
            if self.sprite_move_now.rect.x + self.sprite_move_now.rect[2] > self.size_menu[0]:
                self.sprite_move_now.rect.x -= 3
            elif self.sprite_move_now.rect.x < 0:
                self.sprite_move_now.rect.x += 3

    def render_interface(self):  # функция для отображения спрайтов интерфейса
        for i in [self.interface_sprite_list, self.menus_sprite_list1]:
            for spr_ in i:
                if spr_.visible:
                    self.group_interface.add(spr_)
                elif not spr_.visible and spr_ in self.group_interface:
                    self.group_interface.remove(spr_)
        self.group_interface.draw(self.screen_main)

    def job_with_menu(self):
        self.sprite_menu.visible = not self.sprite_menu.visible
        self.sprite_open_setting.visible = not self.sprite_open_setting.visible
        self.sprite_return_menu.visible = not self.sprite_return_menu.visible

    def menu_click(self):  # открытие меню
        self.job_with_menu()
        if not self.sprite_menu.visible: open_settings(True)

    def open_sprite_list_2(self, flag=False, sprite=''):  # отображения окна государства (вызывается если
        # игрок нажал правой клавишей на регион
        if flag:
            if sprite != '' and self.sprite_country_info.visible and self.selected_map_sprite_2 != sprite:
                self.selected_map_sprite_2 = sprite
            else:
                self.selected_map_sprite_2 = sprite
                self.sprite_country_info.visible = not self.sprite_country_info.visible
        if self.sprite_country_info.visible:
            self.single_group_2.draw(self.screen_main)
            index = 0
            for i in range(len(self.country_list)):
                if self.selected_map_sprite_2.holder == self.country_list[i].name:
                    index = i
                    break
            if not self.country_list[index].bot:  # отображение если выбранная страна - игрок (self.bot == False)
                pass
            else:  # отображение окна, если выбранная страна это бот
                pass

    def open_sprite_list(self, flag=False, sprite=''):  # функция для смены видимости окна и его отображения
        # если передать True и экземпляр нажатого класса SpritesCreateForMap,
        # то выбранный регион изменится на переданный спрайт
        if flag:
            if sprite != '' and self.sprite_province_info.visible and self.selected_map_sprite != sprite:
                self.selected_map_sprite = sprite
            else:
                self.selected_map_sprite = sprite
                self.sprite_province_info.visible = not self.sprite_province_info.visible
        else:
            if self.sprite_province_info.visible:
                self.single_group_1.draw(self.screen_main)
                str1 = "население: " + str(self.selected_map_sprite.population) + "чел."
                str2 = ("поддержка враждебных партий: " + str("%.2f" % (
                        self.selected_map_sprite.support_government / self.selected_map_sprite.population * 100)) + "%"
                        + " (" + str(self.selected_map_sprite.support_government) + ')')
                str3 = ("поддержка нашего движения: " + str(
                    "%.2f" % (
                            self.selected_map_sprite.our_support / self.selected_map_sprite.population * 100)) + "%" +
                        " (" + str(self.selected_map_sprite.our_support) + ")")
                sls = [str1, str2, str3]
                for i in range(len(sls)):  # отображение информации о спрайте
                    self.screen_main.blit(pygame.font.Font(None, 26).render(sls[i], True, (255, 0, 0)),
                                          (self.sprite_province_info.rect.x + 20,
                                           self.sprite_province_info.rect.y + 30 + (i * 20)))
                self.screen_main.blit(
                    pygame.font.Font(None, 32).render(self.selected_map_sprite.name, True, (255, 0, 0)),
                    (self.sprite_province_info.rect.x + 200,
                     self.sprite_province_info.rect.y + 10))  # вывести название региона
                index_x = 0  # индекс смещения иконок по x и y соответственно
                for el in self.selected_map_sprite.town_list:  # цикл для отображения всех построек и местности региона
                    self.group_buildings_icons.add(
                        GameSprite(self.screen_main, self.sprite_province_info.rect.x + 10 + index_x * 60,
                                   self.sprite_province_info.rect.y + 110,
                                   os.path.join("bildings_icons", el[0:-2]) + '.png'))
                    self.group_buildings_icons.add(
                        GameSprite(self.screen_main, self.sprite_province_info.rect.x + 10 + index_x * 60,
                                   self.sprite_province_info.rect.y + 90,
                                   os.path.join("bildings_icons",
                                                self.selected_map_sprite.town_list[el][-1]) + '.png'))
                    for i in range(len(self.selected_map_sprite.town_list[el][0])):
                        self.group_buildings_icons.add(
                            GameSprite(self.screen_main, self.sprite_province_info.rect.x + 10 + index_x * 60,
                                       self.sprite_province_info.rect.y + 110 + (i + 1) * 60,
                                       os.path.join("bildings_icons",
                                                    self.selected_map_sprite.town_list[el][0][
                                                        i]) + '.png'))
                    index_x += 1
                self.group_buildings_icons.draw(self.screen_main)
                for i in self.group_buildings_icons:  # Очистка
                    self.group_buildings_icons.remove(i)

    def stop(self):
        self.next_window = False

    def main_render(self):
        for sprite_ in self.sprite_map_list:  # добавление всех спрайтов карты в группу group_map_sprite
            self.group_map_sprite.add(sprite_)
        clock = pygame.time.Clock()
        while self.running_2:
            clock.tick(60)
            events = pygame.event.get()
            for event in events:
                setting_event(event)
                if event.type == pygame.QUIT:
                    self.running_2 = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.flag_move_1 = False
                if event.type == pygame.MOUSEBUTTONDOWN:

                    for sprit in self.sprite_map_list:  # проверка нажатия на ргион
                        pos_in_mask = event.pos[0] - sprit.rect.x, event.pos[1] - sprit.rect.y
                        if sprit.rect.collidepoint(event.pos) and sprit.mask.get_at(pos_in_mask):
                            if pygame.mouse.get_pressed()[0]:  # проверка, что была нажата левая клавиша мыши
                                function_call = self.functions[sprit.function]  # вызов функции по атрибуту function
                                function_call(True, sprit)  # который передается как ключ в словарь функций functions
                            elif pygame.mouse.get_pressed()[2]:  # проверка, что была нажата левая клавиша мыши
                                function_call = self.functions[
                                    sprit.function + '_2']  # вызов функции по атрибуту function
                                function_call(True, sprit)  # который передается как ключ в словарь функций functions
                    for sprit_ in [s for s in self.special_sprite_list if s.rect.collidepoint(pygame.mouse.get_pos())]:
                        if sprit_.visible:
                            self.sprite_move_now = sprit_
                            if sprit_.function == "move_region_menu" and pygame.mouse.get_pressed()[0]:
                                self.flag_move_1 = not self.flag_move_1
                                if self.flag_move_1:
                                    self.mouse_start = pygame.mouse.get_pos()[0] - sprit_.rect.x, \
                                                       pygame.mouse.get_pos()[
                                                           1] - sprit_.rect.y
                            elif sprit_.function == "move_region_menu" and pygame.mouse.get_pressed()[2]:
                                self.click_r_1 = not self.click_r_1
                            break
                    for i in [self.menus_sprite_list1, self.interface_sprite_list]:
                        for sprit_2 in i:
                            if sprit_2.rect.collidepoint(pygame.mouse.get_pos()) and sprit_2.visible:
                                if pygame.mouse.get_pressed()[0]:
                                    if sprit_2.function != '':
                                        function_call = self.functions[sprit_2.function]
                                        function_call()
            if not self.running_2: break
            pygame.draw.rect(self.screen_main, (0, 0, 0),
                             (0, 0, self.size_menu[0], self.size_menu[1]))  # (временно) заполнение экрана черным фоном

            self.group_map_sprite.draw(self.screen_main)  # отрисовка карты

            self.open_sprite_list_2()  # отрисовка меню страны

            self.open_sprite_list()  # отрисовка меню региона

            self.move_region_menu(self.flag_move_1, self.mouse_start,
                                  True) if self.click_r_1 else self.move_region_menu(
                self.flag_move_1, self.mouse_start)

            self.render_interface()  # отрисовка интерфейса
            render_setting(self.screen_main)
            pygame.display.update()
