# Imports
import pygame as pg

# Dropdown class
class Dropdown:

    # Constructor
    def __init__(self, window, position, size, selected, **kwargs):

        self.window = window
        self.position = position
        self.size = size
        self.selected = selected

        self.open = False
        self.hovering = False
        self.changed = False
        self.highlighted = -1

        # Default visual arguments
        self.visuals = {
            "colorBase": (67, 66, 71),
            "colorHighlight": (89, 90, 92),
            "borderRadius": 0,
            "borderWidth": 3,

            "items": ["Choice 1", "Sample 22", "Choice 333"],
            "textSize": 25,
            "textColor": (227, 229, 233),
        }

        # Replaces all passed visual arguments
        for key in kwargs.keys():
            if key in self.visuals.keys():
                self.visuals[key] = kwargs[key]

        # Text preparation
        self.font = pg.font.Font("media/latoBlack.ttf", self.visuals["textSize"])
        self.text = self.font.render(self.selected, True, self.visuals["textColor"])
        self.renders = [self.font.render(text, True, self.visuals["textColor"]) for text in self.visuals["items"]]

    # Updates dropdown's status
    def update(self, position, pressed, released):

        if self.changed: self.changed = not self.changed

        # Dropdown is open
        if self.open:

            # User is hovering any of the options
            if self.position[0] < position[0] < self.position[0] + self.size[0] and \
            self.position[1] < position[1] < self.position[1] + self.size[1] * (len(self.visuals["items"]) + 1) - \
            self.visuals["borderWidth"] * (len(self.visuals["items"])):

                pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_HAND)
                self.hovering = True

                # Defines highlighted choice
                selection = (position[1] - self.position[1]) / self.size[1] - 1
                selection = int(selection) if selection >= 0 else -1
                self.highlighted = selection

                # User clicked on available option
                if released == 1:
                    self.open = not self.open

                    if not (position[1] - self.position[1]) / self.size[1] < 1:

                        self.selected, self.visuals["items"][selection] = \
                        self.visuals["items"][selection], self.selected
                        self.text, self.renders[selection] = self.renders[selection], self.text
                        self.changed = True

            # We stop hovering
            elif self.hovering:
                
                pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_ARROW)
                self.hovering = False

                 # Handles frame perfect outside click
                if released == 1: self.open = not self.open
            
            # Clicked outside
            else:
                if released == 1: self.open = not self.open

        # Dropdown is closed
        else:

            if self.highlighted != -1: self.highlighted = -1
            if self.position[0] < position[0] < self.position[0] + self.size[0] and \
            self.position[1] < position[1] < self.position[1] + self.size[1]:

                pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_HAND)
                self.hovering = True

                # Defines dropdown visuals
                if released == 1: self.open = not self.open

            elif self.hovering:
                
                pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_ARROW)
                self.hovering = False

        self.draw()

    # Draws dropdown's status
    def draw(self):

        # Dropdown is open
        if self.open:

            # Main selection body
            pg.draw.rect(self.window.display, self.visuals["colorBase"],
            pg.Rect(*self.position, *self.size), border_top_left_radius=self.visuals["borderRadius"],
            border_top_right_radius=self.visuals["borderRadius"])

            # Main selection text
            textSize = self.font.size(self.selected)
            self.window.blit(self.text, (self.position[0] + self.size[0] / 2 - textSize[0] / 2,
            self.position[1] + self.size[1] / 2 - textSize[1] / 2))

            # Main selection border
            pg.draw.rect(self.window.display, self.visuals["colorHighlight"],
            pg.Rect(*self.position, *self.size), self.visuals["borderWidth"],
            border_top_left_radius=self.visuals["borderRadius"],
            border_top_right_radius=self.visuals["borderRadius"])

            # Renders all choices
            for i, render in enumerate(self.renders):

                # Determines choice variables
                offset = (1 + i) * self.size[1] - self.visuals["borderWidth"] * (1 + i)
                color = self.visuals["colorBase"] if i != self.highlighted else self.visuals["colorHighlight"]

                # Choice is last choice
                if i != len(self.renders) - 1:
                    pg.draw.rect(self.window.display, color,
                    pg.Rect(self.position[0], self.position[1] + offset, *self.size))

                    pg.draw.rect(self.window.display, self.visuals["colorHighlight"],
                    pg.Rect(self.position[0], self.position[1] + offset, *self.size), self.visuals["borderWidth"])
                else:
                    pg.draw.rect(self.window.display, color,
                    pg.Rect(self.position[0], self.position[1] + offset, *self.size),
                    border_bottom_left_radius=self.visuals["borderRadius"],
                    border_bottom_right_radius=self.visuals["borderRadius"])

                    pg.draw.rect(self.window.display, self.visuals["colorHighlight"],
                    pg.Rect(self.position[0], self.position[1] + offset, *self.size), self.visuals["borderWidth"],
                    border_bottom_left_radius=self.visuals["borderRadius"],
                    border_bottom_right_radius=self.visuals["borderRadius"])

                # Draws centered choice text
                textSize = self.font.size(self.visuals["items"][i])
                self.window.blit(render, (self.position[0] + self.size[0] / 2 - textSize[0] / 2,
                self.position[1] + self.size[1] / 2 - textSize[1] / 2 + offset))

        # Dropdown is closed
        if not self.open:

            pg.draw.rect(self.window.display, self.visuals["colorBase"],
            pg.Rect(*self.position, *self.size), border_radius=self.visuals["borderRadius"])

            textSize = self.font.size(self.selected)
            self.window.blit(self.text, (self.position[0] + self.size[0] / 2 - textSize[0] / 2,
            self.position[1] + self.size[1] / 2 - textSize[1] / 2))
