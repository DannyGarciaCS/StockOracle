# Imports
import pygame as pg

# Window class
class Window:

    # Constructor
    def __init__(self, screenX, screenY, displayX, displayY, title):

        pg.init()
        pg.display.set_caption(title)

        # Arguments
        self.screenX = screenX
        self.screenY = screenY
        self.displayX = displayX
        self.displayY = displayY

        # Native properties
        self.screen = pg.display.set_mode((self.screenX, self.screenY))
        self.display = pg.Surface((self.displayX, self.displayY))

    # Updates window surfaces
    def update(self):

        self.screen.blit(pg.transform.smoothscale(self.display, (self.screenX, self.screenY)), (0, 0))
        pg.display.flip()

    # Resizes resolution shown
    def resize(self, x=-1, y=-1):

        x = x if x > 0 else self.screenX
        y = y if y > 0 else self.screenY
        self.screen = pg.display.set_mode((self.screenX, self.screenY))

    # Fills window
    def fill(self, color): self.display.fill(color)

    # Draws on window
    def blit(self, surface, position): self.display.blit(surface, position)

    # Quits pygame
    def quit(self): pg.QUIT
