from special import *
import pygame
from pygame import *
from screeninfo import get_monitors
import os
from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT
import pygame
from pygame._sdl2.video import Window


def create_file(name_file, start_option_1, start_option_2, start_option_3):
    print(name_file, start_option_1, start_option_2, start_option_3)
    main()


def render():
    pygame.init()
    clock = pygame.time.Clock()
    size_menu = 1536, 803
    screen_main = pygame.display.set_mode(size_menu, RESIZABLE)

    group_visible_sprite = pygame.sprite.Group()
    Kol = Sprite_create_2(100, 100, "Kol.png")
    group_visible_sprite.add(Kol)

    # screen_main = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, RESIZABLE)

    collider_Kol = pygame.draw.polygon(screen_main, (0, 255, 0),
                                       [(11, 83), (21, 92), (34, 95), (51, 112), (80, 120), (81, 104), (76, 93),
                                        (79, 80), (101, 79), (90, 59), (97, 45), (62, 39), (51, 22), (71, 3),
                                        (60, 0), (14, 39), (20, 64), (8, 81)])

    running_2 = True
    while running_2:
        clock.tick(60)

        # pygame.draw.rect(screen_main, (255, 255, 0), box1)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running_2 = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    running_2 = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if collider_Kol.collidepoint(event.pos):
                print(Kol.mask.get_at(event.pos))
                #     print(screen_main.get_rect())
                #     print(event.pos)
                #     print(collider_Kol)
                # #     # for m in get_monitors():
                # #     #     print(str(m))
                # pass
        pygame.draw.polygon(screen_main, (0, 255, 0),
                            [(11, 83), (21, 92), (34, 95), (51, 112), (80, 120), (81, 104), (76, 93), (79, 80),
                             (101, 79), (90, 59), (97, 45), (62, 39), (51, 22), (71, 3), (60, 0), (14, 39),
                             (20, 64), (8, 81)])

        group_visible_sprite.draw(screen_main)
        # screen_main.blit(Kol_img, (0, 0))
        pygame.display.update()


def main():
    render()
    pygame.quit()
