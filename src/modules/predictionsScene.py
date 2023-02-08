# Imports
from src.classes.DataFile import DataFile
from src.classes.Button import Button
from src.classes.Hint import Hint
import src.modules.build as build
import pygame as pg

# Initializes predictions scene
def boot(window, settings):

    # Scene variables
    clock = pg.time.Clock()
    predictionsData = DataFile("data/predictions.datcs")
    meta = build.generateMeta(predictionsData)
    ui = generateUI(window, settings, meta)

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
        response = handleUI(window, settings, ui, position, pressed, released, meta)
        if response != 1: return response
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
def generateUI(window, settings, meta, buttons=True, text=True, hints=True):

    # More compact argument
    ms = settings.get("menuScale")

    ui = {"blocked": False}
    if buttons:
        ui["buttons"] = [
            Button(window, (5 * ms, 5 * ms), (90 * ms, 90 * ms), drawIcon=True, drawBackground=False,
            iconBase="media/screenerIconBase.png", iconHighlight="media/screenerIconHighlight.png",
            iconClick="media/screenerIconClick.png", iconSize=(55 * ms, 55 * ms)),
            Button(window, (5 * ms, 105 * ms), (90 * ms, 90 * ms), drawIcon=True, drawBackground=False,
            iconBase="media/rulesIconBase.png", iconHighlight="media/rulesIconHighlight.png",
            iconClick="media/rulesIconClick.png", iconSize=(55 * ms, 55 * ms)),
            Button(window, (5 * ms, 205 * ms), (90 * ms, 90 * ms), "active", drawIcon=True, drawBackground=False,
            iconBase="media/predictionsIconBase.png", iconHighlight="media/predictionsIconHighlight.png",
            iconClick="media/predictionsIconClick.png", iconSize=(55 * ms, 55 * ms)),
            Button(window, (5 * ms, 1080 - 195 * ms), (90 * ms, 90 * ms), drawIcon=True, drawBackground=False,
            iconBase="media/settingsIconBase.png", iconHighlight="media/settingsIconHighlight.png",
            iconClick="media/settingsIconClick.png", iconSize=(55 * ms, 55 * ms)),
            Button(window, (5 * ms, 1080 - 95 * ms), (90 * ms, 90 * ms), drawIcon=True, drawBackground=False,
            iconBase="media/exitIconBase.png", iconHighlight="media/exitIconHighlight.png",
            iconClick="media/exitIconClick.png", iconSize=(55 * ms, 55 * ms)),

            Button(window, (1920 - 245 * ms, 1080 / 2 + 35 * ms), (210 * ms, 41 * ms), drawText=True,
            text="Build Predictions", textSize=round(settings.get("TXTread") * ms), textColor=settings.get("CRstrokeL"),
            colorBase=settings.get("CRmenuD"), colorHighlight=settings.get("CRmenuXL"),
            colorClick=settings.get("CRmenuXD"), borderRadius=round(50 * ms)),

            Button(window, (1920 / 2 - 230 * ms, 1080 / 2 + 20 * ms), (220 * ms, 41 * ms), drawText=True,
            text="Yes", textSize=round(settings.get("TXTread") * ms), textColor=settings.get("CRstrokeL"),
            colorBase=settings.get("CRmenuD"), colorHighlight=settings.get("CRmenuXL"),
            colorClick=settings.get("CRmenuXD"), borderRadius=round(50 * ms)),
            Button(window, (1920 / 2 + 10 * ms, 1080 / 2 + 20 * ms), (220 * ms, 41 * ms), drawText=True,
            text="No", textSize=round(settings.get("TXTread") * ms), textColor=settings.get("CRstrokeL"),
            colorBase=settings.get("CRmenuD"), colorHighlight=settings.get("CRmenuXL"),
            colorClick=settings.get("CRmenuXD"), borderRadius=round(50 * ms))
        ]

    # Generates batch of text
    if text:
        header = pg.font.Font("media/latoBold.ttf", round(settings.get("TXTheader") * ms))
        headerBlack = pg.font.Font("media/latoBlack.ttf", round(settings.get("TXTheader") * ms))
        warningSizes = [header.size("Do you want to update the data and make new predictions?"),
        header.size("This might take some time.")]
        ui["text"] = [
            (header.render("Ticker", True, settings.get("CRstrokeL")), (145 * ms, 1080 / 2 + 41 * ms)),
            (header.render("Price", True, settings.get("CRstrokeL")), (255 * ms, 1080 / 2 + 41 * ms)),
            (header.render("Low", True, settings.get("CRstrokeL")), (365 * ms, 1080 / 2 + 41 * ms)),
            (header.render("High", True, settings.get("CRstrokeL")), (475 * ms, 1080 / 2 + 41 * ms)),
            (header.render("Diff", True, settings.get("CRstrokeL")), (585 * ms, 1080 / 2 + 41 * ms)),
            (header.render("Acc (?)", True, settings.get("CRstrokeL")), (695 * ms, 1080 / 2 + 41 * ms)),

            (headerBlack.render(meta["updateDate"], True, settings.get("CRgood" if meta["validDate"] else "CRbad")),
            (1920 - 390 * ms, 1080 / 2 + 41 * ms)),

            (header.render("Do you want to update the data and make new predictions?", True,
            settings.get("CRstrokeL")), (1920 / 2 - warningSizes[0][0] / 2, 1080 / 2 - warningSizes[0][1] - 30 * ms)),
            (header.render("This might take some time.", True, settings.get("CRstrokeL")),
            (1920 / 2 - warningSizes[1][0] / 2, 1080 / 2 - warningSizes[1][1]))
        ]

    # Generates batch of hints
    if hints:
        ui["hints"] = [
            Hint(window, settings, (20 * ms, 110 * ms), (5 * ms, 5 * ms), (90 * ms, 90 * ms),
            "Stock screener (Not Implemented Yet)", settings.get("debug"), "U", 20 * ms),
            Hint(window, settings, (20 *ms, 210 * ms), (5 * ms, 105 * ms), (90 * ms, 90 * ms),
            "Rules editor (Not Implemented Yet)", settings.get("debug"), "U", 20 * ms),
            Hint(window, settings, (20 * ms, 310 * ms), (5 * ms, 205 * ms), (90 * ms, 90 * ms),
            "Predictions dashboard", settings.get("debug"), "U", 20 * ms),
            Hint(window, settings, (20 * ms, 1080 - 260 * ms), (5 * ms, 1080 - 195 * ms), (90 * ms, 90 * ms),
            "Change settings", settings.get("debug"), "D", 20 * ms),
            Hint(window, settings, (20 * ms, 1080 - 160 * ms), (5 * ms, 1080 - 95 * ms), (90 * ms, 90 * ms),
            "Quit Stock Oracle", settings.get("debug"), "D", 20 * ms),

            Hint(window, settings, (135 * ms, 1080 / 2 + 90 * ms), (135 * ms, 1080 / 2 + 35 * ms), (90 * ms, 40 * ms),
            "Stock's ticker name", settings.get("debug"), "U", 35 * ms),
            Hint(window, settings, (180 * ms, 1080 / 2 + 90 * ms), (245 * ms, 1080 / 2 + 35 * ms), (90 * ms, 40 * ms),
            "Current ticker value", settings.get("debug"), "U", 100 * ms),
            Hint(window, settings, (225 * ms, 1080 / 2 + 90 * ms), (355 * ms, 1080 / 2 + 35 * ms), (90 * ms, 40 * ms),
            "One day's lowest price prediction", settings.get("debug"), "U", 165 * ms),
            Hint(window, settings, (270 * ms, 1080 / 2 + 90 * ms), (465 * ms, 1080 / 2 + 35 * ms), (90 * ms, 40 * ms),
            "Two day's highest price prediction", settings.get("debug"), "U", 230 * ms),
            Hint(window, settings, (315 * ms, 1080 / 2 + 90 * ms), (575 * ms, 1080 / 2 + 35 * ms), (90 * ms, 40 * ms),
            "Percentage difference between lowest and highest", settings.get("debug"), "U", 295 * ms),
            Hint(window, settings, (360 * ms, 1080 / 2 + 90 * ms), (685 * ms, 1080 / 2 + 35 * ms), (90 * ms, 40 * ms),
            "Prediction's accuracy (based on previous predictions, not market status)",
            settings.get("debug"), "U", 360 * ms),

            Hint(window, settings, (1920 - 600 * ms, 1080 / 2 + 90 * ms), (1920 - 435 * ms, 1080 / 2 + 35 * ms),
            (190 * ms, 40 * ms), "Date last predictions were built (red if out of date)",
            settings.get("debug"), "U", 250 * ms)
        ]

    return ui

