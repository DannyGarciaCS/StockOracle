# Imports
import pygame as pg
from src.classes.File import File
import src.modules.stockHelper as sh

# Initializes predictions scene
def boot(window, settings):

    # Scene variables
    clock = pg.time.Clock()
    ui = generateUI(settings)

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
        window.blit(ui["misc"][0], (0, 0))
        clock.tick(60)

# Generates ui elements
def generateUI(settings, misc=True):

    # More compact argument
    ms = settings.get("menuScale")

    ui = {}
    ui["loadingFrame"] = 0
    ui["titleFont"] = pg.font.Font("media/latoBold.ttf", round(settings.get("TXTtitle") * ms))
    ui["messageFont"] = pg.font.Font("media/latoBold.ttf", round(settings.get("TXTheader") * ms))
    
    # Generates unclassifiable elements
    if misc:
        loadingIcon = pg.image.load("media/loadingIcon.png").convert_alpha()
        ui["misc"] = [
            pg.image.load("media/predictions.jpg").convert(),
            pg.transform.smoothscale(loadingIcon, (90 * ms, 90 * ms))
        ]

    return ui

def handleUI(window, settings, ui):

    # More compact argument
    ms = settings.get("menuScale")

    # Bar background
    pg.draw.rect(window.display, settings.get("CRmenuXXD"), pg.Rect(0, 1080 / 2 - 150 * ms, 1920, 300 * ms))

    # Draws loading icon
    loadingFrame = rotateCenter(ui["misc"][1], ui["loadingFrame"])
    window.blit(loadingFrame, (1920 / 2 - loadingFrame.get_width() / 2,
    1080 / 2 - loadingFrame.get_height() / 2 - 40 * ms))
    ui["loadingFrame"] += 3

    # Draws loading text
    predictionsData = File("data/predictions.datcs")
    title = predictionsData.get("loadingTitle")
    message = predictionsData.get("loadingMessage")
    title = ui["titleFont"].render(title, True, settings.get("CRstrokeL"))
    message = ui["messageFont"].render(message, True, settings.get("CRstrokeL"))
    window.blit(title, (1920 / 2 - ui["titleFont"].size(predictionsData.get("loadingTitle"))[0] / 2, 1080 / 2 + 25))
    window.blit(message, (1920 / 2 - ui["messageFont"].size(predictionsData.get("loadingMessage"))[0] / 2, 1080 / 2 + 65))

    return 1

# Rotates an image from the center
def rotateCenter(image, angle):

    origRect = image.get_rect()
    rotImage = pg.transform.rotate(image, angle)
    rotRect = origRect.copy()
    rotRect.center = rotImage.get_rect().center
    rotImage = rotImage.subsurface(rotRect).copy()
    return rotImage
