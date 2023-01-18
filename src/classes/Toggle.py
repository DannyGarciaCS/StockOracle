# Imports
import pygame as pg

# Toggle class
class Toggle:

    # Constructor
    def __init__(self, window, position, size, active=False, **kwargs):

        # Passed arguments
        self.window = window
        self.position = position
        self.size = size

        # Implied arguments
        self.active = active
        self.hovering = False
        self.changed = False

        # Default visual arguments
        self.visuals = {
            "colorBase": (67, 66, 71),
            "colorActive": (35, 110, 230),
            "colorHighlight": (45, 45, 47),
            "borderRadius": 0,
            "margin": 10
        }

        # Replaces all passed visual arguments
        for key in kwargs.keys():
            if key in self.visuals.keys():
                self.visuals[key] = kwargs[key]
    
    # Updates toggle's status
    def update(self, position, released):

        self.changed = False

        # Toggle is hovered
        if self.position[0] < position[0] < self.position[0] + self.size[0] and \
        self.position[1] < position[1] < self.position[1] + self.size[1]:

            pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_HAND)
            self.hovering = True

            # Defines toggle visuals
            if released == 1:
                self.active = not self.active
                self.changed = True

        # Toggle is not being hovered
        elif self.hovering:
            
            pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_ARROW)
            self.hovering = False

        self.draw()

    # Draws toggle's status
    def draw(self):

        size = self.size[1] - self.visuals["margin"] * 2

        # Toggle is off
        if self.active:
            pg.draw.rect(self.window.display, self.visuals["colorActive"],
            pg.Rect(*self.position, *self.size), border_radius=self.visuals["borderRadius"])

            pg.draw.rect(self.window.display, self.visuals["colorHighlight"],
            pg.Rect(self.position[0] + self.size[0] - size - self.visuals["margin"],
            self.position[1] + self.visuals["margin"], size, size), border_radius=self.visuals["borderRadius"])
        
        # Toggle is on
        else:
            pg.draw.rect(self.window.display, self.visuals["colorBase"],
            pg.Rect(*self.position, *self.size), border_radius=self.visuals["borderRadius"])

            pg.draw.rect(self.window.display, self.visuals["colorHighlight"],
            pg.Rect(self.position[0] + self.visuals["margin"], self.position[1] + self.visuals["margin"], size, size),
            border_radius=self.visuals["borderRadius"])
