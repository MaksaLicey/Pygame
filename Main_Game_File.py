import pygame.mouse

from special import *
from setting_file import render_setting, open_settings, setting_event, apply_settings


# import asyncio


# главный файл игры

class MainGameClass:  # класс приложения игры
    def __init__(self, filename):
        self.main_size = 1536, 800  # основной размер окна игры
        file = open(os.path.join("data", "settings", "setting_file"))
        settings = file.readlines()  # считывание настроек с файла data\settings\setting_file
        self.fps = int(settings[0])
        self.size_cof = int(settings[3].split()[0]) / self.main_size[1]
        file.close()
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
                                              self.sprite_menu.rect.y + 40,
                                              "setting_btn_img.png", False, "open_settings")
        self.sprite_btn_save_file = GameSprite(self.screen_main, self.sprite_menu.rect.x, self.sprite_menu.rect.y + 160,
                                               os.path.join("game_sprites", "save_file_btn.png"), False,
                                               "save_game_file")
        self.sprite_return_menu = GameSprite(self.screen_main, self.sprite_menu.rect.x + 50,
                                             self.sprite_menu.rect.y + 240,
                                             os.path.join("game_sprites", "return_start_menu.png"), False,
                                             "return_start_menu")
        self.quit_game = GameSprite(self.screen_main, self.sprite_menu.rect.x + 10, self.sprite_menu.rect.y + 390,
                                    "leave_game.png", False, "leave_game")
        self.top_panel = GameSprite(self.screen_main, 0, 0, os.path.join("game_sprites", "top_panel.png"), True, "")
        self.dept_up1 = GameSprite(self.screen_main, 180, 10, os.path.join("game_sprites", "dept_up1.png"), True,
                                   "dept+10")
        self.dept_up2 = GameSprite(self.screen_main, 240, 10, os.path.join("game_sprites", "dept_up1.png"), True,
                                   "dept+100")
        self.dept_down1 = GameSprite(self.screen_main, 180, 60, os.path.join("game_sprites", "dept_down1.png"), True,
                                     "dept-10")
        self.dept_down2 = GameSprite(self.screen_main, 240, 60, os.path.join("game_sprites", "dept_down2.png"), True,
                                     "dept-100")
        self.leave_sprite_1 = GameSprite(self.screen_main, 200, 100, os.path.join("game_sprites", "leave_panel_1.png"),
                                         False, "")
        self.leave_sprite_2 = GameSprite(self.screen_main, self.leave_sprite_1.rect.x + 100,
                                         self.leave_sprite_1.rect.y + 50,
                                         os.path.join("game_sprites", "leave_btn_1.png"), False, "game_break")
        self.leave_sprite_3 = GameSprite(self.screen_main, self.leave_sprite_1.rect.x + 100,
                                         self.leave_sprite_1.rect.y + 170,
                                         os.path.join("game_sprites", "leave_btn_2.png"), False, "save_game_file")
        self.leave_sprite_4 = GameSprite(self.screen_main, self.leave_sprite_1.rect.x + 10,
                                         self.leave_sprite_1.rect.y + 10,
                                         os.path.join("game_sprites", "leave_btn_3.png"), False, "close_leave_menu")

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
        self.menus_sprite_list1 = [self.sprite_menu, self.sprite_return_menu, self.quit_game, self.sprite_btn_save_file,
                                   self.sprite_open_setting]  # лист для спрайтов интерфейса 2
        self.interface_sprite_list_2 = [self.leave_sprite_1, self.leave_sprite_2, self.leave_sprite_3,
                                        self.leave_sprite_4]
        self.group_interface = pygame.sprite.Group()  # и группа для них
        info_list_from_file = file_reader(self.file_name, self.screen_main)  # получение информации из файла
        self.time = info_list_from_file[1][-1].split(".")
        self.sprite_map_list = info_list_from_file[0]  # список спрайтов карты
        # print(self.sprite_map_list[0].town_list)
        self.group_map_sprite = pygame.sprite.Group()  # и группа спрайтов для них
        self.file_info_list = info_list_from_file[1]  # список с информацией об игре (время, сложность и тд)
        self.country_list = info_list_from_file[2]  # список стран (возможных владельцев)
        self.player = None
        for spr in self.country_list:
            if not spr.bot:  # определение класса игрока
                self.player = spr
        self.flag_player = GameSprite(self.screen_main, 5, 5, self.player.flag, True, "open_country_political")
        self.country_political = GameSprite(self.screen_main, 0, 100,
                                            os.path.join("game_sprites", "country_political.png"), False,
                                            "")
        self.health_costs = MenySpriteCreate(self.screen_main, 20, 140,
                                             os.path.join("game_sprites", "health_costs.png"), False,
                                             "")
        self.health_costs = MenySpriteCreate(self.screen_main, 20, 140,
                                             os.path.join("game_sprites", "health_costs.png"), False,
                                             "")
        self.sprite_up_tax_1 = GameSprite(self.screen_main, self.country_political.rect.x + 20,
                                          self.country_political.rect.y + 410,
                                          os.path.join("game_sprites", "up_law.png"), False,
                                          "up_tax_1")
        self.sprite_down_tax_1 = GameSprite(self.screen_main, self.country_political.rect.x + 60,
                                            self.country_political.rect.y + 410,
                                            os.path.join("game_sprites", "down_law.png"), False,
                                            "down_tax_1")
        self.sprite_up_tax_2 = GameSprite(self.screen_main, self.country_political.rect.x + 20,
                                          self.country_political.rect.y + 450,
                                          os.path.join("game_sprites", "up_law.png"), False,
                                          "up_tax_2")
        self.sprite_down_tax_2 = GameSprite(self.screen_main, self.country_political.rect.x + 60,
                                            self.country_political.rect.y + 450,
                                            os.path.join("game_sprites", "down_law.png"), False,
                                            "down_tax_2")

        self.interface_sprite_list = [self.top_panel, self.sprite_open_menu, self.dept_up1, self.dept_up2,
                                      self.dept_down1, self.dept_down2,
                                      self.flag_player]  # лист для спрайтов интерфейса 1
        self.political_interface = [self.country_political, self.health_costs,
                                    self.sprite_up_tax_1, self.sprite_up_tax_2,
                                    self.sprite_down_tax_1, self.sprite_down_tax_2]

        self.sprite_move_now = self.special_sprite_list[0]
        self.flag_move_1 = False  # флаг перемещения спрайта взаимодействия с регионом
        self.mouse_start = 0, 0  # позиции мыши в начале перемещения
        self.click_r_1 = False  # флаг (если выключен, спрайт не сможет выйти за границы экрана)
        self.next_window = True

        self.sls_img_1 = []  # список для картинок местности регионе
        self.sls_img_2 = []  # список для картинок построек местности в регионе
        self.sls_img_3 = []  # список для картинок уровня прочности построек в местности
        self.sls_img_4 = []  # список для изображений кнопок ремонта и разрушения инфраструктуры
        # P.S. не определился какая максимальная "длинна" региона может быть и сколько спрайтов кнопок надо создать

        self.functions = {
            # наконец решил оформить код, исполняемый при нажатии
            # на спрайт в отдельные функции и поместить их в словарь...
            "open_region_info": self.open_sprite_list,  # вызывается при нажатии лкм на регион
            "open_region_info_2": self.open_sprite_list_2,  # вызывается при нажатии пкм на регион
            "move_region_menu": self.move_region_menu,  # вызывается, если пкм зажата на объекте из special_sprite_list
            "menu_click": self.menu_click,  # вызывается при нажатии special_sprite_list
            "open_settings": open_settings,  # вызов окна настроек, функции из special_2.py
            "return_start_menu": self.return_start_menu,
            "leave_game": self.leave_game,
            "game_break": self.game_break,
            "save_game_file": self.save_game_file,
            "close_leave_menu": self.close_leave_menu,
            "open_country_political": self.open_country_political,
            "up_tax_1": self.up_tax_1,
            "down_tax_1": self.down_tax_1,
            "down_tax_2": self.down_tax_2,
            "up_tax_2": self.up_tax_2
        }
        for sprite_ in self.sprite_map_list:  # добавление всех спрайтов карты в группу group_map_sprite
            self.group_map_sprite.add(sprite_)
        self.sprite_change_size()
        self.main_render()

    def fake__init__(self):  # запуск без инициализации нового экземпляра
        pygame.quit()
        self.running_2 = True
        for spr_ in self.menus_sprite_list1:
            spr_.visible = False
        pygame.init()
        self.create_window()
        self.sprite_change_size()
        self.main_render()

    def create_window(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 30)
        pygame.init()
        self.size_menu = self.main_size[0] * self.size_cof, self.main_size[1] * self.size_cof  # размер окна
        self.screen_main = pygame.display.set_mode(self.size_menu)
        # self.screen_main = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        image_for_icon = load_image("icon_for_game.png")  # изображение для иконки приложения
        pygame.display.set_icon(image_for_icon)
        pygame.display.set_caption('The final strike')  # название приложения

    def move_region_menu(self, flag, mouse_start_pos, flag2=False):  # функция для перемещения спрайта
        delta_x = pygame.mouse.get_pos()[0] - mouse_start_pos[0]  # изменение координат по x
        delta_y = pygame.mouse.get_pos()[1] - mouse_start_pos[1]  # изменение координат по y
        if flag:  # True, если левая кнопка мыши зажата на спрайте
            self.sprite_move_now.rect.x = delta_x  # * self.size_cof
            self.sprite_move_now.rect.y = delta_y  # * self.size_cof
        if self.sprite_move_now.rect.y > self.size_menu[1] - 50 * self.size_cof:
            self.sprite_move_now.rect.y -= int(3 * self.size_cof)
        elif self.sprite_move_now.rect.y + self.sprite_move_now.rect[3] < self.top_panel.rect[3] + 50 * self.size_cof:
            self.sprite_move_now.rect.y += int(3 * self.size_cof)
        if self.sprite_move_now.rect.x > self.size_menu[0] - 50 * self.size_cof:
            self.sprite_move_now.rect.x -= int(3 * self.size_cof)
        elif self.sprite_move_now.rect.x + self.sprite_move_now.rect[2] < 50 * self.size_cof:
            self.sprite_move_now.rect.x += int(3 * self.size_cof)
        if flag2:
            if self.sprite_move_now.rect.y + self.sprite_move_now.rect[3] > self.size_menu[1]:
                self.sprite_move_now.rect.y -= int(3 * self.size_cof)
            elif self.sprite_move_now.rect.y < self.top_panel.rect[3]:
                self.sprite_move_now.rect.y += int(3 * self.size_cof)
            if self.sprite_move_now.rect.x + self.sprite_move_now.rect[2] > self.size_menu[0]:
                self.sprite_move_now.rect.x -= int(3 * self.size_cof)
            elif self.sprite_move_now.rect.x < 0:
                self.sprite_move_now.rect.x += int(3 * self.size_cof)

    def return_start_menu(self):
        if open_settings(True) != "error":
            # open_settings(True)
            self.running_2 = False
            self.next_window = True
            self.save_game_file()

    def open_country_political(self, flag=True):
        for spr_ in self.political_interface:
            spr_.visible = not spr_.visible if flag else False

    def dept_change(self, factor=0):  # наращивание либо выплата госдолга
        if self.player.duty + factor < 0:
            self.player.money -= self.player.duty
            self.player.duty = 0
        else:
            self.player.money += factor * 5 if pygame.key.get_mods() == 4097 else factor
            # если зажать shift при увеличении\уменьшении долга произойдет изменение на factor * 5
            self.player.duty += factor * 5 if pygame.key.get_mods() == 4097 else factor

        if self.player.money < 0:  # Автоматическое кредитование, т.к. баланс не может быть < 0
            self.player.duty += -1 * self.player.money + 10
            self.player.money += -1 * self.player.money + 10

    def job_with_menu(self):
        for i in self.menus_sprite_list1:
            i.visible = not i.visible
        if not self.menus_sprite_list1[-1].visible:
            for i in self.interface_sprite_list_2:
                i.visible = False

    def menu_click(self):  # открытие меню
        self.job_with_menu()
        self.open_country_political(False)
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
            # for i in range(len(self.country_list)):
            #     if self.selected_map_sprite_2.holder == self.country_list[i].name:
            #         index = i
            #         break
            self.screen_main.blit(
                pygame.font.Font(None, int(32 * self.size_cof)).render(self.selected_map_sprite_2.holder, True,
                                                                       (0, 0, 0)), (
                    self.sprite_country_info.rect.x + 100 * self.size_cof,
                    self.sprite_country_info.rect.y + 10 * self.size_cof))
            if not self.country_list[index].bot:  # отображение если выбранная страна - игрок (self.bot == False)
                pass
            else:  # отображение окна, если выбранная страна это бот
                pass

    def open_sprite_list(self, flag=False, sprite=None):  # функция для смены видимости окна региона и его отображения
        # если передать True и экземпляр нажатого класса SpritesCreateForMap,
        # то выбранный регион изменится на переданный спрайт
        if flag:
            if not (sprite is None) and self.sprite_province_info.visible and self.selected_map_sprite != sprite:
                self.selected_map_sprite = sprite
            else:
                self.selected_map_sprite = sprite
                self.sprite_province_info.visible = not self.sprite_province_info.visible
            if self.sprite_province_info.visible:
                self.sls_img_1.clear()  # коллекция картинок для местности
                self.sls_img_2.clear()  # коллекция картинок для строений
                self.sls_img_3.clear()
                self.sls_img_4.clear()

                for el in self.selected_map_sprite.town_list:
                    self.sls_img_1.append(
                        load_image(os.path.join("bildings_icons", el[0:-2]) + '.png', self.screen_main))
                    self.sls_img_3.append(
                        load_image(os.path.join("bildings_icons", self.selected_map_sprite.town_list[el][-1]) + '.png',
                                   self.screen_main))
                    self.sls_img_4.append(load_image(os.path.join("bildings_icons", "restore.png"), self.screen_main))
                    self.sls_img_4.append(load_image(os.path.join("bildings_icons", "destroy.png"), self.screen_main))
                    for i in range(len(self.selected_map_sprite.town_list[el][0])):
                        self.sls_img_2.append(load_image(
                            os.path.join("bildings_icons", self.selected_map_sprite.town_list[el][0][i]) + '.png',
                            self.screen_main))
        else:
            if self.sprite_province_info.visible:
                self.single_group_1.draw(self.screen_main)
                str1 = "население: " + str(self.selected_map_sprite.population) + "чел."
                str2 = ("поддержка враждебных партий: " + str("%.2f" % (
                        self.selected_map_sprite.support_government / self.selected_map_sprite.population * 100 * self.size_cof)) + "%"
                        + " (" + str(self.selected_map_sprite.support_government) + ')')
                str3 = ("поддержка нашего движения: " + str(
                    "%.2f" % (
                            self.selected_map_sprite.our_support / self.selected_map_sprite.population * 100 * self.size_cof)) + "%" +
                        " (" + str(self.selected_map_sprite.our_support) + ")")
                str4 = ("союзные войска: " + str(self.player.army[self.selected_map_sprite.id][0]))
                str5 = []
                str5_copy = []
                for c in self.country_list:
                    if c.army[self.selected_map_sprite.id][0] != [0] * 5 and c.army != self.player.army:
                        str__ = ''
                        for i in c.army[self.selected_map_sprite.id][0]:
                            str__ += str(i) + '   '
                        str5.append(c.name + ' (' + self.player.diplomacy[c.name][1] + ') ' + str__)
                str5_copy = str5[0:4] + ['...'] if len(str5) > 4 else str5  # выводить не более 4 армий различных стран
                sls = [str1, str2, str3, str4, *str5_copy]
                for i in range(len(sls)):  # отображение информации о спрайте
                    self.screen_main.blit(
                        pygame.font.Font(None, int(26 * self.size_cof)).render(sls[i], True, (255, 0, 0)),
                        (self.sprite_province_info.rect.x + 20 * self.size_cof,
                         self.sprite_province_info.rect.y + 30 * self.size_cof + (i * 20 * self.size_cof)))
                self.screen_main.blit(
                    pygame.font.Font(None, int(32 * self.size_cof)).render(self.selected_map_sprite.name, True,
                                                                           (255, 0, 0)),
                    (self.sprite_province_info.rect.x + 200 * self.size_cof,
                     self.sprite_province_info.rect.y + 10 * self.size_cof))  # вывести название региона
                index_x = 0  # индекс смещения иконок по x и y соответственно
                for el in self.selected_map_sprite.town_list:
                    for img in self.sls_img_1:
                        self.screen_main.blit(pygame.transform.scale(img, (  # отображение иконок местности...
                            int(img.get_size()[0] * self.size_cof), int(img.get_size()[1] * self.size_cof))), (
                                                  self.sprite_province_info.rect.x + 10 * self.size_cof + index_x * 62 * self.size_cof,
                                                  self.sprite_province_info.rect.y + 210 * self.size_cof))
                    for img in self.sls_img_3:
                        self.screen_main.blit(pygame.transform.scale(img, (  # отображение иконок местности...
                            int(img.get_size()[0] * self.size_cof), int(img.get_size()[1] * self.size_cof))), (
                                                  self.sprite_province_info.rect.x + 10 * self.size_cof + index_x * 62 * self.size_cof,
                                                  self.sprite_province_info.rect.y + 190 * self.size_cof))
                    for i in range(len(self.selected_map_sprite.town_list[el][0])):
                        # img = load_image(
                        #     os.path.join("bildings_icons", self.selected_map_sprite.town_list[el][0][i]) + '.png',
                        #     self.screen_main)
                        for img_ in self.sls_img_2:
                            self.screen_main.blit(pygame.transform.scale(img_, (  # отображение иконок зданий...
                                int(img_.get_size()[0] * self.size_cof), int(img_.get_size()[1] * self.size_cof))), (
                                                      self.sprite_province_info.rect.x + 10 * self.size_cof + index_x * 62 * self.size_cof,
                                                      self.sprite_province_info.rect.y + 210 * self.size_cof + (
                                                              i + 1) * 60 * self.size_cof))

                    index_x += 1
                for img in range(len(self.sls_img_4)):  # отрисовка изображений починки\уничтожения инфраструктуры
                    self.screen_main.blit(pygame.transform.scale(self.sls_img_4[img], (
                        int(self.sls_img_4[img].get_size()[0] * self.size_cof),
                        int(self.sls_img_4[img].get_size()[1] * self.size_cof))), (
                                              self.sprite_province_info.rect.x + 8 * self.size_cof + img *
                                              31 * self.size_cof,
                                              self.sprite_province_info.rect.y + 150 * self.size_cof))

    def restore_destroy(self, event):  # Т.к. кнопки ремонта\уничтожения построек это изображения
        # (их количество изменчиво, нельзя знать заранее сколько спрйтов придется создать),
        # то проверка нажатия на них проверяется постоянно если self.sprite_province_info.visible == True
        if self.sprite_province_info.visible:
            if event.type == pygame.MOUSEBUTTONDOWN:
                cell_x = ((pygame.mouse.get_pos()[0] - self.sprite_province_info.rect.x + 8 * self.size_cof) // 25)
                cell_x = cell_x if 1 <= cell_x <= len(self.sls_img_4) else -1
                print(cell_x)

    def change_settings(self, settings_change):  # изменение настроек
        self.running_2 = False
        self.fps = int(settings_change[0])
        self.size_cof = int(settings_change[3][0]) / self.main_size[1]
        self.sprite_change_size()
        self.fake__init__()

    def sprite_change_size(self):  # изменение размеров и положения спрайтов (аналогично sprite_change_size из main.py)
        for i in [self.special_sprite_list, [self.sprite_province_info, self.sprite_country_info],
                  self.interface_sprite_list, self.menus_sprite_list1, self.sprite_map_list,
                  self.interface_sprite_list_2, self.political_interface]:
            for spr_ in i:
                spr_.rect.x = spr_.rect_x_start * self.size_cof
                spr_.rect.y = spr_.rect_y_start * self.size_cof
                spr_.rect[2] = spr_.image_copy.get_size()[0] * self.size_cof
                spr_.rect[3] = spr_.image_copy.get_size()[1] * self.size_cof
                spr_.image = pygame.transform.scale(spr_.image_copy, (
                    spr_.image_copy.get_size()[0] * self.size_cof,
                    spr_.image_copy.get_size()[1] * self.size_cof))
        for region in self.sprite_map_list:
            for holder in self.country_list:
                if region.holder == holder.name:
                    region.update(holder.color.split("."), self.size_cof)

    def game_break(self):
        self.running_2 = False
        self.stop()
        for i in self.interface_sprite_list_2:
            i.visible = False

    def leave_game(self):  # открытие окна о завершении работы
        for i in self.interface_sprite_list_2:
            i.visible = not i.visible
        self.open_country_political(False)
        # open_settings(True)

    def close_leave_menu(self):  # закрытие окна о завершении работы (на крестик)
        for i in self.interface_sprite_list_2:
            i.visible = False

    def up_tax_1(self):  # увеличение походного налога с физ лиц
        if self.player.income_tax_1 + 1 <= 100: self.player.income_tax_1 += 1

    def down_tax_1(self):  # уменьшение подходного налога с физ лиц
        if self.player.income_tax_1 - 1 >= 0: self.player.income_tax_1 -= 1

    def up_tax_2(self):  # увеличение подоходного налога с компаний
        if self.player.income_tax_2 + 1 <= 100: self.player.income_tax_2 += 1

    def down_tax_2(self):  # уменьшение подоходного налога с компаний
        if self.player.income_tax_2 - 1 >= 0: self.player.income_tax_2 -= 1

    def render_interface(self):  # функция для отображения спрайтов интерфейса
        for i in [self.interface_sprite_list, self.menus_sprite_list1, self.interface_sprite_list_2,
                  self.political_interface]:
            for spr_ in i:
                if spr_.visible:
                    self.group_interface.add(spr_)
                elif not spr_.visible and spr_ in self.group_interface:
                    self.group_interface.remove(spr_)
        self.group_interface.draw(self.screen_main)

    def draw_player_interface(self, event):  # отображение интерфейса игрока (экономические законы)
        all_population = 0
        mobilisation = 0
        cell_x, call_y = -1, -1
        for i in self.sprite_map_list:
            if i.id in self.player.control_id:
                all_population += int(i.population)
        # self.screen_main.blit(
        #     pygame.font.Font(None, int(40 * self.size_cof)).render(str(all_population), True, (255, 0, 0)),
        #     (self.top_panel.rect.x + 250 * self.size_cof, self.top_panel.rect.y + 20 * self.size_cof))
        self.screen_main.blit(
            pygame.font.Font(None, int(40 * self.size_cof)).render(str(self.player.money), True, (255, 0, 0)),
            (self.top_panel.rect.x + 300 * self.size_cof, self.top_panel.rect.y + 20 * self.size_cof))
        self.screen_main.blit(
            pygame.font.Font(None, int(40 * self.size_cof)).render(str(self.player.duty), True, (255, 0, 0)),
            (self.top_panel.rect.x + 300 * self.size_cof, self.top_panel.rect.y + 60 * self.size_cof))
        if self.country_political.visible:
            sls = [self.player.health_costs, self.player.army_costs, self.player.political_costs,
                   self.player.education_costs, self.player.finansical_costs, self.player.police_costs]
            for i in range(1, 7):
                for m in range(13):
                    pygame.draw.rect(self.screen_main, (200, 200, 200) if m <= sls[i - 1] else (100, 50, 100), (
                        90 * self.size_cof + (30 * m * self.size_cof),
                        120 + (i * 50 * self.size_cof),
                        20 * self.size_cof, 40 * self.size_cof))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and self.country_political.rect.collidepoint(event.pos):
                    cell_x = ((pygame.mouse.get_pos()[0] - 90 * self.size_cof) // 30)
                    call_y = ((pygame.mouse.get_pos()[1] - 120 * self.size_cof) // 50) - 1
            if call_y > -1 and cell_x > -1 and call_y <= 5 and cell_x <= 13:
                if call_y == 0: self.player.health_costs = cell_x
                if call_y == 1: self.player.army_costs = cell_x
                if call_y == 2: self.player.political_costs = cell_x
                if call_y == 3: self.player.education_costs = cell_x
                if call_y == 4: self.player.finansical_costs = cell_x
                if call_y == 5: self.player.police_costs = cell_x
            self.screen_main.blit(
                pygame.font.Font(None, int(40 * self.size_cof)).render(str(self.player.income_tax_1), True,
                                                                       (255, 0, 0)),
                (self.country_political.rect.x + 100 * self.size_cof,
                 self.country_political.rect.y + 410 * self.size_cof))
            self.screen_main.blit(
                pygame.font.Font(None, int(40 * self.size_cof)).render(str(self.player.income_tax_2), True,
                                                                       (255, 0, 0)),
                (self.country_political.rect.x + 100 * self.size_cof,
                 self.country_political.rect.y + 450 * self.size_cof))

    def main_render(self):  # функция с игровым циклом
        clock = pygame.time.Clock()
        while self.running_2:
            clock.tick(self.fps)
            events = pygame.event.get()
            for event in events:
                self.restore_destroy(event)
                setting_event(event)
                if event.type == pygame.QUIT:
                    self.leave_game()
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.flag_move_1 = False
                if event.type == pygame.MOUSEBUTTONDOWN:
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
                    for sprit in self.sprite_map_list:  # проверка нажатия на ргион
                        pos_in_mask = event.pos[0] - sprit.rect.x, event.pos[1] - sprit.rect.y
                        if sprit.rect.collidepoint(event.pos) and sprit.mask.get_at(pos_in_mask) and len(
                                [s for s in self.special_sprite_list if
                                 s.rect.collidepoint(pygame.mouse.get_pos()) and s.visible]) == 0 and (
                                False if self.country_political.visible and self.country_political.rect.collidepoint(
                                    event.pos) else True):
                            if pygame.mouse.get_pressed()[0]:  # проверка, что была нажата левая клавиша мыши
                                function_call = self.functions[sprit.function]  # вызов функции по атрибуту function
                                function_call(True, sprit)  # который передается как ключ в словарь функций functions
                            elif pygame.mouse.get_pressed()[2]:  # проверка, что была нажата левая клавиша мыши
                                function_call = self.functions[
                                    sprit.function + '_2']  # вызов функции по атрибуту function
                                function_call(True, sprit)  # который передается как ключ в словарь функций functions
                    for i in [self.menus_sprite_list1, self.interface_sprite_list, self.interface_sprite_list_2,
                              self.political_interface]:
                        for sprit_2 in i:
                            if sprit_2.rect.collidepoint(pygame.mouse.get_pos()) and sprit_2.visible:
                                if pygame.mouse.get_pressed()[0]:
                                    if sprit_2.function[0:4] == 'dept':
                                        self.dept_change(int(sprit_2.function[4:]))
                                    elif sprit_2.function != '':
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
            self.draw_player_interface(event)
            settings_change = apply_settings(False)
            if not settings_change is None: self.change_settings(settings_change)
            render_setting(self.screen_main)
            pygame.display.update()

    def stop(self):  # при закрытии не переходить к начальному окну
        self.next_window = False

    def save_game_file(self):  # запись параметров текущей игры в файл
        pass
