# Imports
import pygame as pg

# Hint class
class Hint:

    # Constructor
    def __init__(self, window, settings, position, text, pointerDirection="-", pointerMargin=0):

        # Passed arguments
        self.window = window
        self.settings = settings
        self.position = position
        self.pointerDirection = pointerDirection
        self.pointerMargin = pointerMargin

        # Implied arguments
        self.color = settings.get("CRmenuXD")
        self.margin = 12 * settings.get("menuScale")
        self.borderRadius = round(8 * settings.get("menuScale"))
        self.borderSize = round(2 * settings.get("menuScale"))
        self.pointerSize = 20 * settings.get("menuScale")
        self.show = False

        # Text
        self.font = pg.font.Font("media/latoBlack.ttf", round(settings.get("TXTread") * settings.get("menuScale")))
        self.text = self.font.render(text, True, settings.get("CRstrokeL"))
        self.size = list(self.font.size(text))
        self.size[0] += self.margin * 2
        self.size[1] += self.margin * 2

    # Draws object status
    def draw(self):

        # Only draws hint if showing
        if self.show:

            # Draws body of hint
            pg.draw.rect(self.window.display, self.color, pg.Rect(
            *self.position, *self.size), border_radius=self.borderRadius)

            pg.draw.rect(self.window.display, (0, 0, 0), pg.Rect(
            *self.position, *self.size), border_radius=self.borderRadius, width=self.borderSize)
            
            self.window.blit(self.text, (self.position[0] + self.margin, self.position[1] + self.margin))

            # Draws hint pointer
            if self.pointerDirection == "U":

                pg.draw.polygon(self.window.display, self.color, [
                (self.position[0] + self.pointerMargin, self.position[1] + self.borderSize),
                (self.position[0] + self.pointerMargin + self.pointerSize, self.position[1] + self.borderSize),
                (self.position[0] + self.pointerMargin + self.pointerSize / 2,
                self.position[1] - self.pointerSize + self.borderSize)])

                pg.draw.line(self.window.display, (0, 0, 0),
                (self.position[0] + self.pointerMargin, self.position[1] + self.borderSize),
                (self.position[0] + self.pointerMargin + self.pointerSize / 2,
                self.position[1] - self.pointerSize + self.borderSize), width=self.borderSize)

                pg.draw.line(self.window.display, (0, 0, 0),
                (self.position[0] + self.pointerMargin + self.pointerSize, self.position[1] + self.borderSize),
                (self.position[0] + self.pointerMargin + self.pointerSize / 2,
                self.position[1] - self.pointerSize + self.borderSize), width=self.borderSize)

            elif self.pointerDirection == "D":

                pg.draw.polygon(self.window.display, self.color, [
                (self.position[0] + self.pointerMargin, self.position[1] + self.size[1] - self.borderSize),
                (self.position[0] + self.pointerMargin + self.pointerSize,
                self.position[1] + self.size[1] - self.borderSize),
                (self.position[0] + self.pointerMargin + self.pointerSize / 2,
                self.position[1] + self.pointerSize + self.size[1] - self.borderSize)])

                pg.draw.line(self.window.display, (0, 0, 0),
                (self.position[0] + self.pointerMargin, self.position[1] + self.size[1] - self.borderSize),
                (self.position[0] + self.pointerMargin + self.pointerSize / 2,
                self.position[1] + self.pointerSize + self.size[1] - self.borderSize), width=self.borderSize)

                pg.draw.line(self.window.display, (0, 0, 0),
                (self.position[0] + self.pointerMargin + self.pointerSize,
                self.position[1] + self.size[1] - self.borderSize),
                (self.position[0] + self.pointerMargin + self.pointerSize / 2,
                self.position[1] + self.pointerSize + self.size[1] - self.borderSize), width=self.borderSize)
