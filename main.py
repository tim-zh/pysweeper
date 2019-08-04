import os
import pygame
from pygame.locals import *

SCREENRECT = Rect(0, 0, 640, 480)

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
    for x in range(0, num_x):
        for y in range(0, num_y):
            rect = (x * tile_width, y * tile_height, tile_width, tile_height)
            result.append(img.subsurface(rect))
    return result


def main():
    pygame.init()
    winstyle = 0  # FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    pygame.display.set_caption('py sweeper')

    bgdtile = load_tileset('cells.png', 9, 2)[1]
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        for y in range(0, SCREENRECT.height, bgdtile.get_height()):
            background.blit(bgdtile, (x, y))
    screen.blit(background, (0, 0))
    pygame.display.flip()

    pygame.time.wait(1000)
    pygame.quit()


if __name__ == '__main__':
    main()
