# Imports
from src.classes.Hint import Hint
import pygame as pg

# Initializes predictions scene
def boot(window, settings):

    # Scene variables
    clock = pg.time.Clock()

    hints = [Hint(window, (300, 700), "Sample Message Bla Bla Bla\nAnother Message")]

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

        pg.draw.rect(window.display, (150, 50, 50), pg.Rect(0, 0, 125, 1080))
        pg.draw.rect(window.display, (200, 75, 75), pg.Rect(15, 15, 95, 95))
        pg.draw.rect(window.display, (200, 75, 75), pg.Rect(15, 125, 95, 95))
        pg.draw.rect(window.display, (200, 75, 75), pg.Rect(15, 235, 95, 95))
        pg.draw.rect(window.display, (200, 75, 75), pg.Rect(15, 970, 95, 95))

        pg.draw.rect(window.display, (50, 50, 150), pg.Rect(140, 15, 1765, 515))

        pg.draw.rect(window.display, (50, 150, 50), pg.Rect(140, 545, 1765, 520))
        pg.draw.rect(window.display, (75, 200, 75), pg.Rect(140, 545, 1765, 80))

        for hint in hints: hint.draw()

        # Updates window
        window.update()
        window.fill((200, 200, 220))
        clock.tick(60)
