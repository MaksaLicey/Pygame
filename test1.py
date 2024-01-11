import pygame
import os
import sys
from os import walk


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


pygame.init()
screen = pygame.display.set_mode((800, 600))


class Cat(pygame.sprite.Sprite):
    def __init__(self, rect_x, rect_y):
        self.image = load_image("Kol.png")
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.mask = pygame.mask.from_surface(self.image)


running = True
sprite_1 = Cat(100, 100)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_in_mask = event.pos[0] - sprite_1.rect.x, event.pos[1] - sprite_1.rect.y
            if sprite_1.rect.collidepoint(*pygame.mouse.get_pos()) and sprite_1.mask.get_at(pos_in_mask):
                screen.fill(pygame.Color('red'))
            else:
                screen.fill(pygame.Color('blue'))
    screen.blit(sprite_1.image, sprite_1.rect)
    pygame.display.update()
