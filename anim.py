import os
import sys
import random
import pygame
from pygame.examples.moveit import WIDTH

FPS = 50
pygame.init()
pname = ['mag.png', 'woin.png', 'wor.png']
polz = pname[0]
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
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
    else:
        image = image.convert_alpha()
    return image


class MagSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.columns = columns
        self.f = 1
        self.d = {'up': 2, 'down': 0, 'left': 1, 'right': 1}
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.counter = 10
        self.sz = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.f:
            keys = pygame.key.get_pressed()
            move = None
            if keys[pygame.K_UP]:
                move = 'up'
                self.rect.y -= 5
            elif keys[pygame.K_DOWN]:
                move = 'down'
                self.rect.y += 5
            elif keys[pygame.K_LEFT]:
                move = 'left'
                self.rect.x -= 5
            elif keys[pygame.K_RIGHT]:
                move = 'right'
                self.rect.x += 5
            if move:
                self.sz += 1
                if self.sz > self.counter:
                    self.sz = 0
                    self.cur_frame = ((self.cur_frame + 1) % self.columns)
                    self.image = pygame.transform.scale(self.frames[self.cur_frame + self.d[move] * self.columns], (147 * 0.8, 133 * 0.8))
                    if move == 'right':
                        self.image = pygame.transform.flip(self.image, True, False)

    def mover(self):
        self.f = 0

    def imover(self):
        self.f = 1


class WoinWorSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.f = 1
        self.frames = []
        self.columns = columns
        self.d = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.counter = 10
        self.sz = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.f:
            keys = pygame.key.get_pressed()
            move = None
            if keys[pygame.K_UP]:
                move = 'up'
                self.rect.y -= 5
            elif keys[pygame.K_DOWN]:
                move = 'down'
                self.rect.y += 5
            elif keys[pygame.K_LEFT]:
                move = 'left'
                self.rect.x -= 5
            elif keys[pygame.K_RIGHT]:
                move = 'right'
                self.rect.x += 5
            if move:
                self.sz += 1
                if self.sz > self.counter:
                    self.sz = 0
                    self.cur_frame = ((self.cur_frame + 1) % self.columns)
                    self.image = pygame.transform.scale(self.frames[self.cur_frame + self.d[move] * self.columns], (147, 133))
                    if move == 'left':
                        self.image = pygame.transform.flip(self.image, True, False)

    def mover(self):
        self.f = 0

    def imover(self):
        self.f = 1


class Tile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(tiles_group)
        self.image = pygame.transform.scale(load_image('pol.jpg'), (width, height))
        self.rect = self.image.get_rect().move(0, 0)


class Sten(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(tiles_group)
        self.image = pygame.transform.scale(load_image('sten.jpg'), (width, height))
        self.rect = self.image.get_rect().move(0, 0)


class Torg(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image('lav.png'), (300, 300))
        self.rect = self.image.get_rect().move(0, 0)


class Port(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image('port.png', colorkey=-1), (300, 300))
        self.rect = self.image.get_rect().move(800, 0)


if __name__ == '__main__':
    screen = pygame.display.set_mode(size)
    screen_rect = (0, 0, width, height)
    Tile()
    Tor = Torg()
    Por = Port()
    hero = MagSprite(load_image(polz, colorkey=-1), 5, 3, 400, 400)
    sz = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if pygame.sprite.collide_mask(hero, Tor):
            print('Yes')
            sz += 1
            hero.mover()
            if sz == 10:
                sz = 0
                hero.imover()
        if pygame.sprite.collide_mask(hero, Por):
            pygame.quit()
            break
        all_sprites.update()
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
print(1)
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()

if __name__ == '__main__':
    print(2)
    pygame.init()
    screen = pygame.display.set_mode(size)
    screen_rect = (0, 0, width, height)
    Sten()
    while True:
        print(3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)