# Imports
import pygame as pg

# Button class
class Button:

    # Constructor
    def __init__(self, window, position, size, lock="NA", **kwargs):

        # Passed arguments
        self.window = window
        self.position = position
        self.size = size
        self.lock = lock

        # Implied arguments
        self.status = "base"
        self.send = False
        self.hovering = False

        # Default visual arguments
        self.visuals = {
            "colorBase": (50, 50, 52),
            "colorHighlight": (69, 70, 72),
            "colorClick": (45, 45, 47),
            "drawBackground": True,
            "drawBorder": False,
            "borderWidth": 1,
            "borderColor": (0, 0, 0),
            "borderRadius": 0,

            "drawIcon": False,
            "iconBase": "media/predictionsIconBase.png",
            "iconHighlight": "media/predictionsIconHighlight.png",
            "iconClick": "media/predictionsIconClick.png",
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
        self.iconBase = pg.image.load(self.visuals["iconBase"]).convert_alpha()
        self.iconBase = pg.transform.scale(self.iconBase, self.visuals["iconSize"])
        self.iconHighlight = pg.image.load(self.visuals["iconHighlight"]).convert_alpha()
        self.iconHighlight = pg.transform.scale(self.iconHighlight, self.visuals["iconSize"])
        self.iconClick = pg.image.load(self.visuals["iconClick"]).convert_alpha()
        self.iconClick = pg.transform.scale(self.iconClick, self.visuals["iconSize"])

        # Text preparation (Extract if dynamic buttons needed)
        self.font = pg.font.Font("media/latoBlack.ttf", self.visuals["textSize"])
        self.text = self.font.render(self.visuals["text"], True, self.visuals["textColor"])
        self.textSize = self.font.size(self.visuals["text"])
    
    # Updates button's status
    def update(self, position, pressed, released):

        # Button is being hovered
        if self.position[0] < position[0] < self.position[0] + self.size[0] and \
        self.position[1] < position[1] < self.position[1] + self.size[1]:

            pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_HAND)
            self.hovering = True

            # Defines button visuals
            if pressed[0]: self.status = "click"
            else: self.status = "highlight"

            # Executes button signal if button released
            if released == 1: self.send = True
            else: self.send = False

        # User stopped hovering
        elif self.hovering:

            pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_ARROW)
            self.hovering = False
            
            # Defines button visuals
            self.status = "base"

        # Button is in permanent active state
        if self.lock == "active":
            self.status = "highlight"
            self.send = False

        # Button is in permanent inactive state
        elif self.lock == "inactive":
            self.status = "base"
            self.send = False

        self.draw()

    # Draws button's status
    def draw(self):

        # Draws body of button
        if self.visuals["drawBackground"]:
            if self.status == "base":
                pg.draw.rect(self.window.display, self.visuals["colorBase"],
                pg.Rect(*self.position, *self.size), border_radius=self.visuals["borderRadius"])
            elif self.status == "highlight":
                pg.draw.rect(self.window.display, self.visuals["colorHighlight"],
                pg.Rect(*self.position, *self.size), border_radius=self.visuals["borderRadius"])
            elif self.status == "click":
                pg.draw.rect(self.window.display, self.visuals["colorClick"],
                pg.Rect(*self.position, *self.size), border_radius=self.visuals["borderRadius"])

            # Draws border
            if self.visuals["drawBorder"]:
                pg.draw.rect(self.window.display, self.visuals["borderColor"], pg.Rect(
                *self.position, *self.size), border_radius=self.visuals["borderRadius"],
                width=self.visuals["borderWidth"])

        # Draws icon
        if self.visuals["drawIcon"]:
            if self.status == "base":
                self.window.blit(self.iconBase, (self.position[0] + self.size[0] / 2 -
                self.visuals["iconSize"][0] / 2, self.position[1] + self.size[1] / 2 -
                self.visuals["iconSize"][1] / 2))
            elif self.status == "highlight":
                self.window.blit(self.iconHighlight, (self.position[0] + self.size[0] / 2 -
                self.visuals["iconSize"][0] / 2, self.position[1] + self.size[1] / 2 -
                self.visuals["iconSize"][1] / 2))
            elif self.status == "click":
                self.window.blit(self.iconClick, (self.position[0] + self.size[0] / 2 -
                self.visuals["iconSize"][0] / 2, self.position[1] + self.size[1] / 2 -
                self.visuals["iconSize"][1] / 2))

        # Draws text
        if self.visuals["drawText"]:
            self.window.blit(self.text, (self.position[0] + self.size[0] / 2 - self.textSize[0] / 2,
            self.position[1] + self.size[1] / 2 - self.textSize[1] / 2))
