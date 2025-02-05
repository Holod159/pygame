import os
import sys
import random
import pygame
import sqlite3


name = input('Перед началом игры введите свой никнейм: ')
con = sqlite3.connect('users')
cur = con.cursor()
result = cur.execute("""SELECT name FROM users""").fetchall()
id = 0
sz = 0
for i in result:
    if i[0] == name:
        print('Вы уже зарегистрированы')
        id = sz
        break
    sz += 1
else:
    cur.execute(f"""INSERT INTO users (name, klass, level) VALUES (?, ?, ?)""", (name, random.randint(1, 3), random.randint(1, 3)))
    con.commit()
    print('Вы успешно зарегистрированы')
    id = len(result)
print(id)
result = cur.execute("""SELECT * FROM users """).fetchall()

print(result)
FPS = 50
pygame.init()
pname = ['woin.png', 'mag.png', 'wor.png']
ppname = ['woinb.png', 'mb.png', 'worb.png']
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
clock = pygame.time.Clock()
tb = result[id][2] - 1
polz = pname[tb]


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


def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["Добро пожаловать", ""]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start_screen()
    screen = pygame.display.set_mode(size)
    screen_rect = (0, 0, width, height)
    Tile()
    Tor = Torg()
    Por = Port()
    if tb != 1:
        hero = WoinWorSprite(load_image(polz, colorkey=-1), 4, 1, 400, 400)
    else:
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
            break
        all_sprites.update()
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

polz = ppname[tb]
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
FPS = 5


class MagB(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.columns = columns
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = ((self.cur_frame + 1) % self.columns)
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (147 * 2, 133 * 2))


class Wrag1(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.columns = columns
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = ((self.cur_frame + 1) % self.columns)
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (147 * 2, 133 * 2))
        self.image = pygame.transform.flip(self.image, True, False)


if __name__ == '__main__':
    pygame.init()
    pl = 0
    tl = result[id][3]
    print(tl)
    hph = tl * random.randint(3, 10)
    hpw = tl * random.randint(1, 6)
    if tb != 0:
        hero = MagB(load_image(polz, colorkey=-1), 4, 1, 300, 400)
    else:
        hero = MagB(load_image(polz, colorkey=-1), 8, 1, 300, 400)
    wrag = Wrag1(load_image('wrag1.png', colorkey=-1), 8, 1, 500, 400)
    screen = pygame.display.set_mode(size)
    screen_rect = (0, 0, width, height)
    Sten()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        print(hph, hpw)
        a = random.randint(1, 5) * tl // 10
        b = random.randint(1, 8) * tl // 10
        if a == 0:
            a = 1
        if b == 0:
            b = 1
        hph -= a
        hpw -= b
        all_sprites.update()
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        if hph <= 0:
            print('You lose')
            break
        if hpw <= 0:
            print('You win')
            pl += 1
            if pl >= tl:
                tl += 1
                cur = con.cursor()
                cur.execute(f"UPDATE users SET level = 100")
                print(1)
                pl = 0
            all_sprites = pygame.sprite.Group()
            sz = (sz + 1) % 2
            if tl >= 999:
                hph = tl * random.randint(3, 10)
            else:
                hph = tl * random.randint(1, 6)
            hpw = tl * random.randint(1, 6)
            if tb != 0:
                hero = MagB(load_image(polz, colorkey=-1), 4, 1, 300, 400)
            else:
                hero = MagB(load_image(polz, colorkey=-1), 8, 1, 300, 400)
            if sz == 0:
                wrag = Wrag1(load_image('wrag1.png', colorkey=-1), 8, 1, 500, 400)
            else:
                wrag = Wrag1(load_image('wrag2.png', colorkey=-1), 5, 1, 500, 400)