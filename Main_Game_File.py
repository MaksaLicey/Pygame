import pygame

from special import *
from special_2 import render_setting, open_settings, setting_event


# главный файл игры

def create_file(name_file, start_option_1, start_option_2, start_option_3):  # получаем параметры игры
    file_game = open(os.path.join("saves", name_file), mode="w", encoding="utf-8")  # создаем новый файл
    # except
    file_game.write(f"file_name = {name_file}" + "\n")  # записываем в него все стартовые параметры
    file_game.write(f"map_name = {start_option_1[7:-4]}" + "\n")
    file_game.write(f"difficult = {start_option_2[7:-4]} \n")
    file_game.write(f"leader = {start_option_3[7:-4]} \n")
    file_game.write(f"time = 1.1.2030.00.00 \n")
    f = open(os.path.join('starts_file', f'{start_option_1[7:-4]}.txt'), 'r+', encoding="utf-8")
    # открываем файл, в соответствии с выбранной картой
    sls = f.readlines()
    for i in sls:
        file_game.write(i)  # переписываем его содержимое в недавно созданный файл
    f.close()
    file_game.close()
    pygame.quit()
    main(name_file)


def render(file_name):
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 30)

    pygame.init()

    size_menu = 1536, 803  # размер окна
    screen_main = pygame.display.set_mode(size_menu)
    image_for_icon = load_image("icon_for_game.png")  # изображение для иконки приложения
    pygame.display.set_icon(image_for_icon)
    pygame.display.set_caption('The final strike')  # название приложения

    sprite_province_info = GameSprite(500, 10, os.path.join("game_sprites", "province_info.png"), False,
                                      "move_region_menu")  # спрайт взаимодействия с регионом
    sprite_country_info = GameSprite(500, 500, os.path.join("game_sprites", "country_info.png"), False,
                                     "move_region_menu")  # спрайт для взаимодействия с регионом

    sprite_open_menu = GameSprite(1400, 10, os.path.join("game_sprites", "menu_game.png"), True, "menu_click")
    top_panel = GameSprite(0, 0, os.path.join("game_sprites", "top_panel.png"), True, "")

    special_sprite_list = [sprite_province_info,
                           sprite_country_info]  # список для определенных спрайтов(меню региона, меню владельца)
    single_group_1 = pygame.sprite.GroupSingle(sprite_province_info)  # одиночная группа для sprite_province_info
    single_group_2 = pygame.sprite.GroupSingle(sprite_country_info)  # одиночная группа для sprite_country_info
    interface_sprite_list = [top_panel, sprite_open_menu]  # лист для спрайтов интерфейса
    group_interface = pygame.sprite.Group()  # и группа для них
    group_buildings_icons = pygame.sprite.Group()  # группа для иконок при отображении информации о регионе

    info_list_from_file = file_reader(file_name)  # получение информации из файла
    sprite_map_list = info_list_from_file[0]  # список спрайтов карты
    group_map_sprite = pygame.sprite.Group()  # и группа спрайтов для них
    file_info_list = info_list_from_file[1]  # список с информацией об игре (время, сложность и тд)
    country_list = info_list_from_file[2]  # список стран (возможных владельцев)

    sprite_move_now = special_sprite_list[0]
    flag_move_1 = False  # флаг перемещения спрайта взаимодействия с регионом
    mouse_start = 0, 0  # позиции мыши в начале перемещения
    click_r_1 = False  # флаг (если выключен, спрайт не сможет выйти за границы экрана)

    for sprite_ in sprite_map_list:  # добавление всех спрайтов карты в группу group_map_sprite
        group_map_sprite.add(sprite_)

    def move_region_menu(flag, mouse_start_pos, flag2=False):  # функция для перемещения спрайта
        delta_x = pygame.mouse.get_pos()[0] - mouse_start_pos[0]  # изменение координат по x
        delta_y = pygame.mouse.get_pos()[1] - mouse_start_pos[1]  # изменение координат по y
        if flag:  # True, если левая кнопка мыши зажата на спрайте
            sprite_move_now.rect.x = delta_x
            sprite_move_now.rect.y = delta_y
        if sprite_move_now.rect.y + sprite_move_now.rect[2] - 450 > size_menu[1]:
            sprite_move_now.rect.y -= 3
        elif sprite_move_now.rect.y < -350:
            sprite_move_now.rect.y += 3
        if sprite_move_now.rect.x > size_menu[0] - 50:
            sprite_move_now.rect.x -= 3
        elif sprite_move_now.rect.x + sprite_move_now.rect[3] < -50:
            sprite_move_now.rect.x += 3
        if flag2:
            if sprite_move_now.rect.y + sprite_move_now.rect[1] > size_menu[1]:
                sprite_move_now.rect.y -= 3
            elif sprite_move_now.rect.y + sprite_move_now.rect[1] < 0:
                sprite_move_now.rect.y += 3
            if sprite_move_now.rect.x + sprite_move_now.rect[2] > size_menu[0]:
                sprite_move_now.rect.x -= 3
            elif sprite_move_now.rect.x < 0:
                sprite_move_now.rect.x += 3

    def render_interface():  # функция для отображения спрайтов интерфейса
        for i in interface_sprite_list:
            if i.visible:
                group_interface.add(i)
            elif not i.visible and i in group_interface:
                group_interface.remove(i)
        group_interface.draw(screen_main)

    def menu_click():  # открытие меню
        open_settings()

    def open_sprite_list_2(flag=False, sprite=''):  # отображения окна государства (вызывается если
        # игрок нажал правой клавишей на регион
        global selected_map_sprite_2
        if flag:
            if sprite != '' and sprite_country_info.visible and selected_map_sprite_2 != sprite:
                selected_map_sprite_2 = sprite
            else:
                selected_map_sprite_2 = sprite
                sprite_country_info.visible = not sprite_country_info.visible
        if sprite_country_info.visible:
            single_group_2.draw(screen_main)
            index = 0
            for i in range(len(country_list)):
                if selected_map_sprite_2.holder == country_list[i].name:
                    index = i
                    break
            if not country_list[index].bot:  # отображение если выбранная страна - игрок (self.bot == False)
                pass
            else:  # отображение окна, если выбранная страна это бот
                pass

    def open_sprite_list(flag=False, sprite=''):  # функция для смены видимости окна и его отображения
        # если передать True и экземпляр нажатого класса SpritesCreateForMap,
        # то выбранный регион изменится на переданный спрайт
        global selected_map_sprite
        if flag:
            if sprite != '' and sprite_province_info.visible and selected_map_sprite != sprite:
                selected_map_sprite = sprite
            else:
                selected_map_sprite = sprite
                sprite_province_info.visible = not sprite_province_info.visible
        else:
            if sprite_province_info.visible:
                single_group_1.draw(screen_main)
                str1 = "население: " + str(selected_map_sprite.population) + "чел."
                str2 = ("поддержка враждебных партий: " + str("%.2f" % (
                        selected_map_sprite.support_government / selected_map_sprite.population * 100)) + "%" + " (" +
                        str(selected_map_sprite.support_government) + ')')
                str3 = "поддержка нашего движения: " + str(
                    "%.2f" % (
                            selected_map_sprite.our_support / selected_map_sprite.population * 100)) + "%" + " (" + str(
                    selected_map_sprite.our_support) + ")"
                sls = [str1, str2, str3]
                for i in range(len(sls)):  # отображение информации о спрайте
                    screen_main.blit(pygame.font.Font(None, 26).render(sls[i], True, (255, 0, 0)),
                                     (sprite_province_info.rect.x + 20,
                                      sprite_province_info.rect.y + 30 + (i * 20)))
                screen_main.blit(pygame.font.Font(None, 32).render(selected_map_sprite.name, True, (255, 0, 0)),
                                 (sprite_province_info.rect.x + 200,
                                  sprite_province_info.rect.y + 10))  # вывести название региона
                index_x = 0  # индекс смещения иконок по x и y соответственно
                for el in selected_map_sprite.town_list:  # цикл для отображения всех построек и местности региона
                    group_buildings_icons.add(GameSprite(sprite_province_info.rect.x + 10 + index_x * 60,
                                                         sprite_province_info.rect.y + 110,
                                                         os.path.join("bildings_icons", el[0:-2]) + '.png'))
                    group_buildings_icons.add(GameSprite(sprite_province_info.rect.x + 10 + index_x * 60,
                                                         sprite_province_info.rect.y + 90,
                                                         os.path.join("bildings_icons",
                                                                      selected_map_sprite.town_list[el][-1]) + '.png'))
                    for i in range(len(selected_map_sprite.town_list[el][0])):
                        group_buildings_icons.add(GameSprite(sprite_province_info.rect.x + 10 + index_x * 60,
                                                             sprite_province_info.rect.y + 110 + (i + 1) * 60,
                                                             os.path.join("bildings_icons",
                                                                          selected_map_sprite.town_list[el][0][
                                                                              i]) + '.png'))
                    index_x += 1
                group_buildings_icons.draw(screen_main)
                for i in group_buildings_icons:  # Очистка
                    group_buildings_icons.remove(i)

    functions = {
        # наконец решил оформить код, исполняемый при нажатии
        # на спрайт в отдельные функции и поместить их в список...
        "open_region_info": open_sprite_list,  # вызывается при нажатии лкм на регион
        "open_region_info_2": open_sprite_list_2,  # вызывается при нажатии пкм на регион
        "move_region_menu": move_region_menu,  # вызывается, если пкм зажата на объекте из special_sprite_list
        "menu_click": menu_click  # вызывается при нажатии special_sprite_list
    }
    clock = pygame.time.Clock()
    running_2 = True
    while running_2:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            setting_event(event)
            if event.type == pygame.QUIT:
                running_2 = False
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_a:
            #         running_2 = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    flag_move_1 = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprit in sprite_map_list:  # проверка нажатия на ргион
                    pos_in_mask = event.pos[0] - sprit.rect.x, event.pos[1] - sprit.rect.y
                    if sprit.rect.collidepoint(event.pos) and sprit.mask.get_at(pos_in_mask):
                        if pygame.mouse.get_pressed()[0]:  # проверка, что была нажата левая клавиша мыши
                            function_call = functions[sprit.function]  # вызов функции по атрибуту function
                            function_call(True, sprit)  # который передается как ключ в словарь функций functions
                        elif pygame.mouse.get_pressed()[2]:  # проверка, что была нажата левая клавиша мыши
                            function_call = functions[sprit.function + '_2']  # вызов функции по атрибуту function
                            function_call(True, sprit)  # который передается как ключ в словарь функций functions
                for sprit_ in [s for s in special_sprite_list if s.rect.collidepoint(pygame.mouse.get_pos())]:
                    if sprit_.visible:
                        sprite_move_now = sprit_
                        if sprit_.function == "move_region_menu" and pygame.mouse.get_pressed()[0]:
                            flag_move_1 = not flag_move_1
                            if flag_move_1:
                                mouse_start = pygame.mouse.get_pos()[0] - sprit_.rect.x, pygame.mouse.get_pos()[
                                    1] - sprit_.rect.y
                        elif sprit_.function == "move_region_menu" and pygame.mouse.get_pressed()[2]:
                            click_r_1 = not click_r_1
                        break
                for sprit_2 in interface_sprite_list:
                    if sprit_2.rect.collidepoint(pygame.mouse.get_pos()) and sprit_2.visible:
                        if pygame.mouse.get_pressed()[0]:
                            if sprit_2.function != '':
                                function_call = functions[sprit_2.function]
                                function_call()

        pygame.draw.rect(screen_main, (0, 0, 0),
                         (0, 0, size_menu[0], size_menu[1]))  # (временно) заполнение экрана черным фоном
        group_map_sprite.draw(screen_main)  # отрисовка карты
        open_sprite_list_2()  # отрисовка меню страны
        open_sprite_list()  # отрисовка меню региона
        move_region_menu(flag_move_1, mouse_start, True) if click_r_1 else move_region_menu(flag_move_1, mouse_start)
        render_interface()  # отрисовка интерфейса
        render_setting(screen_main)
        pygame.display.update()


def main(file_name):
    render(file_name)
    pygame.quit()
