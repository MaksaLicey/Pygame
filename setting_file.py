from special import MenySpriteCreate
import pygame
import os

# файл для работы с настройками

sprite_setting_menu = MenySpriteCreate(None, 700, 200, os.path.join("settings", "setting_menu.png"),
                                       False, "")
sprite_input_text = MenySpriteCreate(None, sprite_setting_menu.rect.x + 275, sprite_setting_menu.rect.y + 25,
                                     os.path.join("settings", "input_name_file.png"),
                                     False, "start_input")
sprite_apply_setting = MenySpriteCreate(None, sprite_setting_menu.rect.x + 100, sprite_setting_menu.rect.y + 300,
                                        os.path.join("settings", "apply_setting.png"),
                                        False, "apply_settings")
sprite_save_setting = MenySpriteCreate(None, sprite_setting_menu.rect.x + 100, sprite_setting_menu.rect.y + 350,
                                       os.path.join("settings", "save_setting.png"),
                                       False, "save_settings")
sprite_down_volume = MenySpriteCreate(None, sprite_setting_menu.rect.x + 20, sprite_setting_menu.rect.y + 100,
                                      os.path.join("settings", "down_volume.png"),
                                      False, "down_volume")
sprite_up_volume = MenySpriteCreate(None, sprite_setting_menu.rect.x + 330, sprite_setting_menu.rect.y + 100,
                                    os.path.join("settings", "up_volume.png"),
                                    False, "up_volume")
sprite_check_fuel_screen = MenySpriteCreate(None, sprite_setting_menu.rect.x + 160, sprite_setting_menu.rect.y + 200,
                                            os.path.join("settings", "check_box1.png"),
                                            False, "check_fuel_screen")
sprite_check_mark = MenySpriteCreate(None, sprite_setting_menu.rect.x + 160, sprite_setting_menu.rect.y + 200,
                                     os.path.join("settings", "check_mark.png"),
                                     False, "")
sprite_input_screen_size = MenySpriteCreate(None, sprite_setting_menu.rect.x + 160, sprite_setting_menu.rect.y + 160,
                                            os.path.join("settings", "input_screen_size.png"),
                                            False, "start_input_size")
sprite_input_save_time = MenySpriteCreate(None, sprite_setting_menu.rect.x + 160, sprite_setting_menu.rect.y + 255,
                                          os.path.join("settings", "input_screen_size.png"),
                                          False, "input_days_of_save")
sprite_remove_settings = MenySpriteCreate(None, sprite_setting_menu.rect.x, sprite_setting_menu.rect.y - 44,
                                          os.path.join("settings", "remove_settings.png"),
                                          False, "remove_settings")
sprite_settings_err1 = MenySpriteCreate(None, sprite_setting_menu.rect.x, sprite_setting_menu.rect.y,
                                        os.path.join("settings", "settings_err1.png"),
                                        False, "settings_err1")
sprite_close_settings = MenySpriteCreate(None, sprite_setting_menu.rect.x + 365, sprite_setting_menu.rect.y + 2,
                                         os.path.join("settings", "close_settings.png"),
                                         False, "open_settings")

setting_sprite_list = [sprite_setting_menu, sprite_input_text, sprite_apply_setting, sprite_save_setting,
                       sprite_down_volume, sprite_remove_settings, sprite_close_settings,
                       sprite_up_volume, sprite_check_fuel_screen, sprite_input_screen_size, sprite_input_save_time]
checker_single_group = pygame.sprite.GroupSingle(sprite_check_mark)
error_single_group = pygame.sprite.GroupSingle(sprite_settings_err1)
group_for_setting = pygame.sprite.Group()

# значения настроек
file_settings = open(os.path.join("data", "settings", "setting_file"), encoding="utf8")
sls = file_settings.readlines()
fps = int(sls[0])  # считывание настроек из data\settings\setting_file
volume = int(sls[1])
auto_save = False if sls[2] == "False" else True
screen_size1 = [int(sls[3].split()[0]), int(sls[3].split()[1])]
koff = screen_size1[0] / 800
days_to_save = int(sls[4])
file_settings.close()

enter_fps = False  # если True, происходит ввод ограничения фпс
enter_size = False  # аналогично
enter_days_of_save = False
return_settings = False


def change_sprites_size():  # изменение размеров окна настроек (аналогично sprite_change_size классов
    global koff
    for i in [setting_sprite_list, [sprite_check_mark, sprite_settings_err1]]:
        for sprit_s in i:
            sprit_s.rect.x = sprit_s.rect_x_start * koff
            sprit_s.rect.y = sprit_s.rect_y_start * koff
            sprit_s.rect[2] = sprit_s.image_copy.get_size()[0] * koff
            sprit_s.rect[3] = sprit_s.image_copy.get_size()[1] * koff
            sprit_s.image = pygame.transform.scale(sprit_s.image_copy, (
                sprit_s.image_copy.get_size()[0] * koff,
                sprit_s.image_copy.get_size()[1] * koff))


def input_days_of_save():  # начало\конец ввода интервала авто сохранений (в днях)
    global enter_fps, enter_size, enter_days_of_save
    enter_days_of_save = not enter_days_of_save
    if enter_days_of_save: enter_size, enter_fps = False, False


