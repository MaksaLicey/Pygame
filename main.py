from Main_Game_File import *
from special import *
from setting_file import render_setting, open_settings, setting_event, apply_settings


# файл для работы со стартовым меню

class StartMenu:  # класс запуска меню
    def __init__(self):
        self.game_size = 1536, 800  # основной размер окна игры (чтоб рассчитать коэффициент изменения размера)
        #  (основой размер окна меню 1100 * 700)
        file = open(os.path.join("data", "settings", "setting_file"))
        settings = file.readlines()  # считывание настроек с файла data\settings\setting_file
        self.fps = int(settings[0])  # получение ограничения фпс
        self.size_cof = int(settings[3].split()[0]) / self.game_size[1]  # коэффициент изменения размеров
        file.close()

        self.image_for_menu = None  # изображения заднего фона меню
        self.image_for_menu_copy = None  # его копия (для нормального изменения размера)
        self.screen = None  # нужно для того, чтобы после завершения работы всех функций класса
        self.create_window()  # после повторного вызова не пришлось заново объявлять параметры окна

        # объявление спрайтов меню, экземпляров класса SpriteCreate, из special.py
        self.sprite_play_btn = MenySpriteCreate(self.screen, 320, 30,
                                                "btn_GamePlay.png", True, 'open_start_menu')
        self.sprite_leave_game = MenySpriteCreate(self.screen, 320, 200,
                                                  "leave_game.png", True, 'stop')
        self.sprite_open_setting = MenySpriteCreate(self.screen, 950, 90, "setting_btn_img.png", True, 'open_setting')
        self.sprite_start_menu = MenySpriteCreate(self.screen, 80, 50, "start_menu.png", False)
        self.sprite_start_afrika = MenySpriteCreate(self.screen, self.sprite_start_menu.rect.x + 30,
                                                    self.sprite_start_menu.rect.y + 70, "Afrika.png", False,
                                                    'edit_selected_spr_1', 'prompt_1.png')
        self.sprite_start_europe = MenySpriteCreate(self.screen, self.sprite_start_menu.rect.x + 280,
                                                    self.sprite_start_menu.rect.y + 70,
                                                    "europe.png", False, 'edit_selected_spr_1', 'prompt_1.png')
        self.sprite_start_latina = MenySpriteCreate(self.screen, self.sprite_start_menu.rect.x + 490,
                                                    self.sprite_start_menu.rect.y + 70,
                                                    "Latina.png",
                                                    False, 'edit_selected_spr_1', 'prompt_latina.png')
        self.sprite_start_america = MenySpriteCreate(self.screen, self.sprite_start_menu.rect.x + 650,
                                                     self.sprite_start_menu.rect.y + 60, "America.png",
                                                     False, 'edit_selected_spr_1', 'prompt_1.png')
        self.sprite_game_diff_1 = MenySpriteCreate(self.screen, self.sprite_start_menu.rect.x + 70,
                                                   self.sprite_start_menu.rect.y + 320, "game_difficutly_1.png",
                                                   False, 'edit_selected_spr_2', 'prompt_difficutly_1.png')
        self.sprite_game_diff_2 = MenySpriteCreate(self.screen, self.sprite_start_menu.rect.x + 270,
                                                   self.sprite_start_menu.rect.y + 320, "game_difficutly_2.png",
                                                   False, 'edit_selected_spr_2', 'prompt_difficutly_2.png')
        self.sprite_game_diff_3 = MenySpriteCreate(self.screen, self.sprite_start_menu.rect.x + 470,
                                                   self.sprite_start_menu.rect.y + 320,
                                                   "game_difficutly_3.png",
                                                   False, 'edit_selected_spr_2', 'prompt_difficutly_3.png')
        self.sprite_game_diff_4 = MenySpriteCreate(self.screen, self.sprite_start_menu.rect.x + 670,
                                                   self.sprite_start_menu.rect.y + 320, "game_difficutly_4.png",
                                                   False, 'edit_selected_spr_2', 'prompt_difficutly_4.png')
        self.sprite_character_1 = MenySpriteCreate(self.screen, self.sprite_start_menu.rect.x + 100,
                                                   self.sprite_start_menu.rect.y + 400, "character_1.png",
                                                   False, 'edit_selected_spr_3', 'prompt_character_1.png')
        self.sprite_character_2 = MenySpriteCreate(self.screen, self.sprite_start_menu.rect.x + 300,
                                                   self.sprite_start_menu.rect.y + 400,
                                                   "character_2.png",
                                                   False, 'edit_selected_spr_3', 'prompt_character_2.png')
        self.sprite_character_3 = MenySpriteCreate(self.screen, self.sprite_start_menu.rect.x + 500,
                                                   self.sprite_start_menu.rect.y + 400,
                                                   "character_3.png", False, 'edit_selected_spr_3',
                                                   'prompt_character_3.png')
        self.sprite_character_4 = MenySpriteCreate(self.screen, self.sprite_start_menu.rect.x + 700,
                                                   self.sprite_start_menu.rect.y + 400, "character_4.png",
                                                   False, 'edit_selected_spr_3', 'prompt_character_4.png')
        self.sprite_start_game = MenySpriteCreate(self.screen, self.sprite_start_menu.rect.x + 350,
                                                  self.sprite_start_menu.rect.y + 500,
                                                  "btn_start_game.png", False, 'open_list')
        self.sprite_file_menu = MenySpriteCreate(self.screen, self.sprite_start_menu.rect.x + 320,
                                                 self.sprite_start_menu.rect.y + 180, "file_list.png", False)
        self.sprite_up_list = MenySpriteCreate(self.screen, self.sprite_file_menu.rect.x + 20,
                                               self.sprite_file_menu.rect.y + 200, "up_list.png", False, 'up_list')
        self.sprite_down_list = MenySpriteCreate(self.screen, self.sprite_file_menu.rect.x + 60,
                                                 self.sprite_file_menu.rect.y + 200, "down_list.png",
                                                 False, 'down_list')
        self.sprite_input_name_file = MenySpriteCreate(self.screen, self.sprite_file_menu.rect.x + 20,
                                                       self.sprite_file_menu.rect.y + 240,
                                                       "input_name_file.png", False, 'start_input_file_name', '')
        self.sprite_crete_file = MenySpriteCreate(self.screen, self.sprite_file_menu.rect.x + 30,
                                                  self.sprite_file_menu.rect.y + 290, "create_file.png",
                                                  False, 'create_file_and_start')
        self.sprite_file_name_mistake = MenySpriteCreate(self.screen, self.sprite_file_menu.rect.x - 100,
                                                         self.sprite_file_menu.rect.y - 140, "file_name_mistake.png",
                                                         False, 'file_name_mistake')
        self.sprite_file_name_mistake2 = MenySpriteCreate(self.screen, self.sprite_file_menu.rect.x - 70, 20,
                                                          "file_name_mistake2.png",
                                                          False, 'file_name_mistake2')
        self.sprite_file_name_mistake2 = MenySpriteCreate(self.screen, self.sprite_file_menu.rect.x - 70, 20,
                                                          "file_name_mistake2.png",
                                                          False, '')
        # "глобальные" атрибуты для класса
        self.clicked_sprites = []  # список нажатых спрайтов
        self.selected = False  # переменные, определяющие выбран ли спрайт
        self.selected_2 = False  # в каждой строке (карты, сложность, стартовый
        self.selected_3 = False  # персонаж
        self.selected_sprite_1 = None  # спрайты, далее использующиеся как копии выбранных спрайтов
        self.selected_sprite_2 = None  # из каждой группы выбора стартовых настроек (карта, сложность, лидер)
        self.selected_sprite_3 = None
        self.text_input_active = False  # переменная для начала записи названия нового файла
        self.err1 = None  # сообщение об ошибке при создании нового файла
        self.text_file_name = ''  # строка для хранения введенного названия файла
        self.running = True  # пока True: выполняется цикл игры
        self.next_window = False  # если переменная True, начнется выполнение функции main_render другого класса
        self.prompt_image = None
        self.prompt_image_path = None

        # общий список спрайтов меню, хранит спрайты, которые не относятся к другим списка спрайтов
        self.other_menu_sprites = [self.sprite_play_btn, self.sprite_open_setting, self.sprite_leave_game]
        self.list_error_sprite = [self.sprite_file_name_mistake, self.sprite_file_name_mistake2]
        # список спрайтов меню подготовки к началу игры
        self.start_menu_sprites = [self.sprite_start_menu, self.sprite_start_afrika, self.sprite_start_europe,
                                   self.sprite_start_latina, self.sprite_start_america, self.sprite_game_diff_1,
                                   self.sprite_game_diff_2, self.sprite_game_diff_3,
                                   self.sprite_game_diff_4, self.sprite_character_1, self.sprite_character_2,
                                   self.sprite_character_3, self.sprite_character_4, self.sprite_start_game]
        # список спрайтов, связанных с отображением списка файлов и вводом имени нового файла
        self.file_list_sprites = [self.sprite_file_menu, self.sprite_up_list, self.sprite_down_list,
                                  self.sprite_input_name_file, self.sprite_crete_file]

        self.group_visible_sprite = pygame.sprite.Group()  # группа для хранения видимых спрайтов,
        # Единственная для всех спрайтов меню. В цикле игры наполняется спрайтами, у которых visible = True
        self.func_dictionary = {  # словарь функций спрайтов
            "file_name_mistake": self.file_name_mistake,  # закрытие сообщения об ошибке (файл с таким же именем)
            "file_name_mistake2": self.file_name_mistake2,
            # закрытие сообщения об иных ошибках (недопустимые символы в названии файла, не найдем файл карты и тд)
            "create_file_and_start": self.create_file_and_start,  # если все хорошо создаться файл и откроется игра
            "start_input_file_name": self.start_input_file_name,  # начала\конец ввода имени файла
            "up_list": self.up_list,  # пролистать список файлов вверх
            "down_list": self.down_list,  # пролистать список файлов вниз
            "open_list": self.open_list,  # открытие окна создания файла
            "edit_selected_spr_1": self.edit_selected_spr_1,  # изменение выбранного спрайта карты
            "edit_selected_spr_2": self.edit_selected_spr_2,  # изменение выбранного спрайта сложности
            "edit_selected_spr_3": self.edit_selected_spr_3,  # изменение выбранного спрайта лидера
            "open_start_menu": self.open_start_menu,  # открытие меню начальных параметров игры
            "open_setting": open_settings,  # открытие настроек (функция из special_2.py)
            "stop": self.leave_game

        }
        self.sprite_change_size()  # изменение спрайтов с учетом size_cof
        self.main_render()  # запуск функции с циклом игры

    def create_window(self):  # задание параметров окна
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200, 50)  # задание стартового положения окна
        pygame.init()
        pygame.mixer.init()

        # pygame.mixer.music.load(os.path.join("sounds", "shtil-orkestr-vagner.mp3"))
        # pygame.mixer.music.play()
        # pygame.mixer.music.set_volume(0.1)

        size_menu = 1100 * self.size_cof, 700 * self.size_cof  # размер окна меню
        self.screen = pygame.display.set_mode(size_menu)
        self.image_for_menu = load_image("test1.png", self.screen)
        self.image_for_menu_copy = self.image_for_menu
        self.image_for_menu = pygame.transform.scale(self.image_for_menu_copy, (
            self.image_for_menu_copy.get_size()[0] * self.size_cof,
            self.image_for_menu_copy.get_size()[1] * self.size_cof))
        image_for_icon = load_image("icon_for_game.png", self.screen)  # изображение для иконки приложения
        pygame.display.set_icon(image_for_icon)
        pygame.display.set_caption('The final strike')  # название приложения

    def fake__init__(self):  # запуск приложения без новой инициализации
        pygame.quit()
        for i in [self.start_menu_sprites, self.file_list_sprites, self.file_list_sprites]:
            for spr_ in i:
                spr_.visible = False
        self.running = True
        self.text_file_name = ''
        self.create_window()
        self.main_render()

    def change_settings(self, sls):  # смена настроек
        self.running = False
        self.fps = int(sls[0])

        self.size_cof = int(sls[3][0]) / self.game_size[1]
        self.sprite_change_size()
        self.fake__init__()

    def sprite_change_size(self):  # умножение положения спрайтов на size_cof
        #  и замена текущих изображений на копии начальных с изменением размера на size_cof
        for i in [self.other_menu_sprites, self.list_error_sprite, self.start_menu_sprites, self.file_list_sprites]:
            for sprit_s in i:
                sprit_s.rect.x = sprit_s.rect_x_start * self.size_cof
                sprit_s.rect.y = sprit_s.rect_y_start * self.size_cof
                sprit_s.rect[2] = sprit_s.image_copy.get_size()[0] * self.size_cof
                sprit_s.rect[3] = sprit_s.image_copy.get_size()[1] * self.size_cof
                sprit_s.image = pygame.transform.scale(sprit_s.image_copy, (
                    sprit_s.image_copy.get_size()[0] * self.size_cof,
                    sprit_s.image_copy.get_size()[1] * self.size_cof))

    def file_name_mistake(self):  # закрыть окно ошибки "файл с таким именем уже есть"
        if self.clicked_sprites[-1].function == "file_name_mistake":
            self.sprite_file_name_mistake.visible = False

    def file_name_mistake2(self):  # закрыть окно о прочих ошибках
        if self.clicked_sprites[-1].function == "file_name_mistake2":
            self.sprite_file_name_mistake2.visible = False

    def start_input_file_name(self):  # начала\конец ввода имени файла
        if self.clicked_sprites[-1].function == "start_input_file_name":
            self.text_input_active = not self.text_input_active

    def down_list(self):  # пролистать список файлов вниз
        if self.clicked_sprites[-1].function == 'down_list':
            get_files_list(1)

    def up_list(self):  # пролистать список файлов вверх
        if self.clicked_sprites[-1].function == 'up_list':
            get_files_list(-1)

    def open_list(self):  # открытие окна создания файла
        if (self.clicked_sprites[-1].function == 'open_list' and not self.selected_sprite_1 is None and
                not self.selected_sprite_2 is None and not self.selected_sprite_3 is None):
            self.list_file_menu()

    def open_start_menu(self, flag=True):  # открытие меню стартовых настроек
        for spr in self.start_menu_sprites:
            spr.visible = not spr.visible if flag else False
        if not self.sprite_start_menu.visible:
            self.list_file_menu()

    def list_file_menu(self):  # отображение спрайтов меню
        for spr in self.file_list_sprites:
            spr.visible = not spr.visible if self.sprite_start_menu.visible else False
        if not self.sprite_file_menu.visible:
            self.sprite_file_name_mistake.visible = self.sprite_file_menu.visible
            self.sprite_file_name_mistake2.visible = self.sprite_file_menu.visible

    def edit_selected_spr_1(self):  # изменение выбранного спрайта карты
        if not self.sprite_file_menu.visible:
            if self.clicked_sprites[-1] != self.selected_sprite_1:
                self.selected_sprite_1 = self.clicked_sprites[-1]
                self.selected = True
            else:
                self.selected_sprite_1 = None
                self.selected = False

    def edit_selected_spr_2(self):  # изменение выбранного спрайта сложности
        if self.clicked_sprites[-1].function == 'edit_selected_spr_2' and not self.sprite_file_menu.visible:
            if self.clicked_sprites[-1] != self.selected_sprite_2:
                self.selected_sprite_2 = self.clicked_sprites[-1]
                self.selected_2 = True
            else:
                self.selected_sprite_2 = None
                self.selected_2 = False

    def edit_selected_spr_3(self):  # изменение выбранного спрайта лидера
        if self.clicked_sprites[-1].function == 'edit_selected_spr_3' and not self.sprite_file_menu.visible:
            if self.clicked_sprites[-1] != self.selected_sprite_3:
                self.selected_sprite_3 = self.clicked_sprites[-1]
                self.selected_3 = True
            else:
                self.selected_sprite_3 = None
                self.selected_3 = False

    # Далее функции draw_... , просто, чтоб цикл был более читабельным
    def draw_selected(self):  # отображение выделения спрайтов начальных параметров
        if self.selected and self.sprite_start_menu.visible and not self.sprite_file_menu.visible:
            if len(self.clicked_sprites) > 0:
                if self.selected_sprite_1.function == 'edit_selected_spr_1':
                    pygame.draw.rect(self.screen, (255, 0, 0), (
                        self.selected_sprite_1.rect[0] - 15 * self.size_cof,
                        self.selected_sprite_1.rect[1] - 15 * self.size_cof,
                        self.selected_sprite_1.rect[2] + 30 * self.size_cof,
                        self.selected_sprite_1.rect[3] + 30 * self.size_cof),
                                     width=round(5 * self.size_cof))
        if self.selected_2 and self.sprite_start_menu.visible and not self.sprite_file_menu.visible:
            if len(self.clicked_sprites) > 0:
                if self.selected_sprite_2.function == 'edit_selected_spr_2':
                    pygame.draw.rect(self.screen, (0, 255, 0), (
                        self.selected_sprite_2.rect[0], self.selected_sprite_2.rect[1],
                        self.selected_sprite_2.rect[2],
                        self.selected_sprite_2.rect[3]), width=round(5 * self.size_cof))
        if self.selected_3 and self.sprite_start_menu.visible and not self.sprite_file_menu.visible:
            if len(self.clicked_sprites) > 0:
                if self.selected_sprite_3.function == 'edit_selected_spr_3':
                    pygame.draw.rect(self.screen, (0, 0, 255), (
                        self.selected_sprite_3.rect.x, self.selected_sprite_3.rect.y,
                        self.selected_sprite_3.image.get_size()[0],
                        self.selected_sprite_3.image.get_size()[1]), width=round(5 * self.size_cof))

    def draw_file_name(self):  # отображение вводимого названия файла
        if self.sprite_input_name_file.visible:
            if self.text_input_active:
                self.screen.fill((200, 100, 100), self.sprite_input_name_file.rect)
                txt_surface = pygame.font.Font(None, round(40 * self.size_cof)).render(self.text_file_name, True,
                                                                                       (70, 195, 150))
                self.screen.blit(txt_surface,
                                 (self.sprite_input_name_file.rect.x + 10 * self.size_cof,
                                  self.sprite_input_name_file.rect.y + 5 * self.size_cof))
            else:
                txt_surface = pygame.font.Font(None, round(40 * self.size_cof)).render(self.text_file_name, True,
                                                                                       (100, 100, 200))
                self.screen.blit(txt_surface,
                                 (self.sprite_input_name_file.rect.x + 10 * self.size_cof,
                                  self.sprite_input_name_file.rect.y + 5 * self.size_cof))

    def draw_list_files(self):  # отрисовка списка файлов сохранений
        if self.sprite_file_menu.visible:
            for i in range(len(get_files_list()[0])):
                txt_surface = pygame.font.Font(None, round(32 * self.size_cof)).render(self.text_file_name, True,
                                                                                       (255, 0, 0))
                max_text_width = 150  # максимальная длинна имени файла
                if txt_surface.get_width() >= max_text_width:  # проверка длины текста
                    for b in range(len(self.text_file_name)):
                        txt_surface = pygame.font.Font(None, round(32 * self.size_cof)).render(self.text_file_name[0:b],
                                                                                               True, (255, 0, 0))
                        if txt_surface.get_width() >= max_text_width:
                            self.text_file_name = self.text_file_name[0:b]
                            break
                self.screen.blit(
                    pygame.font.Font(None, round(32 * self.size_cof)).render(get_files_list()[0][i], True, (255, 0, 0)),
                    (self.sprite_file_menu.rect.x + 20 * self.size_cof,
                     self.sprite_file_menu.rect.y + 20 + (i * 20) * self.size_cof))

    def draw_error_text(self):  # отображение текста ошибки
        if self.sprite_file_name_mistake2.visible:
            self.screen.blit(
                pygame.font.Font(None, round(30 * self.size_cof)).render(str(self.err1), True, (255, 255, 200)),
                (self.sprite_file_name_mistake2.rect.x + 20 * self.size_cof,
                 self.sprite_file_name_mistake2.rect.y + 40 * self.size_cof))

    def main_render(self):
        clock = pygame.time.Clock()
        while self.running:  # основной цикл игры
            clock.tick(self.fps)
            events = pygame.event.get()
            for EVENT in events:
                setting_event(EVENT)  # передача события в обработчике работы с настройками
                if EVENT.type == pygame.QUIT:
                    self.running = False
                if EVENT.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:  # проверка нажатия ЛКМ
                        pos = pygame.mouse.get_pos()
                        self.clicked_sprites = [s for s in self.group_visible_sprite if s.rect.collidepoint(
                            pos)]  # добавление видимых спрайтов, на которых был курсор мыши во время нажатия
                        if len(self.clicked_sprites) > 0:
                            if self.clicked_sprites[-1].function != '':
                                func_call = self.func_dictionary[self.clicked_sprites[-1].function]
                                func_call()  # вызов функции верхнего нажатого спрайта
                if EVENT.type == pygame.KEYDOWN:
                    if self.text_input_active:  # ввод названия файла
                        if EVENT.key == pygame.K_BACKSPACE:
                            self.text_file_name = self.text_file_name[:-1]  # удаление символа на backspace
                        else:
                            if (EVENT.unicode != '\\' and EVENT.unicode != '\r' and EVENT.unicode != 'a\t'
                                    and EVENT.unicode != '\x1b'):  # '/' '|'  '*'
                                self.text_file_name += EVENT.unicode
                    if EVENT.key == pygame.K_ESCAPE:
                        if self.sprite_file_menu.visible:
                            self.list_file_menu()  # закрытие меню создания файла на esc
                        else:
                            if not self.file_list_sprites[0].visible:
                                self.open_start_menu(False)

            for s in [self.other_menu_sprites, self.start_menu_sprites, self.file_list_sprites, self.list_error_sprite]:
                for sprit in s:  # проход по всем спрайтов всех списков
                    if sprit.visible and sprit:
                        self.group_visible_sprite.add(sprit)  # добавление видимых спрайтов в группу
                    elif sprit in self.group_visible_sprite:  # удаление из группы, если visible == False
                        self.group_visible_sprite.remove(sprit)
            if not self.running: break  # на всякий случай
            self.screen.blit(self.image_for_menu, (0, 0))  # отрисовка изображения фона
            self.group_visible_sprite.draw(self.screen)  # отображение видимых спрайтов
            self.draw_selected()  # отображение выделения спрайтов карты, сложности и лидера

            self.draw_list_files()
            self.draw_error_text()
            if EVENT.type == pygame.MOUSEMOTION:  # события при передвижении курсора
                pos = pygame.mouse.get_pos()
                clicked_sprites_2 = [s for s in self.group_visible_sprite if s.rect.collidepoint(pos)]
                # добавление спрайтов, на которых попал курсор мыши в список
                if len(clicked_sprites_2) > 0:  # ну и отображение подсказки, если таковая есть
                    if clicked_sprites_2[
                        -1].prompt != '' and not self.sprite_file_menu.visible and self.prompt_image_path != \
                            clicked_sprites_2[-1].prompt:
                        self.prompt_image_path = clicked_sprites_2[-1].prompt
                        img_ = load_image(clicked_sprites_2[-1].prompt, self.screen)
                        self.prompt_image = pygame.transform.scale(img_, (
                        img_.get_size()[0] * self.size_cof, img_.get_size()[1] * self.size_cof))
                    if not self.prompt_image is None and clicked_sprites_2[-1].prompt != '': self.screen.blit(
                        self.prompt_image, pos)
            self.draw_file_name()

            settings_change = apply_settings(False)  # запрос об изменении настроек
            if not settings_change is None: self.change_settings(settings_change)
            if self.running:
                render_setting(self.screen)  # отображение окна настроек
                pygame.display.update()

    def create_file_and_start(self):  # если все хорошо создаться файл и откроется игра
        if self.clicked_sprites[-1].function == "create_file_and_start" and self.text_file_name != "":
            if self.text_file_name in get_files_list()[1]:
                self.sprite_file_name_mistake.visible = True
            else:
                if open_settings(True) != "error":  # закрытие настроек при переходе в игре
                    self.err1 = self.create_file()
                    if self.err1 is None:
                        self.running = False
                        self.next_window = True
                    else:
                        # self.err1 = None
                        self.sprite_file_name_mistake2.visible = True

    def create_file(self):  # получаем параметры игры
        global file_name
        try:
            file_game = open(os.path.join("saves", self.text_file_name), mode="w",
                             encoding="utf-8")  # создаем новый файл
            file_game.write(f"file_name = {self.text_file_name}" + "\n")  # записываем в него все стартовые параметры
            file_game.write(f"map_name = {self.selected_sprite_1.prompt[7:-4]}" + "\n")
            file_game.write(f"difficult = {self.selected_sprite_2.prompt[7:-4]} \n")
            file_game.write(f"leader = {self.selected_sprite_3.prompt[7:-4]} \n")
            file_game.write(f"time = 1.1.2030 \n")
            f = open(os.path.join('starts_file', f'{self.selected_sprite_1.prompt[7:-4]}.txt'), 'r+', encoding="utf-8")
            # открываем файл, в соответствии с выбранной картой
            sls = f.readlines()
            for i in sls:
                file_game.write(i)  # переписываем его содержимое в недавно созданный файл
            f.close()
            file_game.close()
            file_name = self.text_file_name
            pygame.quit()
            return None
        except Exception as e:
            return e

    def stop(self):  # если next_window == False, приложение окна завершает работу р
        self.next_window = False  # не переходя к следующему окну

    def leave_game(self):
        self.running = False


def main():  # при действиях игрока запускает окно меню и игры поочередно
    app1 = StartMenu()
    app2 = None
    while True:
        if app1.next_window:
            if app2 is None:
                app2 = MainGameClass(file_name)
            else:
                app2.fake__init__()
            app1.stop()
        if not (app2 is None):
            if app2.next_window:
                app1.fake__init__()
                app2.stop()
            elif not app1.next_window and not app2.next_window:
                print("работа завершена в штатном режиме")
                break  # полное завершение работы
        else:
            print("работа завершена в штатном режиме")
            break
    pygame.quit()


if __name__ == "__main__":
    file_name = ''  # решил оставить имя файла глобальное переменной
    main()  # запуск приложения
#