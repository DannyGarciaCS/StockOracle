# Imports
import pygame as pg
from sys import exit
from src.classes.Button import Button

# Initializes predictions scene
def boot(window, settings):

    # Scene variables
    clock = pg.time.Clock()
    ui = generateUI(window, settings)

    # Main scene loop
    while True:

        # Event handling
        position, pressed, released = getMouse(window)
        for event in pg.event.get():

            # Cross is pressed
            if event.type == pg.QUIT: return False, ""

            # Mouse button is released
            if event.type == pg.MOUSEBUTTONUP: released = event.button

        # Updates window
        handleUI(window, settings, ui, position, pressed, released)
        window.update()
        window.fill(settings.get("CRmenuD"))
        clock.tick(60)

# Refreshes mouse information
def getMouse(window):

    # Mouse position
    position = list(pg.mouse.get_pos())
    position[0] = position[0] * window.aspectX
    position[1] = position[1] * window.aspectY

    # Mouse interactivity
    pressed = pg.mouse.get_pressed()
    released = 0

    return position, pressed, released

# Generates ui elements
def generateUI(window, settings, buttons=True):

    ui = {}

    # Generates batch of buttons
    if buttons:
        ui["buttons"] = [
            Button(window, (5 * settings.get("menuScale"), 5 * settings.get("menuScale")),
            (90 * settings.get("menuScale"), 90 * settings.get("menuScale")), drawIcon=True, drawBackground=False,
            iconBase="media/screenerIconBase.png",
            iconHighlight="media/screenerIconHighlight.png",
            iconClick="media/screenerIconClick.png",
            iconSize=(55 * settings.get("menuScale"), 55 * settings.get("menuScale")), drawHint = True,
            hintParameters = (window, settings, (20 * settings.get("menuScale"), 110 * settings.get("menuScale")),
            "Stock screener (Not Implemented Yet)", "U", 20 * settings.get("menuScale"))),

            Button(window, (5 * settings.get("menuScale"), 105 * settings.get("menuScale")),
            (90 * settings.get("menuScale"), 90 * settings.get("menuScale")), drawIcon=True, drawBackground=False,
            iconBase="media/rulesIconBase.png",
            iconHighlight="media/rulesIconHighlight.png",
            iconClick="media/rulesIconClick.png",
            iconSize=(55 * settings.get("menuScale"), 55 * settings.get("menuScale")), drawHint = True,
            hintParameters = (window, settings, (20 * settings.get("menuScale"), 210 * settings.get("menuScale")),
            "Rules editor (Not Implemented Yet)", "U", 20 * settings.get("menuScale"))),

            Button(window, (5 * settings.get("menuScale"), 205 * settings.get("menuScale")),
            (90 * settings.get("menuScale"), 90 * settings.get("menuScale")), drawIcon=True, drawBackground=False,
            iconBase="media/predictionsIconBase.png",
            iconHighlight="media/predictionsIconHighlight.png",
            iconClick="media/predictionsIconClick.png",
            iconSize=(55 * settings.get("menuScale"), 55 * settings.get("menuScale")), drawHint = True,
            hintParameters = (window, settings, (20 * settings.get("menuScale"), 310 * settings.get("menuScale")),
            "Predictions dashboard", "U", 20 * settings.get("menuScale")))
        ]

    return ui

def handleUI(window, settings, ui, position, pressed, released):

    # Draws navigation menu
    pg.draw.rect(window.display, settings.get("CRmenuL"), pg.Rect(0, 0, 100 * settings.get("menuScale"), 1080))
    pg.draw.rect(window.display, settings.get("CRstrokeL"), pg.Rect(94 * settings.get("menuScale"),
    210 * settings.get("menuScale"), 6 * settings.get("menuScale"), 80 * settings.get("menuScale")))

    # pg.draw.rect(window.display, (50, 50, 150), pg.Rect(140, 15, 1765, 515))
    # pg.draw.rect(window.display, (50, 150, 50), pg.Rect(140, 545, 1765, 520))
    # pg.draw.rect(window.display, (75, 200, 75), pg.Rect(140, 545, 1765, 80))

    for button in ui["buttons"]: button.update(position, pressed, released)
    for button in ui["buttons"]: button.drawHint()
