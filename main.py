import pygame
import os
import sys
import pygame as pg


class SpriteCreate(pygame.sprite.Sprite):  # класс для создания спрайтов
    def __init__(self, rect_x, rect_y, file_name, visible_s, fuction_s, promt):
        super().__init__()
        # self.image = image
        self.image = load_image(file_name)
        self.size = load_image(file_name).get_size()
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.visible = visible_s
        self.function = fuction_s
        self.prompt = promt


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


selected = False
selected_2 = False
selected_3 = False
selected_sptite = pygame.sprite
selected_sptite_2 = pygame.sprite
selected_sptite_3 = pygame.sprite


def main():
    pygame.init()

    group_visible_sprite = pygame.sprite.Group()  # группа для хранения видимых спрайтов
    sprite_play_btn = SpriteCreate(300, 30, "btn_GamePlay.png", True, 'open_start_menu', '')
    # создаем спрайт кнопки 0, экземпляр класса SpriteCreate
    sprite_setting_menu = SpriteCreate(700, 160, "setting_menu.png", False, '', '')  # создаем спрайт кнопки начала игры
    sprite_open_setting = SpriteCreate(950, 30, "setting_btn_img.png", True, 'open_setting', '')
    sprite_btn1_setting = SpriteCreate(sprite_setting_menu.rect.x + 20, sprite_setting_menu.rect.y + 20,
                                       "setting_btn_2.png", sprite_setting_menu.visible,
                                       'open_setting', '')  # создаем спрайт кнопки 2
    sprite_start_btn = SpriteCreate(100, 100, "start_menu.png", False, '', '')
    sprite_start_Afrika = SpriteCreate(sprite_start_btn.rect.x + 30, sprite_start_btn.rect.y + 70, "Afrika.png",
                                       False, 'selected_1', 'prompt_1.png')
    sprite_start_Europe = SpriteCreate(sprite_start_btn.rect.x + 280, sprite_start_btn.rect.y + 70, "europe.png",
                                       False, 'selected_1', 'prompt_1.png')

    sprite_start_Latina = SpriteCreate(sprite_start_btn.rect.x + 490, sprite_start_btn.rect.y + 70, "Latina.png",
                                       False, 'selected_1', 'prompt_1.png')

    sprite_start_Amerika = SpriteCreate(sprite_start_btn.rect.x + 650, sprite_start_btn.rect.y + 60, "Amerika.png",
                                        False, 'selected_1', 'prompt_1.png')

    sprite_game_diff_1 = SpriteCreate(sprite_start_btn.rect.x + 70, sprite_start_btn.rect.y + 320,
                                      "game_difficutly_1.png",
                                      False, 'selected_2', 'prompt_1.png')

    sprite_game_diff_2 = SpriteCreate(sprite_start_btn.rect.x + 270, sprite_start_btn.rect.y + 320,
                                      "game_difficutly_2.png",
                                      False, 'selected_2', 'prompt_1.png')

    sprite_game_diff_3 = SpriteCreate(sprite_start_btn.rect.x + 470, sprite_start_btn.rect.y + 320,
                                      "game_difficutly_3.png",
                                      False, 'selected_2', 'prompt_1.png')

    sprite_game_diff_4 = SpriteCreate(sprite_start_btn.rect.x + 670, sprite_start_btn.rect.y + 320,
                                      "game_difficutly_4.png",
                                      False, 'selected_2', 'prompt_1.png')

    sprite_character_1 = SpriteCreate(sprite_start_btn.rect.x + 100, sprite_start_btn.rect.y + 400,
                                      "character_1.png",
                                      False, 'selected_3', 'prompt_1.png')

    sprite_character_2 = SpriteCreate(sprite_start_btn.rect.x + 300, sprite_start_btn.rect.y + 400,
                                      "character_2.png",
                                      False, 'selected_3', 'prompt_1.png')
    sprite_character_3 = SpriteCreate(sprite_start_btn.rect.x + 500, sprite_start_btn.rect.y + 400,
                                      "character_3.png",
                                      False, 'selected_3', 'prompt_1.png')
    sprite_character_4 = SpriteCreate(sprite_start_btn.rect.x + 700, sprite_start_btn.rect.y + 400,
                                      "character_4.png",
                                      False, 'selected_3', 'prompt_1.png')
    # pygame.draw.rect(sprite_start_Afrika.rect.x, sprite_start_Afrika.rect.y, sprite_start_Afrika.rect)

    menu_sprites = list()  # список справйтов меню
    menu_sprites.append(sprite_play_btn)
    menu_sprites.append(sprite_setting_menu)
    menu_sprites.append(sprite_open_setting)
    menu_sprites.append(sprite_btn1_setting)
    menu_sprites.append(sprite_start_btn)
    menu_sprites.append(sprite_start_Afrika)
    menu_sprites.append(sprite_start_Europe)
    menu_sprites.append(sprite_start_Latina)
    menu_sprites.append(sprite_start_Amerika)
    menu_sprites.append(sprite_game_diff_1)
    menu_sprites.append(sprite_game_diff_2)
    menu_sprites.append(sprite_game_diff_3)
    menu_sprites.append(sprite_game_diff_4)
    menu_sprites.append(sprite_character_1)
    menu_sprites.append(sprite_character_2)
    menu_sprites.append(sprite_character_3)
    menu_sprites.append(sprite_character_4)

    def sprite_checker1():
        global selected
        global selected_2
        global selected_3
        global selected_sptite
        global selected_sptite_2
        global selected_sptite_3
        if clicked_sprites[-1].function == 'open_setting':
            sprite_setting_menu.visible = not sprite_setting_menu.visible
            sprite_btn1_setting.visible = sprite_setting_menu.visible

        if clicked_sprites[-1].function == 'open_start_menu':
            sprite_start_btn.visible = not sprite_start_btn.visible
            sprite_start_Afrika.visible = sprite_start_btn.visible
            sprite_start_Europe.visible = sprite_start_btn.visible
            sprite_start_Latina.visible = sprite_start_btn.visible
            sprite_start_Amerika.visible = sprite_start_btn.visible
            sprite_game_diff_1.visible = sprite_start_btn.visible
            sprite_game_diff_2.visible = sprite_start_btn.visible
            sprite_game_diff_3.visible = sprite_start_btn.visible
            sprite_game_diff_4.visible = sprite_start_btn.visible
            sprite_character_1.visible = sprite_start_btn.visible
            sprite_character_2.visible = sprite_start_btn.visible
            sprite_character_3.visible = sprite_start_btn.visible
            sprite_character_4.visible = sprite_start_btn.visible
        if clicked_sprites[-1].function == 'selected_1':
            if clicked_sprites[-1] != selected_sptite:
                selected_sptite = clicked_sprites[-1]
                selected = True
            else:
                selected_sptite = pygame.sprite
                selected = False
        if clicked_sprites[-1].function == 'selected_2':
            if clicked_sprites[-1] != selected_sptite_2:
                selected_sptite_2 = clicked_sprites[-1]
                selected_2 = True
            else:
                selected_sptite_2 = pygame.sprite
                selected_2 = False
        if clicked_sprites[-1].function == 'selected_3':
            if clicked_sprites[-1] != selected_sptite_3:
                selected_sptite_3 = clicked_sprites[-1]
                selected_3 = True
            else:
                selected_sptite_3 = pygame.sprite
                selected_3 = False

    #
    size_menu = 1100, 700  # размер меню
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode(size_menu)
    image = load_image("test1.png")  # фон для меню
    screen.blit(image, (0, 0))
    img = pygame.image.load("data\_frist.png")
    pygame.display.set_icon(img)
    pygame.display.set_caption('The final strike')

    clock = pg.time.Clock()
    running = True
    while running:  # основной цикл игры
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in group_visible_sprite if s.rect.collidepoint(pos)]

                if len(clicked_sprites) > 0:
                    sprite_checker1()
        for sprit in menu_sprites:
            if sprit.visible:
                group_visible_sprite.add(sprit)  # добавление видимых спрайтов в группу
            else:
                if sprit in group_visible_sprite:
                    group_visible_sprite.remove(sprit)

        screen.blit(image, (0, 0))
        group_visible_sprite.draw(screen)  # отображение видимых спрайтов
        if selected and sprite_start_btn.visible:
            if len(clicked_sprites) > 0:
                if selected_sptite.function == 'selected_1':
                    pygame.draw.rect(screen, (255, 0, 0), (
                        (selected_sptite.rect)[0] - 15, (selected_sptite.rect)[1] - 15,
                        (selected_sptite.rect)[2] + 30,
                        (selected_sptite.rect)[3] + 30),
                                     width=5)
        if selected_2 and sprite_start_btn.visible:
            if len(clicked_sprites) > 0:
                if selected_sptite_2.function == 'selected_2':
                    pygame.draw.rect(screen, (0, 255, 0), (
                        (selected_sptite_2.rect)[0], (selected_sptite_2.rect)[1], (selected_sptite_2.rect)[2],
                        (selected_sptite_2.rect)[3]), width=5)
        if selected_3 and sprite_start_btn.visible:
            if len(clicked_sprites) > 0:
                if selected_sptite_3.function == 'selected_3':
                    pygame.draw.rect(screen, (0, 0, 255), (
                        (selected_sptite_3.rect)[0], (selected_sptite_3.rect)[1], (selected_sptite_3.rect)[2],
                        (selected_sptite_3.rect)[3]), width=5)

        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            clicked_sprites_2 = [s for s in group_visible_sprite if s.rect.collidepoint(pos)]
            if len(clicked_sprites_2) > 0:
                if clicked_sprites_2[-1].prompt != '':
                    test_image = load_image(clicked_sprites_2[-1].prompt)
                    screen.blit(test_image, pos)
        pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.quit()
