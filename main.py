import pygame
from pygame.locals import *

SCREENRECT = Rect(0, 0, 640, 480)

def main():
    pygame.init()
    winstyle = 0  # FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    pygame.display.set_caption('py sweeper')

    pygame.time.wait(1000)
    pygame.quit()


if __name__ == '__main__':
    main()
