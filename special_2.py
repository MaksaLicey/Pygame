from special import MenySpriteCreate
import pygame
import os

sprite_setting_menu = MenySpriteCreate(None, 700, 200, os.path.join("settings", "setting_menu.png"),
                                       False, "")  # создаем спрайт кнопки начала игры
sprite_input_text = MenySpriteCreate(None, sprite_setting_menu.rect.x + 275, sprite_setting_menu.rect.y + 25,
                                     os.path.join("settings", "input_name_file.png"),
                                     False, "start_input")  # создаем спрайт кнопки начала игры
sprite_save_setting = MenySpriteCreate(None, sprite_setting_menu.rect.x + 100, sprite_setting_menu.rect.y + 300,
                                     os.path.join("settings", "save_setting.png"),
                                     False, "")  # создаем спрайт кнопки начала игры

setting_sprite_list = [sprite_setting_menu, sprite_input_text, sprite_save_setting]
group_for_setting = pygame.sprite.Group()
fps = 60

enter_fps = False


def start_input():
    global enter_fps
    enter_fps = not enter_fps


function_set = {
    "start_input": start_input,
}


def setting_event(event):
    global enter_fps
    global fps

    if sprite_setting_menu.visible:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] and sprite_setting_menu.rect.collidepoint(event.pos):
                call = [i for i in setting_sprite_list if i.rect.collidepoint(event.pos)][-1].function
                if call != '': function_set[call]()
    if event.type == pygame.KEYDOWN:
        if sprite_input_text.rect.collidepoint(pygame.mouse.get_pos()) and event.unicode == '\r':
            start_input()
        elif enter_fps:
            try:
                if event.key == pygame.K_BACKSPACE:
                    fps = int(str(fps)[:-1]) if len(str(fps)[:-1]) >= 1 else 0
                elif event.key != pygame.K_BACKSPACE and int(
                        str(fps) + event.unicode) <= 10000 and event.unicode != '\r':
                    fps = int(str(fps) + event.unicode)
                elif event.unicode == '\r':
                    start_input()
            except Exception as e:
                error = e
                # print(error)
    if not enter_fps:
        if fps <= 0:
            fps = 1
        elif fps > 144:
            fps = 144


def open_settings(flag=False):
    for i in setting_sprite_list:
        i.visible = not i.visible if not flag else False


def render_setting(screen):
    for i in setting_sprite_list:
        if i.visible:
            group_for_setting.add(i)
        elif not i.visible and i in group_for_setting:
            group_for_setting.remove(i)
    if sprite_setting_menu.visible:
        group_for_setting.draw(screen)
        str1 = 'ограничение фпс (1--144): '
        str2 = 'размер окна: '
        sls = [str1, str2]
        for i in range(len(sls)):  # отображение информации о спрайте
            screen.blit(pygame.font.Font(None, 28).render(sls[i], True, (255, 255, 255)),
                        (sprite_setting_menu.rect.x + 20,
                         sprite_setting_menu.rect.y + 30 + (i * 45)))
        if enter_fps:
            pygame.draw.rect(screen, (100, 150, 60),
                             (sprite_input_text.rect.x, sprite_input_text.rect.y, sprite_input_text.rect[2], sprite_input_text.rect[3]))
        screen.blit(pygame.font.Font(None, 26).render(str(fps), True, (0, 0, 0)),
                    (sprite_input_text.rect.x + 10,
                     sprite_input_text.rect.y + 3))
