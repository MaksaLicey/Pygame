from special import *
import os


# import random


# import shutil


# файл игры

def create_file(name_file, start_option_1, start_option_2, start_option_3):  # получаем параметры игры
    file_game = open(os.path.join("saves", name_file), mode="w", encoding="utf-8")  # создаем новый файл
    file_game.write(f"file_name = {name_file}" + "\n")  # записываем в него все стартовые параметры
    file_game.write(f"map_name = {start_option_1[7:-4]}" + "\n")
    file_game.write(f"difficlt = {start_option_2[7:-4]} \n")
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

    clock = pygame.time.Clock()
    size_menu = 1536, 803
    screen_main = pygame.display.set_mode(size_menu)
    image_for_icon = load_image("icon_for_game.png")  # изображение для иконки приложения
    pygame.display.set_icon(image_for_icon)
    pygame.display.set_caption('The final strike')  # название приложения

    sprite_province_info = GameSprite(500, 10, "province_info.png", False, "open_region_info")

    sprites_list = [sprite_province_info]
    group_visible_sprite_1 = pygame.sprite.Group()

    info_list_from_file = file_reader(file_name)  # получение информации из файла
    sprite_map_list = info_list_from_file[0]
    file_info_list = info_list_from_file[1]
    country_list = info_list_from_file[2]
    group_map_sprite = pygame.sprite.Group()

    selected_map_sprite = sprite_map_list[0]  # выделенный спрайт (чтоб не создавать новый спрайт, просто в начале

    # присвоил любой первый экземпляр SpritesCreateForMap из sprite_map_list)

    def open_sprite_list(flag, sprite=''):  # функция для смены видимости окна
        # информации о регионе, если передать True и экземпляр нажатого класса SpritesCreateForMap
        global selected_map_sprite
        if flag:
            if sprite != '' and sprite_province_info.visible and selected_map_sprite != sprite:
                selected_map_sprite = sprite
            else:
                selected_map_sprite = sprite
                sprite_province_info.visible = not sprite_province_info.visible
        else:
            if sprite_province_info.visible:
                group_visible_sprite_1.add(sprite_province_info)
                group_visible_sprite_1.draw(screen_main)
                screen_main.blit(pygame.font.Font(None, 32).render(selected_map_sprite.name, True, (255, 0, 0)),
                                 (100, 100))
            elif not sprite_province_info.visible and sprite_province_info in group_visible_sprite_1:
                group_visible_sprite_1.remove(group_visible_sprite_1)

    functions = {
        # наконец решил оформить код, исполняемый при нажатии
        # на спрайт в отдельные функции и поместить их в список...
        "open_region_info": open_sprite_list
    }

    for sprite_ in sprite_map_list:  # добавление всех спрайтов карты в группу group_map_sprite
        group_map_sprite.add(sprite_)

    running_2 = True
    while running_2:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running_2 = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    running_2 = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for sprit in sprite_map_list:
                    pos_in_mask = event.pos[0] - sprit.rect.x, event.pos[1] - sprit.rect.y
                    if sprit.rect.collidepoint(event.pos) and sprit.mask.get_at(pos_in_mask):
                        if pygame.mouse.get_pressed()[0]:  # проверка, что была нажата левая клавиша мыши
                            l = functions[sprit.function]  # вызов функции по атрибуту function
                            l(True, sprit)  # который передается как ключ в словарь функций functions
                for sprite in sprites_list:
                    if sprite.rect.collidepoint(event.pos):
                        pass
        pygame.draw.rect(screen_main, (0, 0, 0),
                         (0, 0, size_menu[0], size_menu[1]))  # (временно) заполнение экрана черным фоном
        group_map_sprite.draw(screen_main)
        open_sprite_list(False)
        pygame.display.update()


def main(file_name):
    render(file_name)
    pygame.quit()
