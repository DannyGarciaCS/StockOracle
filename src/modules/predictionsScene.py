# Imports
import pygame as pg

# Initializes predictions scene
def boot(window, settings):

    # Scene variables
    clock = pg.time.Clock()

    # Main scene loop
    while True:

        # Updates window
        window.update()
        window.fill((0, 0, 0))
        clock.tick(60)

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