# Handles input and visualization
def handleUI(window, settings, ui, position, pressed, released, meta):

    # More compact argument
    ms = settings.get("menuScale")

    # Draws navigation menu
    pg.draw.rect(window.display, settings.get("CRmenuL"), pg.Rect(0, 0, 100 * ms, 1080))
    pg.draw.rect(window.display, settings.get("CRstrokeL"), pg.Rect(94 * ms, 210 * ms, 6 * ms, 80 * ms))

    # Predictions background
    pg.draw.rect(window.display,  settings.get("CRmenuXD"), pg.Rect(100 * ms, 0, 1920 - 100 * ms, 1080 / 2))
    pg.draw.rect(window.display,  settings.get("CRmenuXD"), pg.Rect(125 * ms,
    1080 / 2 + 25 * ms, 1920 - 150 * ms, 1080 / 2 - 50 * ms))
    pg.draw.rect(window.display,  settings.get("CRmenuL"), pg.Rect(125 * ms,
    1080 / 2 + 25 * ms, 1920 - 150 * ms, 1080 / 2 - 50 * ms), round(4 * ms))

    # Predictions body
    

    # Predictions header
    pg.draw.rect(window.display,  settings.get("CRmenuL"), pg.Rect(125 * ms,
    1080 / 2 + 25 * ms, 1920 - 150 * ms, 60 * ms))
    pg.draw.line(window.display, settings.get("CRmenuL"),
    (235 * ms, 1080 / 2 + 85 * ms), (235 * ms, 1080 - 26 * ms), round(4 * ms))
    pg.draw.line(window.display, settings.get("CRmenuL"),
    (345 * ms, 1080 / 2 + 85 * ms), (345 * ms, 1080 - 26 * ms), round(4 * ms))
    pg.draw.line(window.display, settings.get("CRmenuL"),
    (455 * ms, 1080 / 2 + 85 * ms), (455 * ms, 1080 - 26 * ms), round(4 * ms))
    pg.draw.line(window.display, settings.get("CRmenuL"),
    (565 * ms, 1080 / 2 + 85 * ms), (565 * ms, 1080 - 26 * ms), round(4 * ms))
    pg.draw.line(window.display, settings.get("CRmenuL"),
    (675 * ms, 1080 / 2 + 85 * ms), (675 * ms, 1080 - 26 * ms), round(4 * ms))
    pg.draw.line(window.display, settings.get("CRmenuL"),
    (785 * ms, 1080 / 2 + 85 * ms), (785 * ms, 1080 - 26 * ms), round(4 * ms))

    pg.draw.circle(window.display, settings.get("CRgood" if meta["validDate"] else "CRbad"),
    (1920 - 415 * ms, 1080 / 2 + 56 * ms), 9 * ms)

    # Draws custom non-warning elements
    for text in ui["text"][:-2]: window.blit(*text)
    for button in ui["buttons"][:-2]: button.update(position, pressed, released, ui["blocked"])
    for hint in ui["hints"]: hint.update(position, ui["blocked"])

    # Handles navigation buttons
    # if ui["buttons"][0].send: pass
    # if ui["buttons"][1].send: pass
    if ui["buttons"][3].send: return True, "settings"
    if ui["buttons"][4].send: return False, "NA"

    # Blocks ui and displays a warning
    if ui["buttons"][5].send:
        ui["blocked"] = True
        pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_ARROW)
        ui["buttons"][5].status = "base"
        ui["buttons"][5].send = False
    
    # Predictions build warning
    if ui["blocked"]:

        # Warning background
        window.fillTransparent(settings.get("CRshadow"))
        pg.draw.rect(window.display, settings.get("CRmenuXXD"), pg.Rect(0, 1080 / 2 - 150 * ms, 1920, 300 * ms))

        # Draws custom warning elements
        for text in ui["text"][-2:]: window.blit(*text)
        for button in ui["buttons"][-2:]: button.update(position, pressed, released)

        # Handles warning buttons
        if ui["buttons"][6].send:
            pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_ARROW)
            pg.image.save(window.display,"media/predictions.jpg")
            return True, "computing"
        if ui["buttons"][7].send:
            ui["buttons"][7].status = "base"
            ui["buttons"][7].send = False
            ui["blocked"] = False

    return 1
