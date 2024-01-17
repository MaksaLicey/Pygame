from special import *
from pygame import *
import os
import random
import shutil


# файл игры

def create_file(name_file, start_option_1, start_option_2, start_option_3):
    # shutil.copy(os.path.join('starts_file', f'{start_option_1[7:-4]}.txt'), os.path.join("saves", name_file))
    file_game = open(os.path.join("saves", name_file), mode="w", encoding="utf-8")
    file_game.write(f"file_name = {name_file} \n")
    file_game.write(f"map_name = {start_option_1[7:-4]} \n")
    file_game.write(f"difficlt = {start_option_2[7:-4]} \n")
    file_game.write(f"leader = {start_option_3[7:-4]} \n")
    f = open(os.path.join('starts_file', f'{start_option_1[7:-4]}.txt'), 'r+', encoding="utf-8")
    sls = f.readlines()
    for i in sls:
        file_game.write(i)
    f.close()
    file_game.close()
    pygame.quit()
    main()


def render():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 30)

    pygame.init()

    clock = pygame.time.Clock()
    size_menu = 1536, 803
    screen_main = pygame.display.set_mode(size_menu)
    file_reader()
    # Kol = SpritesCreateForMap(100, 100, "Kol.png")
    # spite_list_province = [Kol]
    group_visible_sprite = pygame.sprite.Group()
    # group_visible_sprite.add(Kol)

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
                pass
                # for sprit in spite_list_province:
                #     pos_in_mask = event.pos[0] - sprit.rect.x, event.pos[1] - sprit.rect.y
                #     if sprit.rect.collidepoint(event.pos) and sprit.mask.get_at(pos_in_mask):
                #         sprit.image = change_color(sprit.image_start,
                #                                   (random.randrange(0, 255), random.randrange(0, 255), 0))
        group_visible_sprite.draw(screen_main)
        pygame.display.update()


def main():
    render()
    pygame.quit()
