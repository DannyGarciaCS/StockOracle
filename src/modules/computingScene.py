# Imports
import pygame as pg
from src.classes.File import File
import src.modules.stockHelper as sh

# Initializes predictions scene
def boot(window, settings):

    # Scene variables
    clock = pg.time.Clock()
    predictionsData = File("data/predictions.datcs")
    meta = sh.generateMeta(predictionsData)
    ui = generateUI(window, settings, meta)

    predictionBack = pg.image.load("media/predictions.jpg").convert()

    # Main scene loop
    while True:

        # Event handling
        for event in pg.event.get():

            # Cross is pressed
            if event.type == pg.QUIT: return False, ""

        # Updates window
        response = handleUI(window, settings, ui)
        if response != 1: return response
        window.update()
        window.blit(predictionBack, (0, 0))
        clock.tick(60)

# Generates ui elements
def generateUI(window, settings, misc=True):

    # More compact argument
    ms = settings.get("menuScale")

    ui = {}
    
    # Generates unclassifiable elements
    if misc:
        ui["misc"] = [

        ]

    return ui

def handleUI(window, settings, ui):

    # More compact argument
    ms = settings.get("menuScale")

    # Bar background
    pg.draw.rect(window.display, settings.get("CRmenuXXD"), pg.Rect(0, 1080 / 2 - 150 * ms, 1920, 300 * ms))

    return 1