def start_input_size():  # начало\конец ввода размера окна игры
    global enter_fps, enter_size, enter_days_of_save
    if not sprite_check_mark.visible:
        enter_size = not enter_size
        if enter_size: enter_fps, enter_days_of_save = False, False
    else:
        sprite_check_mark.visible = False
        start_input_size()


def input_fps():  # начала\конец ввода ограничения фпс
    global enter_fps, enter_size, enter_days_of_save
    enter_fps = not enter_fps
    if enter_fps: enter_size, enter_days_of_save = False, False


def down_volume():  # уменьшить громкость звуков в игре
    global volume
    if volume >= 0: volume -= 1


def up_volume():  # увеличить громкость в игре
    global volume
    if volume < 10: volume += 1


def check_auto_save(flag=True):  # включение\отключение авто сохранения
    global auto_save, enter_size, enter_size, enter_fps, enter_days_of_save
    if flag:
        enter_size, enter_fps, enter_days_of_save = False, False, False
        auto_save = not auto_save
    sprite_check_mark.visible = auto_save


def save_settings():  # сохранить выбранные настройки в data\settings\setting_file
    global fps, volume, auto_save, screen_size1, days_to_save, enter_size, enter_fps, enter_days_of_save
    enter_size, enter_fps, enter_days_of_save = False, False, False
    check_validity()
    file_setting = open(os.path.join("data", "settings", "setting_file"), "w", encoding="utf8")
    file_setting.write(str(fps) + '\r')
    file_setting.write(str(volume) + '\r')
    file_setting.write(str(auto_save) + '\r')
    file_setting.write(str(screen_size1[0]) + " " + str(int(float(screen_size1[1]) * 1.92)) + '\r')
    file_setting.write(str(days_to_save))
    file_setting.close()


def remove_settings():  # вернуть настройки по умолчанию (сохранены в data\settings\setting_file_base)
    global fps, volume, auto_save, screen_size1, days_to_save, enter_size, enter_fps, enter_days_of_save
    file_settings = open(os.path.join("data", "settings", "setting_file_base"), encoding="utf8")
    sls1 = file_settings.readlines()
    fps = int(sls1[0])
    volume = int(sls1[1])
    auto_save = False if sls1[2] == "False" else True
    screen_size1 = [int(sls1[3].split()[0]), int(sls1[3].split()[1])]
    days_to_save = 30
    apply_settings()
    file_settings.close()


def apply_settings(flag=True):  # применить настройки
    global return_settings, fps, volume, auto_save, screen_size1, days_to_save, enter_size, enter_fps
    global enter_days_of_save, koff
    if flag:
        return_settings = not return_settings
    if not flag and return_settings:
        return_settings = False
        enter_fps, enter_size, enter_days_of_save = False, False, False
        check_validity()
        koff = screen_size1[0] / 800

        change_sprites_size()
        return [fps, volume, auto_save, screen_size1, days_to_save]


def settings_err1():  # закрытие окна об ошибке (настройки отличаются от сохраненных)
    sprite_settings_err1.visible = False


def check_validity():  # проверка корректности введенных данных
    global fps, volume, auto_save, screen_size1, days_to_save, enter_size, enter_fps, enter_days_of_save
    if not enter_fps:
        if fps <= 5:
            fps = 5
        elif fps > 144:
            fps = 144
    if not enter_days_of_save:
        if days_to_save > 1000:
            days_to_save = 1000
        if days_to_save <= 0:
            days_to_save = 10
    if not enter_size:
        if screen_size1[0] <= 100:
            screen_size1[0] = 100
        if screen_size1[0] > 25 * 86:
            screen_size1[0] = 2150


