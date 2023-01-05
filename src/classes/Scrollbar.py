# Imports
import pygame as pg

# Scrollbar class
class Scrollbar:

    # Constructor
    def __init__(self, window, position, size, magnitude, **kwargs):

        self.window = window
        self.position = position
        self.size = size
        self.magnitude = magnitude

        self.scroll = 0
        self.held = False

        # Default visual arguments
        self.visuals = {
            "color": (45, 45, 47),
            "radius": 0,
            "pointerColor": (35, 165, 240)
        }

        # Replaces all passed visual arguments
        for key in kwargs.keys():
            if key in self.visuals.keys():
                self.visuals[key] = kwargs[key]
    
    # Updates scrollbar's status
    def update(self, position, pressed, released):

        self.draw()

    # Draws button's status
    def draw(self):

        # Main scrollbar background
        pg.draw.rect(self.window.display, self.visuals["color"], pg.Rect(
        *self.position, *self.size), border_radius=self.visuals["radius"])
