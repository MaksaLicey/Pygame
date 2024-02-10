import pygame

from Main_Game_File import *
from special import *
from special_2 import render_setting, open_settings, setting_event

# файл для работы со стартовым меню

def main():
    pygame.init()
    text_file_name = ''
    # os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 30)

    sprite_play_btn = MenySpriteCreate(300, 30, "btn_GamePlay.png", True, 'open_start_menu')
    # спрайт кнопки начать новую игру, экземпляр класса SpriteCreate, из special.py
    sprite_open_setting = MenySpriteCreate(950, 30, "setting_btn_img.png", True, 'open_setting')
    sprite_start_menu = MenySpriteCreate(100, 50, "start_menu.png", False)
    sprite_start_afrika = MenySpriteCreate(sprite_start_menu.rect.x + 30, sprite_start_menu.rect.y + 70, "Afrika.png",
                                           False, 'selected_1', 'prompt_1.png')
    sprite_start_europe = MenySpriteCreate(sprite_start_menu.rect.x + 280, sprite_start_menu.rect.y + 70, "europe.png",
                                           False, 'selected_1', 'prompt_1.png')

    sprite_start_latina = MenySpriteCreate(sprite_start_menu.rect.x + 490, sprite_start_menu.rect.y + 70, "Latina.png",
                                           False, 'selected_1', 'prompt_latina.png')

    sprite_start_america = MenySpriteCreate(sprite_start_menu.rect.x + 650, sprite_start_menu.rect.y + 60,
                                            "America.png",
                                            False, 'selected_1', 'prompt_1.png')

    sprite_game_diff_1 = MenySpriteCreate(sprite_start_menu.rect.x + 70, sprite_start_menu.rect.y + 320,
                                          "game_difficutly_1.png",
                                          False, 'selected_2', 'prompt_difficutly_1.png')
    # sprite_game_diff_1, sprite_game_diff_2... спрайты кнопок выбора сложности
    sprite_game_diff_2 = MenySpriteCreate(sprite_start_menu.rect.x + 270, sprite_start_menu.rect.y + 320,
                                          "game_difficutly_2.png",
                                          False, 'selected_2', 'prompt_difficutly_2.png')
    sprite_game_diff_3 = MenySpriteCreate(sprite_start_menu.rect.x + 470, sprite_start_menu.rect.y + 320,
                                          "game_difficutly_3.png",
                                          False, 'selected_2', 'prompt_difficutly_3.png')
    sprite_game_diff_4 = MenySpriteCreate(sprite_start_menu.rect.x + 670, sprite_start_menu.rect.y + 320,
                                          "game_difficutly_4.png",
                                          False, 'selected_2', 'prompt_difficutly_4.png')

    sprite_character_1 = MenySpriteCreate(sprite_start_menu.rect.x + 100, sprite_start_menu.rect.y + 400,
                                          "character_1.png",
                                          False, 'selected_3', 'prompt_character_1.png')
    # sprite_character_1, ... спрайты кнопок выбора лидера
    sprite_character_2 = MenySpriteCreate(sprite_start_menu.rect.x + 300, sprite_start_menu.rect.y + 400,
                                          "character_2.png",
                                          False, 'selected_3', 'prompt_character_2.png')
    sprite_character_3 = MenySpriteCreate(sprite_start_menu.rect.x + 500, sprite_start_menu.rect.y + 400,
                                          "character_3.png",
                                          False, 'selected_3', 'prompt_character_3.png')
    sprite_character_4 = MenySpriteCreate(sprite_start_menu.rect.x + 700, sprite_start_menu.rect.y + 400,
                                          "character_4.png",
                                          False, 'selected_3', 'prompt_character_4.png')
    sprite_start_game = MenySpriteCreate(sprite_start_menu.rect.x + 350, sprite_start_menu.rect.y + 500,
                                         "btn_start_game.png",
                                         False, 'open_list')

    sprite_file_menu = MenySpriteCreate(sprite_start_menu.rect.x + 320, sprite_start_menu.rect.y + 180,
                                        "file_list.png",
                                        False)
    sprite_up_list = MenySpriteCreate(sprite_file_menu.rect.x + 20, sprite_file_menu.rect.y + 200,
                                      "up_list.png",
                                      False, 'up_list')
    sprite_down_list = MenySpriteCreate(sprite_file_menu.rect.x + 60, sprite_file_menu.rect.y + 200,
                                        "down_list.png",
                                        False, 'down_list')
    sprite_input_name_file = MenySpriteCreate(sprite_file_menu.rect.x + 20, sprite_file_menu.rect.y + 240,
                                              "input_name_file.png",
                                              False, 'start_input_file_name', '')
    sprite_crete_file = MenySpriteCreate(sprite_file_menu.rect.x + 30, sprite_file_menu.rect.y + 290,
                                         "create_file.png",
                                         False, 'create_file_and_start')

    sprite_file_name_mistake = MenySpriteCreate(sprite_file_menu.rect.x - 100, sprite_file_menu.rect.y - 140,
                                                "file_name_mistake.png",
                                                False, 'file_name_mistake')

    # список спрайтов меню (в последующем не изменяется)
    menu_sprites = [sprite_play_btn, sprite_open_setting, sprite_start_menu,
                    sprite_start_menu, sprite_start_afrika, sprite_start_europe, sprite_start_latina,
                    sprite_start_america, sprite_game_diff_1, sprite_game_diff_2, sprite_game_diff_3,
                    sprite_game_diff_4, sprite_character_1, sprite_character_2,
                    sprite_character_3, sprite_character_4, sprite_start_game, sprite_file_menu, sprite_up_list,
                    sprite_down_list, sprite_input_name_file, sprite_crete_file, sprite_file_name_mistake]

    group_visible_sprite = pygame.sprite.Group()  # группа для хранения видимых спрайтов,

    # Единственная для всех спрайтов меню. В цикле игры наполняется спрайтами, у которых visible = True

    def list_file_menu():  # отображение спрайтов меню
        if sprite_start_menu.visible:
            sprite_file_menu.visible = not sprite_file_menu.visible
        else:
            sprite_file_menu.visible = False
        sprite_up_list.visible = sprite_file_menu.visible
        sprite_down_list.visible = sprite_file_menu.visible
        sprite_input_name_file.visible = sprite_file_menu.visible
        sprite_crete_file.visible = sprite_file_menu.visible
        if not sprite_file_menu.visible:
            sprite_file_name_mistake.visible = sprite_file_menu.visible

    def sprite_checker1():  # функция обработки нажатия на спрайты меню (не смотреть!!!)
        global selected  # может быть True/False, в зависимости выбран ли параметр из первой строчки
        global selected_2  # по аналогии с первым
        global selected_3
        global selected_sprite_1  # копия выделенного спрайта
        global selected_sprite_2
        global selected_sprite_3
        global text_input_active
        global running
        if clicked_sprites[-1].function == 'open_setting':
            # sprite_setting_menu.visible = not sprite_setting_menu.visible
            # sprite_btn1_setting.visible = sprite_setting_menu.visible
            open_settings()
            # pass

        if clicked_sprites[-1].function == 'open_start_menu':
            sprite_start_menu.visible = not sprite_start_menu.visible
            sprite_start_afrika.visible = sprite_start_menu.visible
            sprite_start_europe.visible = sprite_start_menu.visible
            sprite_start_latina.visible = sprite_start_menu.visible
            sprite_start_america.visible = sprite_start_menu.visible
            sprite_game_diff_1.visible = sprite_start_menu.visible
            sprite_game_diff_2.visible = sprite_start_menu.visible
            sprite_game_diff_3.visible = sprite_start_menu.visible
            sprite_game_diff_4.visible = sprite_start_menu.visible
            sprite_character_1.visible = sprite_start_menu.visible
            sprite_character_2.visible = sprite_start_menu.visible
            sprite_character_3.visible = sprite_start_menu.visible
            sprite_character_4.visible = sprite_start_menu.visible
            sprite_start_game.visible = sprite_start_menu.visible
            if not sprite_start_menu.visible:
                list_file_menu()

        if clicked_sprites[-1].function == 'selected_1' and not sprite_file_menu.visible:
            if clicked_sprites[-1] != selected_sprite_1:
                selected_sprite_1 = clicked_sprites[-1]
                selected = True
            else:
                selected_sprite_1 = pygame.sprite
                selected = False
        if clicked_sprites[-1].function == 'selected_2' and not sprite_file_menu.visible:
            if clicked_sprites[-1] != selected_sprite_2:
                selected_sprite_2 = clicked_sprites[-1]
                selected_2 = True
            else:
                selected_sprite_2 = pygame.sprite
                selected_2 = False
        if clicked_sprites[-1].function == 'selected_3' and not sprite_file_menu.visible:
            if clicked_sprites[-1] != selected_sprite_3:
                selected_sprite_3 = clicked_sprites[-1]
                selected_3 = True
            else:
                selected_sprite_3 = pygame.sprite
                selected_3 = False
        if (clicked_sprites[-1].function == 'open_list' and selected_sprite_1 != pygame.sprite and
                selected_sprite_2 != pygame.sprite and selected_sprite_3 != pygame.sprite):
            list_file_menu()

        if clicked_sprites[-1].function == 'up_list':
            get_files_list(-1)
        if clicked_sprites[-1].function == 'down_list':
            get_files_list(1)

        if clicked_sprites[-1].function == "start_input_file_name":
            text_input_active = not text_input_active
        if clicked_sprites[-1].function == "create_file_and_start" and text_file_name != "":
            if text_file_name in get_files_list()[1]:
                sprite_file_name_mistake.visible = True
            else:
                running = False
                open_settings(True)
                create_file(text_file_name, selected_sprite_1.prompt, selected_sprite_2.prompt,
                            selected_sprite_3.prompt)
        if clicked_sprites[-1].function == "file_name_mistake":
            sprite_file_name_mistake.visible = False

    size_menu = 1100, 700  # размер меню
    screen = pygame.display.set_mode(size_menu)
    image_for_menu = load_image("test1.png")  # фон для меню
    screen.blit(image_for_menu, (0, 0))
    image_for_icon = load_image("icon_for_game.png")  # изображение для иконки приложения
    pygame.display.set_icon(image_for_icon)
    pygame.display.set_caption('The final strike')  # название приложения

    clock = pygame.time.Clock()
    global running
    while running:  # основной цикл игры
        clock.tick(60)
        events = pygame.event.get()
        for EVENT in events:
            setting_event(EVENT) # передача события в обработчик работы с настройками
            if EVENT.type == pygame.QUIT:
                running = False
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [s for s in group_visible_sprite if s.rect.collidepoint(
                        pos)]  # добавление спрайтов, на которых был курсор мыши во время нажатия
                    if len(clicked_sprites) > 0:
                        sprite_checker1()
            if EVENT.type == pygame.KEYDOWN:
                if text_input_active:  # ввод названия файла
                    if EVENT.key == pygame.K_BACKSPACE:
                        text_file_name = text_file_name[:-1]
                    else:
                        if (EVENT.unicode != '\\' and EVENT.unicode != '/' and EVENT.unicode != '\r' and
                                EVENT.unicode != '\t' and EVENT.unicode != '\x1b' and EVENT.unicode != '|'):
                            text_file_name += EVENT.unicode
                if EVENT.key == pygame.K_ESCAPE and sprite_file_menu.visible:  # закрытие меню создания файла на esc
                    list_file_menu()


        for sprit in menu_sprites:
            if sprit.visible:
                group_visible_sprite.add(sprit)  # добавление видимых спрайтов в группу
            elif sprit in group_visible_sprite:
                group_visible_sprite.remove(sprit)
        if not running:  # иногда окно уже закрыто, а цикл не завершен
            break
        screen.blit(image_for_menu, (0, 0))
        group_visible_sprite.draw(screen)  # отображение видимых спрайтов

        if selected and sprite_start_menu.visible and not sprite_file_menu.visible:
            if len(clicked_sprites) > 0:
                if selected_sprite_1.function == 'selected_1':
                    pygame.draw.rect(screen, (255, 0, 0), (
                        selected_sprite_1.rect[0] - 15, selected_sprite_1.rect[1] - 15,
                        selected_sprite_1.rect[2] + 30,
                        selected_sprite_1.rect[3] + 30),
                                     width=5)
        if (selected_2 and sprite_start_menu.visible and not sprite_file_menu.visible):
            if len(clicked_sprites) > 0:
                if selected_sprite_2.function == 'selected_2':
                    pygame.draw.rect(screen, (0, 255, 0), (
                        selected_sprite_2.rect[0], selected_sprite_2.rect[1], selected_sprite_2.rect[2],
                        selected_sprite_2.rect[3]), width=5)
        if (selected_3 and sprite_start_menu.visible and not sprite_file_menu.visible):
            if len(clicked_sprites) > 0:
                if selected_sprite_3.function == 'selected_3':
                    pygame.draw.rect(screen, (0, 0, 255), (
                        selected_sprite_3.rect[0], selected_sprite_3.rect[1], selected_sprite_3.rect[2],
                        selected_sprite_3.rect[3]), width=5)
        if sprite_file_menu.visible:
            for i in range(len(get_files_list()[0])):
                txt_surface = pygame.font.Font(None, 32).render(text_file_name, True, (255, 0, 0))
                max_text_width = 150  # максимальная длинна имени файла
                if txt_surface.get_width() >= max_text_width:  # проверка длины текста
                    for b in range(len(text_file_name)):
                        txt_surface = pygame.font.Font(None, 32).render(text_file_name[0:b], True, (255, 0, 0))
                        if txt_surface.get_width() >= max_text_width:
                            text_file_name = text_file_name[0:b]
                            break
                screen.blit(pygame.font.Font(None, 32).render(get_files_list()[0][i], True, (255, 0, 0)),
                            (sprite_file_menu.rect.x + 20, sprite_file_menu.rect.y + 20 + (i * 20)))

        if EVENT.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            clicked_sprites_2 = [s for s in group_visible_sprite if s.rect.collidepoint(pos)]
            # добавление спрайтов, на которых попал курсор мыши в список
            if len(clicked_sprites_2) > 0:  # ну и отображение подсказки, если таковая есть
                if clicked_sprites_2[-1].prompt != '' and not sprite_file_menu.visible:
                    prompt_image = load_image(clicked_sprites_2[-1].prompt)
                    screen.blit(prompt_image, pos)
        if sprite_input_name_file.visible:
            if text_input_active:
                screen.fill((200, 100, 100), sprite_input_name_file.rect)
                txt_surface = pygame.font.Font(None, 40).render(text_file_name, True, (70, 195, 150))
                screen.blit(txt_surface, (sprite_input_name_file.rect.x + 10, sprite_input_name_file.rect.y + 5))
            else:
                txt_surface = pygame.font.Font(None, 40).render(text_file_name, True, (100, 100, 200))
                screen.blit(txt_surface, (sprite_input_name_file.rect.x + 10, sprite_input_name_file.rect.y + 5))
        render_setting(screen)
        pygame.display.update()


if __name__ == "__main__":
    selected = False
    selected_2 = False
    selected_3 = False
    selected_sprite_1 = pygame.sprite
    selected_sprite_2 = pygame.sprite
    selected_sprite_3 = pygame.sprite
    text_input_active = False
    running = True
    main()
    pygame.quit()
