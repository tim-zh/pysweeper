import os
import math
import random
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
        self.neighbor_mines = 0
        self.is_mine = False
        self.is_open = False
        self.type = 12
        self.image = self.images[self.type]
        self.rect = self.image.get_rect()
        self.rect.left = x * Cell.tile_width
        self.rect.top = y * Cell.tile_height

    def open(self):
        self.is_open = True
        if self.is_mine:
            self.type = 10
        else:
            self.type = self.neighbor_mines

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

    def place_mines(self, num):
        for i in range(0, num):
            while True:
                x = random.randrange(0, self.num_x)
                y = random.randrange(0, self.num_y)
                if not self.cells[x][y].is_mine:
                    self.cells[x][y].is_mine = True
                    break

    def contains(self, x, y):
        return 0 <= x < self.num_x and 0 <= y < self.num_y

    def get_neighbors(self, x, y):
        result = []
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if self.contains(x + dx, y + dy) and not (dx == 0 and dy == 0):
                    xy = (x + dx, y + dy)
                    result.append(xy)
        return result

    def get_cell(self, xy):
        return self.cells[xy[0]][xy[1]]

    def calculate_types(self):
        for x in range(0, self.num_x):
            for y in range(0, self.num_y):
                for xy in self.get_neighbors(x, y):
                    cell = self.get_cell(xy)
                    if cell.is_mine:
                        self.cells[x][y].neighbor_mines += 1

    def open(self, x, y):
        self.cells[x][y].open()
        if self.cells[x][y].neighbor_mines == 0:
            for xy in self.get_neighbors(x, y):
                if not self.get_cell(xy).is_open:
                    self.open(xy[0], xy[1])


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
    field.place_mines(10)
    field.calculate_types()
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
                field.open(x, y)

        cells_group.update()
        dirty = cells_group.draw(screen)
        pygame.display.update(dirty)

        clock.tick(40)


if __name__ == '__main__':
    main()
