# Imports
import pygame as pg

# Slider class
class Slider:

    # Constructor
    def __init__(self, window, position, size, initialFill=0, **kwargs):

        self.window = window
        self.position = position
        self.size = size

        self.status = "base"
        self.hovering = False
        self.fill = initialFill
        self.percent = initialFill / size[0]
        self.lastHeld = False

        # Default visual arguments
        self.visuals = {
            "colorBase": (50, 50, 52),
            "colorPointer": (35, 110, 230),
            "colorShadow": (35, 80, 200),
            "drawBorder": False,
            "borderWidth": 1,
            "borderColor": (0, 0, 0),

            "trackMargin": 0,
            "trackRadius": 0,
            "pointerRadius": 0
        }

        # Replaces all passed visual arguments
        for key in kwargs.keys():
            if key in self.visuals.keys():
                self.visuals[key] = kwargs[key]
    
    # Updates button's status
    def update(self, position, pressed, released):

        # Slider is being hovered
        if self.position[0] < position[0] < self.position[0] + self.size[0] and \
        self.position[1] < position[1] < self.position[1] + self.size[1]:

            pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_HAND)
            self.hovering = True

            # Defines button visuals
            if pressed[0] and not self.lastHeld: self.status = "held"

            # Slider is no longer held
            if released == 1: self.status = "base"

        # Slider stoped being hovered
        elif self.hovering:

            pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_ARROW)
            self.hovering = False
            if released == 1: self.status = "base"

        # Slider is not being hovered
        else:
            if released == 1: self.status = "base"

        if self.status == "held": self.fill = max(min(position[0] - self.position[0], self.size[0]), 0)
        self.lastHeld = pressed[0]
        self.draw()

    # Draws Slider's status
    def draw(self):

        # Draws track
        pg.draw.rect(self.window.display, self.visuals["colorBase"],
        pg.Rect(self.position[0], self.position[1] + self.visuals["trackMargin"], self.size[0],
        self.size[1] - self.visuals["trackMargin"] * 2), border_radius=self.visuals["trackRadius"])

        # Draws track shadow
        pg.draw.rect(self.window.display, self.visuals["colorShadow"],
        pg.Rect(self.position[0], self.position[1] + self.visuals["trackMargin"], (self.position[0] + \
        self.fill - self.size[1] / 2) - self.position[0] + self.size[1] / 2,
        self.size[1] - self.visuals["trackMargin"] * 2), border_radius=self.visuals["trackRadius"])

        # Draws pointer
        pg.draw.rect(self.window.display, self.visuals["colorPointer"],
        pg.Rect(self.position[0] + self.fill - self.size[1] / 2, self.position[1], self.size[1],
        self.size[1]), border_radius=self.visuals["pointerRadius"])
