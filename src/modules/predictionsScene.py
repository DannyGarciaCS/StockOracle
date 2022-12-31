# Imports
from src.classes.Button import Button
import pygame as pg

# Initializes predictions scene
def boot(window, settings):

    # Scene variables
    clock = pg.time.Clock()

    buttons = [
        Button(window, (15, 15), (95, 95), borderRadius=10, drawIcon=True, icon="media/screenerIconBase.png", iconSize=(60, 60)),

        Button(window, (15, 125), (95, 95), borderRadius=10, drawIcon=True, icon="media/rulesIconBase.png", iconSize=(60, 60)),
        Button(window, (15, 235), (95, 95), borderRadius=10, drawIcon=True, icon="media/predictionsIconBase.png", iconSize=(60, 60)),
        Button(window, (15, 970), (95, 95), borderRadius=10, drawIcon=True, icon="media/settingsIconBase.png", iconSize=(60, 60))
    ]

    # Main scene loop
    while True:

        # Mouse
        position = list(pg.mouse.get_pos())
        position[0] = position[0] * window.aspectX
        position[1] = position[1] * window.aspectY

        # Event handling
        for event in pg.event.get():

            # Cross is pressed
            if event.type == pg.QUIT: return False, ""

        pg.draw.rect(window.display, (40, 39, 43), pg.Rect(0, 0, 125, 1080))
        
        # pg.draw.rect(window.display, (200, 75, 75), pg.Rect(15, 15, 95, 95))
        # pg.draw.rect(window.display, (200, 75, 75), pg.Rect(15, 125, 95, 95))
        # pg.draw.rect(window.display, (200, 75, 75), pg.Rect(15, 235, 95, 95))
        # pg.draw.rect(window.display, (200, 75, 75), pg.Rect(15, 970, 95, 95))

        # pg.draw.rect(window.display, (50, 50, 150), pg.Rect(140, 15, 1765, 515))

        # pg.draw.rect(window.display, (50, 150, 50), pg.Rect(140, 545, 1765, 520))
        # pg.draw.rect(window.display, (75, 200, 75), pg.Rect(140, 545, 1765, 80))

        for button in buttons: button.update(position)

        # Updates window
        window.update()
        window.fill((57, 56, 61))
        clock.tick(60)
