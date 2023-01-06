# Imports
import pygame as pg

# Scrollbar class
class Scrollbar:

    # Constructor
    def __init__(self, window, position, size, overhead, **kwargs):

        self.window = window
        self.position = position
        self.size = size
        self.overhead = overhead

        self.magnitude = 0
        self.scroll = 0
        self.held = False

        # Default visual arguments
        self.visuals = {
            "color": (45, 45, 47),
            "radius": 0,
            "pointerColor": (35, 110, 230)
        }

        # Replaces all passed visual arguments
        for key in kwargs.keys():
            if key in self.visuals.keys():
                self.visuals[key] = kwargs[key]

        self.pack(1050)
        self.pack(1050)
    
    # Updates scrollbar's status
    def update(self, position, pressed, released):

        self.draw()

    # Draws button's status
    def draw(self):

        # Main scrollbar background
        pg.draw.rect(self.window.display, self.visuals["color"], pg.Rect(
        *self.position, *self.size), border_radius=self.visuals["radius"])

        # Draws scrollbar pointer if there is contentlarger than container
        if self.magnitude > self.overhead:

            coverage = self.overhead / self.magnitude

            pg.draw.rect(self.window.display, self.visuals["pointerColor"], pg.Rect(
            *self.position, self.size[0], self.size[1] * coverage), border_radius=self.visuals["radius"])
    
    # Adds size of content to scrollbar magnitude
    def pack(self, volume): self.magnitude += volume
