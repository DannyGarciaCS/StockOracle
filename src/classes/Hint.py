# Imports
import pygame as pg

# Hint class
class Hint:

    # Constructor
    def __init__(self, window, settings, drawPosition, position,
    size, text, debugSpawn=False, pointerDirection="-", pointerMargin=0):

        # Passed arguments
        self.window = window
        self.settings = settings
        self.drawPosition = drawPosition
        self.position = position
        self.size = size
        self.debugSpawn = debugSpawn
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
        self.drawSize = list(self.font.size(text))
        self.drawSize[0] += self.margin * 2
        self.drawSize[1] += self.margin * 2
    
    # Updates hint's status
    def update(self, position, blocked=False):

        # Hint is being hovered
        if not blocked:
            self.show = (self.position[0] < position[0] < self.position[0] + self.size[0] and \
            self.position[1] < position[1] < self.position[1] + self.size[1])

        self.draw()

    # Draws object status
    def draw(self):

        # Draws area for debugging
        if self.debugSpawn: pg.draw.rect(self.window.display, (255, 0, 0), pg.Rect(*self.position, *self.size), 1)

        # Only draws hint if showing
        if self.show:

            # Draws body of hint
            pg.draw.rect(self.window.display, self.color, pg.Rect(
            *self.drawPosition, *self.drawSize), border_radius=self.borderRadius)

            pg.draw.rect(self.window.display, (0, 0, 0), pg.Rect(
            *self.drawPosition, *self.drawSize), border_radius=self.borderRadius, width=self.borderSize)
            
            self.window.blit(self.text, (self.drawPosition[0] + self.margin, self.drawPosition[1] + self.margin))

            # Draws hint pointer looking up
            if self.pointerDirection == "U":

                pg.draw.polygon(self.window.display, self.color, [
                (self.drawPosition[0] + self.pointerMargin, self.drawPosition[1] + self.borderSize),
                (self.drawPosition[0] + self.pointerMargin + self.pointerSize, self.drawPosition[1] + self.borderSize),
                (self.drawPosition[0] + self.pointerMargin + self.pointerSize / 2,
                self.drawPosition[1] - self.pointerSize + self.borderSize)])

                pg.draw.line(self.window.display, (0, 0, 0),
                (self.drawPosition[0] + self.pointerMargin, self.drawPosition[1] + self.borderSize),
                (self.drawPosition[0] + self.pointerMargin + self.pointerSize / 2,
                self.drawPosition[1] - self.pointerSize + self.borderSize), width=self.borderSize)

                pg.draw.line(self.window.display, (0, 0, 0),
                (self.drawPosition[0] + self.pointerMargin + self.pointerSize, self.drawPosition[1] + self.borderSize),
                (self.drawPosition[0] + self.pointerMargin + self.pointerSize / 2,
                self.drawPosition[1] - self.pointerSize + self.borderSize), width=self.borderSize)

            # Draws hint pointer looking down
            elif self.pointerDirection == "D":

                pg.draw.polygon(self.window.display, self.color, [
                (self.drawPosition[0] + self.pointerMargin, self.drawPosition[1] + self.drawSize[1] - self.borderSize),
                (self.drawPosition[0] + self.pointerMargin + self.pointerSize,
                self.drawPosition[1] + self.drawSize[1] - self.borderSize),
                (self.drawPosition[0] + self.pointerMargin + self.pointerSize / 2,
                self.drawPosition[1] + self.pointerSize + self.drawSize[1] - self.borderSize)])

                pg.draw.line(self.window.display, (0, 0, 0),
                (self.drawPosition[0] + self.pointerMargin, self.drawPosition[1] + self.drawSize[1] - self.borderSize),
                (self.drawPosition[0] + self.pointerMargin + self.pointerSize / 2,
                self.drawPosition[1] + self.pointerSize + self.drawSize[1] - self.borderSize), width=self.borderSize)

                pg.draw.line(self.window.display, (0, 0, 0),
                (self.drawPosition[0] + self.pointerMargin + self.pointerSize,
                self.drawPosition[1] + self.drawSize[1] - self.borderSize),
                (self.drawPosition[0] + self.pointerMargin + self.pointerSize / 2,
                self.drawPosition[1] + self.pointerSize + self.drawSize[1] - self.borderSize), width=self.borderSize)
