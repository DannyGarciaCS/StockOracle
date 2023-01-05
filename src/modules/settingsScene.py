# Imports
from src.classes.Button import Button
import pygame as pg

# Initializes settings scene
def boot(window, settings):

    # Scene variables
    clock = pg.time.Clock()

    buttons = [
        Button(window, (15, 15), (95, 95), borderRadius=10, drawIcon=True, iconBase="media/screenerIconBase.png",
        iconHighlight="media/screenerIconHighlight.png", iconClick="media/screenerIconClick.png",
        hintParameters = (window, (15, 140), "Go to stock screener (Not Implemented Yet)", "U", 34), drawHint = True,
        iconSize=(60, 60)),

        Button(window, (15, 125), (95, 95), borderRadius=10, drawIcon=True, iconBase="media/rulesIconBase.png",
        iconHighlight="media/rulesIconHighlight.png", iconClick="media/rulesIconClick.png",
        hintParameters = (window, (15, 250), "Go to rules editor (Not Implemented Yet)", "U", 34), drawHint = True,
        iconSize=(60, 60)),

        Button(window, (15, 235), (95, 95), borderRadius=10, drawIcon=True, iconBase="media/predictionsIconBase.png",
        iconHighlight="media/predictionsIconHighlight.png", iconClick="media/predictionsIconClick.png",
        hintParameters = (window, (15, 360), "Refresh predictions dashboard", "U", 34), drawHint = True,
        iconSize=(60, 60)),

        Button(window, (15, 970), (95, 95), borderRadius=10, drawIcon=True, iconBase="media/settingsIconBase.png",
        iconHighlight="media/settingsIconHighlight.png", iconClick="media/settingsIconClick.png",
        hintParameters = (window, (15, 880), "Change settings", "D", 34), drawHint = True,
        iconSize=(60, 60))
    ]

    # Main scene loop
    while True:

        # Mouse
        position = list(pg.mouse.get_pos())
        position[0] = position[0] * window.aspectX
        position[1] = position[1] * window.aspectY
        pressed = pg.mouse.get_pressed()
        released = 0

        # Event handling
        for event in pg.event.get():

            # Cross is pressed
            if event.type == pg.QUIT: return False, ""

            # Mouse button is released
            if event.type == pg.MOUSEBUTTONUP: released = event.button

        # Draws navigation menu
        pg.draw.rect(window.display, (40, 39, 43), pg.Rect(0, 0, 125, 1080))
        for button in buttons: button.update(position, pressed, released)

        # Draws overlay elements
        for button in buttons: button.drawHint()

        # Handles navigation buttons
        if buttons[0].send: pass
        if buttons[1].send: pass
        if buttons[2].send: return True, "predictions"
        if buttons[3].send: return True, "settings"

        # Updates window
        window.update()
        window.fill((57, 56, 61))
        clock.tick(60)
