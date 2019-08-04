import os
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


class Cell:
    type = 0
    open = False


class MineField:
    def __init__(self, tile_set, num_x, num_y):
        self.tile_set = tile_set
        self.tile_width = tile_set[0].get_width()
        self.tile_height = tile_set[0].get_height()
        self.num_x = num_x
        self.num_y = num_y
        self.surface = pygame.Surface((self.tile_width * num_x, self.tile_height * num_y))
        self.cells = []
        for x in range(0, num_x + 2):
            row = []
            for y in range(0, num_y + 2):
                row.append(Cell())
            self.cells.append(row)

    def render(self, screen):
        for x in range(1, self.num_x + 1):
            for y in range(1, self.num_y + 1):
                if self.cells[x][y].open:
                    self.surface.blit(self.tile_set[0], (self.tile_width * (x - 1), self.tile_height * (y - 1)))
                elif self.cells[x][y].type == 0:
                    self.surface.blit(self.tile_set[12], (self.tile_width * (x - 1), self.tile_height * (y - 1)))
        screen.blit(self.surface, (0, 0))


def main():
    pygame.init()
    winstyle = 0  # FULLSCREEN
    screen_rect = (10, 10)
    bestdepth = pygame.display.mode_ok(screen_rect, winstyle, 32)
    screen = pygame.display.set_mode(screen_rect, winstyle, bestdepth)
    pygame.display.set_caption('py sweeper')

    cells = load_tileset('cells.png', 9, 2)
    field = MineField(cells, 9, 9)
    screen_rect = (field.num_x * field.tile_width, field.num_y * field.tile_height)
    screen = pygame.display.set_mode(screen_rect, winstyle, bestdepth)
    field.render(screen)
    pygame.display.flip()

    pygame.time.wait(1000)
    pygame.quit()


if __name__ == '__main__':
    main()
