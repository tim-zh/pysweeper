import os
import math
import pygame
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]


def load_image(file):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))
    return surface.convert()


def load_tileset(file, num_x, num_y):
    result = []
    img = load_image(file)
    width, height = img.get_size()
    tile_width = width // num_x
    tile_height = height // num_y
    for y in range(0, num_y):
        for x in range(0, num_x):
            rect = (x * tile_width, y * tile_height, tile_width, tile_height)
            result.append(img.subsurface(rect))
    return result


class Cell(pygame.sprite.Sprite):
    images = []
    tile_width = 0
    tile_height = 0

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self._is_open = False
        self.type = 12
        self.image = self.images[self.type]
        self.rect = self.image.get_rect()
        self.rect.left = x * Cell.tile_width
        self.rect.top = y * Cell.tile_height

    def open(self):
        self._is_open = True
        self.type = 0

    def update(self):
        self.image = self.images[self.type]


class MineField:
    def __init__(self, num_x, num_y):
        self.num_x = num_x
        self.num_y = num_y
        self.cells = []
        for x in range(0, num_x):
            row = []
            for y in range(0, num_y):
                row.append(Cell(x, y))
            self.cells.append(row)


def main():
    pygame.init()
    winstyle = 0  # FULLSCREEN
    screen_rect = (10, 10)
    bestdepth = pygame.display.mode_ok(screen_rect, winstyle, 32)
    pygame.display.set_mode(screen_rect, winstyle, bestdepth)
    pygame.display.set_caption('py sweeper')

    cells_group = pygame.sprite.RenderUpdates()
    Cell.containers = cells_group

    Cell.images = load_tileset('cells.png', 9, 2)
    Cell.tile_width = Cell.images[0].get_width()
    Cell.tile_height = Cell.images[0].get_height()
    field = MineField(9, 9)
    screen_rect = (field.num_x * Cell.tile_width, field.num_y * Cell.tile_height)
    screen = pygame.display.set_mode(screen_rect, winstyle, bestdepth)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            if event.type == MOUSEBUTTONUP:
                pos_x, pos_y = pygame.mouse.get_pos()
                x = math.floor(pos_x / Cell.tile_width)
                y = math.floor(pos_y / Cell.tile_height)
                field.cells[x][y].open()

        cells_group.update()
        dirty = cells_group.draw(screen)
        pygame.display.update(dirty)

        clock.tick(40)


if __name__ == '__main__':
    main()