def setting_event(event):  # обработка события из цикла игры текущего окна
    global enter_fps, enter_fps, fps, screen_size1, days_to_save, enter_days_of_save, enter_size
    if sprite_setting_menu.visible:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] and (sprite_setting_menu.rect.collidepoint(
                    event.pos) or sprite_remove_settings.rect.collidepoint(event.pos)):
                call = [i for i in setting_sprite_list if i.rect.collidepoint(event.pos)][-1].function
                if call != '': function_set[call]()
    if sprite_settings_err1.visible and sprite_settings_err1.rect.collidepoint(
            pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
        settings_err1()
    if event.type == pygame.KEYDOWN:
        if event.unicode == '\r':
            enter_fps, enter_size, enter_days_of_save = False, False, False
        elif enter_fps:
            try:
                if event.key == pygame.K_BACKSPACE:
                    fps = int(str(fps)[:-1]) if len(str(fps)[:-1]) >= 1 else 0
                elif event.key != pygame.K_BACKSPACE and int(
                        str(fps) + event.unicode) <= 10000 and event.unicode != '\r':
                    fps = int(str(fps) + event.unicode)
            except Exception as e:
                error = e
        elif enter_size:
            try:
                if event.key == pygame.K_BACKSPACE:
                    screen_size1[0] = int(str(screen_size1[0])[:-1]) if len(str(screen_size1[0])[:-1]) >= 1 else 0
                elif event.key != pygame.K_BACKSPACE and int(
                        str(screen_size1[0]) + event.unicode) <= 20000 and event.unicode != '\r':
                    screen_size1[0] = int(str(screen_size1[0]) + event.unicode)
            except Exception as e:
                error = e
        elif enter_days_of_save:
            try:
                if event.key == pygame.K_BACKSPACE:
                    days_to_save = int(str(days_to_save)[:-1]) if len(str(days_to_save)[:-1]) >= 1 else 0
                elif event.key != pygame.K_BACKSPACE and int(
                        str(days_to_save) + event.unicode) <= 10000 and event.unicode != '\r':
                    days_to_save = int(str(days_to_save) + event.unicode)
            except Exception as e:
                error = e

    check_auto_save(False)
    check_validity()


def open_settings(flag=False):
    global fps, volume, auto_save, screen_size1, days_to_save
    if setting_sprite_list[0].visible:
        file_settings = open(os.path.join("data", "settings", "setting_file"), encoding="utf8")
        sls = file_settings.readlines()
        if (int(sls[0]) != fps or days_to_save != int(sls[4]) or screen_size1[0] != int(sls[3].split()[0]) or
                int(screen_size1[0]) != int(sls[3].split()[0]) or ''.join(sls[2][0:5].split()) != str(auto_save)):
            sprite_settings_err1.visible = True
        file_settings.close()
    if not flag:
        change_sprites_size()
        if not sprite_settings_err1.visible:
            for i in setting_sprite_list:
                i.visible = not i.visible
    else:
        if not sprite_settings_err1.visible:
            for i in setting_sprite_list:
                i.visible = False
        if sprite_settings_err1.visible:
            return "error"


def render_setting(screen):  # изображение окна настроек на принимаемый экран
    for i in setting_sprite_list:
        if i.visible:
            group_for_setting.add(i)
        elif not i.visible and i in group_for_setting:
            group_for_setting.remove(i)
    if sprite_setting_menu.visible:
        group_for_setting.draw(screen)
        str1 = 'ограничение фпс (5--144): '
        str2 = 'громкость аудио: '
        str3 = ' '
        str5 = '(!:'
        str6 = '!:'
        str7 = 'интревал'
        sls = [str1, str2, str3, str5, str6, str7]
        for i in range(len(sls)):  # отображение информации о спрайте
            # print(koff, screen_size1[0])
            screen.blit(pygame.font.Font(None, round(28 * koff)).render(sls[i], True,
                                                                        (255, 255, 255)),
                        (sprite_setting_menu.rect.x + 20 * koff,
                         sprite_setting_menu.rect.y + 30 * koff + (i * 45) * koff))
        if enter_fps:
            pygame.draw.rect(screen, (100, 150, 60),
                             (sprite_input_text.rect.x, sprite_input_text.rect.y, sprite_input_text.rect[2],
                              sprite_input_text.rect[3]))
        screen.blit(pygame.font.Font(None, int(26 * koff)).render(str(fps), True, (0, 0, 0)),
                    (sprite_input_text.rect.x + 10 * koff,
                     sprite_input_text.rect.y + 3 * koff))
        if sprite_setting_menu.visible:
            for index in range(11):
                color = (200, 0, 45) if index <= volume else (20, 100, 150)
                pygame.draw.rect(screen, color,
                                 (sprite_down_volume.rect.x + (50 + index * 24) * koff, sprite_down_volume.rect.y,
                                  17 * koff, 45 * koff))
        if sprite_check_mark.visible: checker_single_group.draw(screen)
        if sprite_settings_err1.visible: error_single_group.draw(screen)
        if enter_size:
            pygame.draw.rect(screen, (100, 150, 60),
                             (sprite_input_screen_size.rect.x, sprite_input_screen_size.rect.y,
                              sprite_input_screen_size.rect[2], sprite_input_screen_size.rect[3]))
        screen.blit(pygame.font.Font(None, round(26 * koff)).render(
            (str(screen_size1[0]) + 'x' + str(float(screen_size1[0]) * 1.92)), True, (0, 0, 0)),
            (sprite_input_screen_size.rect.x + 10 * koff, sprite_input_screen_size.rect.y + 5 * koff))
        if enter_days_of_save:
            pygame.draw.rect(screen, (100, 150, 60),
                             (sprite_input_save_time.rect.x, sprite_input_save_time.rect.y,
                              sprite_input_save_time.rect[2], sprite_input_save_time.rect[3]))
        screen.blit(pygame.font.Font(None, round(26 * koff)).render(
            str(days_to_save), True, (0, 0, 0)),
            (sprite_input_save_time.rect.x + 10, sprite_input_save_time.rect.y + 5))


function_set = {
    "start_input": input_fps,
    "up_volume": up_volume,
    "down_volume": down_volume,
    "check_fuel_screen": check_auto_save,
    "start_input_size": start_input_size,
    "input_days_of_save": input_days_of_save,
    "save_settings": save_settings,
    "remove_settings": remove_settings,
    "apply_settings": apply_settings,
    "open_settings": open_settings
}
