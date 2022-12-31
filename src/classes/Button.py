# Imports
import pygame as pg

# Button class
class Button:

    # Constructor
    def __init__(self, window, position, size, **kwargs):

        self.window = window
        self.position = position
        self.size = size

        # Default visual arguments
        self.visuals = {
            "color": (50, 50, 52),
            "drawBorder": False,
            "borderWidth": 1,
            "borderColor": (0, 0, 0),
            "borderRadius": 0,

            "drawIcon": False,
            "icon": "media/predictionsIconBase.png",
            "iconSize": (int(self.size[0] * 0.9), int(self.size[1] * 0.9)),

            "drawText": False,
            "text": "Button",
            "textSize": 25,
            "textColor": (227, 229, 233)
        }

        # Replaces all passed visual arguments
        for key in kwargs.keys():
            if key in self.visuals.keys():
                self.visuals[key] = kwargs[key]

        # Icon preparation (Extract if dynamic buttons needed)
        self.icon = pg.image.load(self.visuals["icon"]).convert_alpha()
        self.icon = pg.transform.scale(self.icon, self.visuals["iconSize"])

        # Text preparation (Extract if dynamic buttons needed)
        self.font = pg.font.Font("media/latoBlack.ttf", self.visuals["textSize"])
        self.text = self.font.render(self.visuals["text"], True, self.visuals["textColor"])
        self.textSize = self.font.size(self.visuals["text"])
    
    # Updates button's status
    def update(self, position):

        self.draw()

    # Draws button's status
    def draw(self):

        # Draws body of button
        pg.draw.rect(self.window.display, self.visuals["color"],
        pg.Rect(*self.position, *self.size), border_radius=self.visuals["borderRadius"])

        # Draws border
        if self.visuals["drawBorder"]:
            pg.draw.rect(self.window.display, self.visuals["borderColor"], pg.Rect(
            *self.position, *self.size), border_radius=self.visuals["borderRadius"], width=self.visuals["borderWidth"])

        # Draws icon
        if self.visuals["drawIcon"]:
            self.window.blit(self.icon, (self.position[0] + self.size[0] / 2 - self.visuals["iconSize"][0] / 2,
            self.position[1] + self.size[1] / 2 - self.visuals["iconSize"][1] / 2))

        # Draws text
        if self.visuals["drawText"]:
            self.window.blit(self.text, (self.position[0] + self.size[0] / 2 - self.textSize[0] / 2,
            self.position[1] + self.size[1] / 2 - self.textSize[1] / 2))
