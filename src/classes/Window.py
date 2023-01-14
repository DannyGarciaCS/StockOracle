# Imports
import pygame as pg

# Window class
class Window:

    # Constructor
    def __init__(self, fullscreen, screenX, screenY, displayX, displayY, title):

        pg.init()
        pg.display.set_caption(title)

        self.fullscreen = fullscreen

        self.screenX = screenX
        self.screenY = screenY
        self.displayX = displayX
        self.displayY = displayY
        self.aspectX = self.displayX / self.screenX
        self.aspectY = self.displayY / self.screenY

        self.updateDisplay()
        self.display = pg.Surface((self.displayX, self.displayY))

    # Updates window surfaces
    def update(self):

        self.screen.blit(pg.transform.smoothscale(self.display, (self.screenX, self.screenY)), (0, 0))
        pg.display.flip()
    
    # Toggles to or off fullscreen
    def toggleFullscreen(self):

        self.fullscreen = not self.fullscreen
        self.updateDisplay()

    # Resizes resolution shown
    def resize(self, x=-1, y=-1):

        self.screenX = x if x > 0 else self.screenX
        self.screenY = y if y > 0 else self.screenY
        self.aspectX = self.displayX / self.screenX
        self.aspectY = self.displayY / self.screenY
        self.updateDisplay()

    # Fills window
    def fill(self, color): self.display.fill(color)

    # Draws on window
    def blit(self, surface, position): self.display.blit(surface, position)

    # Quits pygame
    def quit(self): pg.QUIT

    # Updates used display
    def updateDisplay(self):
        if self.fullscreen: self.screen = pg.display.set_mode(
        (self.screenX, self.screenY), pg.FULLSCREEN, pg.HWSURFACE, vsync=1)
        else: self.screen = pg.display.set_mode((self.screenX, self.screenY))
        pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_ARROW)
