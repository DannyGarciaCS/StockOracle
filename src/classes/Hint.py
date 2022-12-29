# Imports
import pygame as pg

# Hint class
class Hint:

    # Constructor
    def __init__(self, window, position, text, show=True, pointerDirection="U", pointerMargin=10):

        self.window = window
        self.position = position
        self.show = show
        self.pointerDirection = pointerDirection
        self.pointerMargin = pointerMargin

        self.color = (50, 50, 52)
        self.fontColor = (227, 229, 233)
        self.fontSize = 25
        self.margin = 15
        self.borderRadius = 8
        self.pointerSize = 20

        self.font = pg.font.Font("media/latoBlack.ttf", self.fontSize)
        self.text = self.font.render(text, True, self.fontColor)
        self.size = list(self.font.size(text))
        self.size[0] += self.margin * 2
        self.size[1] += self.margin * 2

    # Draws object status
    def draw(self):

        # Only draws hint if showing
        if self.show:

            # Draws body of hint
            pg.draw.rect(self.window.display, self.color, pg.Rect(*self.position, *self.size), border_radius=self.borderRadius)
            self.window.blit(self.text, (self.position[0] + self.margin, self.position[1] + self.margin))

            # Draws hint pointer
            if self.pointerDirection == "U":
                pg.draw.polygon(self.window.display, self.color, [
                (self.position[0] + self.pointerMargin, self.position[1]),
                (self.position[0] + self.pointerMargin + self.pointerSize, self.position[1]),
                (self.position[0] + self.pointerMargin + self.pointerSize / 2, self.position[1] - self.pointerSize)])
            elif self.pointerDirection == "D":
                pg.draw.polygon(self.window.display, self.color, [
                (self.position[0] + self.pointerMargin, self.position[1] + self.size[1]),
                (self.position[0] + self.pointerMargin + self.pointerSize, self.position[1] + self.size[1]),
                (self.position[0] + self.pointerMargin + self.pointerSize / 2, self.position[1] + self.pointerSize + self.size[1])])
