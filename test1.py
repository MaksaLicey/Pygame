import pygame
import os
import sys
from os import walk


def load_image(name, colorkey=None):  # функция для загрузки изображений (из учебника)
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


class Cat(pygame.sprite.Sprite):  # класс для создания спрайтов
    def __init__(self, rect_x, rect_y, name):
        super().__init__()
        self.image = load_image("Kol.png")
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.mask = pygame.mask.from_surface(self.image)
        self.name = name


running = True
sprite_1 = Cat(100, 100, "it's spite 1!")
sprite_2 = Cat(400, 100, "it's spite 2!")
sprite_group = pygame.sprite.Group()
sprite_group.add(sprite_1)
sprite_group.add(sprite_2)

spite_list = (sprite_1, sprite_2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for sprit in spite_list:
                pos_in_mask = event.pos[0] - sprit.rect.x, event.pos[1] - sprit.rect.y
                if sprit.rect.collidepoint(event.pos) and sprit.mask.get_at(pos_in_mask):
                    # проверка, находится ли курсор на спрайте --^
                    print(sprit.name)
    screen.fill(pygame.Color('blue'))
    sprite_group.draw(screen)
    # screen.blit(sprite_1.image, sprite_1.rect)
    pygame.display.update()
