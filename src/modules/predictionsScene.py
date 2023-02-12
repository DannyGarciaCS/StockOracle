# Imports
from src.classes.DataFile import DataFile
from src.classes.Button import Button
from src.classes.Hint import Hint
import src.modules.build as build
import matplotlib
from src.modules import util
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
import pickle
import numpy as np

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg

# Initializes predictions scene
def boot(window, settings):

    # Scene variables
    clock = pg.time.Clock()
    predictionsData = DataFile("data/predictions.datcs")
    ui = generateUI(window, settings, predictionsData)

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
        response = handleUI(window, settings, ui, position, pressed, released, predictionsData)
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
def generateUI(window, settings, predictionsData, buttons=True, text=True, hints=True, graph=True):

    # More compact argument
    ms = settings.get("menuScale")

    # Object properties
    header = pg.font.Font("media/latoBold.ttf", round(settings.get("TXTheader") * ms))
    headerBlack = pg.font.Font("media/latoBlack.ttf", round(settings.get("TXTheader") * ms))
    warningSizes = [header.size("Do you want to update the data and make new predictions?"),
    header.size("This might take some time.")]
    
    warningMargin = 12 * ms
    warningOffset = (warningSizes[0][1] + 2 * warningMargin + warningSizes[1][1] + 40 * ms) / 2

    headerY = 1080 / 2 - warningOffset
    subHeaderY = 1080 / 2 + warningSizes[0][1] + warningMargin - warningOffset
    buttonY = 1080 / 2 + warningSizes[0][1] + 2 * warningMargin + warningSizes[1][1] - warningOffset

    ui = {"blocked": False, "updated": "CRgood" if build.isLastTradingDay(predictionsData.get("modelUpdate")) else "CRbad"}
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

            Button(window, (1920 - 245 * ms, 1080 / 2 + 35 * ms), (210 * ms, 40 * ms), drawText=True,
            text="Build Predictions", textSize=round(settings.get("TXTread") * ms), textColor=settings.get("CRstrokeL"),
            colorBase=settings.get("CRmenuD"), colorHighlight=settings.get("CRmenuXL"),
            colorClick=settings.get("CRmenuXD"), borderRadius=round(50 * ms)),

            Button(window, (1920 / 2 - 230 * ms, buttonY), (220 * ms, 40 * ms), drawText=True,
            text="Yes", textSize=round(settings.get("TXTread") * ms), textColor=settings.get("CRstrokeL"),
            colorBase=settings.get("CRmenuD"), colorHighlight=settings.get("CRmenuXL"),
            colorClick=settings.get("CRmenuXD"), borderRadius=round(50 * ms)),
            Button(window, (1920 / 2 + 10 * ms, buttonY), (220 * ms, 40 * ms), drawText=True,
            text="No", textSize=round(settings.get("TXTread") * ms), textColor=settings.get("CRstrokeL"),
            colorBase=settings.get("CRmenuD"), colorHighlight=settings.get("CRmenuXL"),
            colorClick=settings.get("CRmenuXD"), borderRadius=round(50 * ms))
        ]

    # Generates batch of text
    if text:
        ui["text"] = [
            (header.render("Ticker", True, settings.get("CRstrokeL")), (145 * ms, 1080 / 2 + 41 * ms)),
            (header.render("Price", True, settings.get("CRstrokeL")), (255 * ms, 1080 / 2 + 41 * ms)),
            (header.render("Low", True, settings.get("CRstrokeL")), (365 * ms, 1080 / 2 + 41 * ms)),
            (header.render("High", True, settings.get("CRstrokeL")), (475 * ms, 1080 / 2 + 41 * ms)),
            (header.render("Diff", True, settings.get("CRstrokeL")), (585 * ms, 1080 / 2 + 41 * ms)),
            (header.render("Acc (?)", True, settings.get("CRstrokeL")), (695 * ms, 1080 / 2 + 41 * ms)),

            (headerBlack.render(predictionsData.get("modelUpdate"), True, settings.get(ui["updated"])),
            (1920 - 390 * ms, 1080 / 2 + 41 * ms)),

            (header.render("Do you want to update the data and make new predictions?", True,
            settings.get("CRstrokeL")), (1920 / 2 - warningSizes[0][0] / 2, headerY)),
            (header.render("This might take some time.", True, settings.get("CRstrokeL")),
            (1920 / 2 - warningSizes[1][0] / 2, subHeaderY))
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
    
    if graph: buildGraph(ms, ui)
    return ui

# Builds displayed graph
def buildGraph(ms, ui):

    # Loads ticker
    predictionsData = util.safeLoad("data/predictions.datcs")
    if os.path.exists(f"data/prices/{predictionsData.get('displayedTicker')}"):

        # Loads price data
        tickerName = predictionsData.get('displayedTicker')
        with open(f"data/prices/{tickerName}/{tickerName}.price", "rb") as prices:

            data = pickle.load(prices)
            tickerPrices = [price[1][0] for price in data]
            dataMean = np.mean(tickerPrices)

            # Determines line color
            lineColor = "#05C800" if data[-1][1][0] >= dataMean else "#D72323"
            fillColor = "#329632" if data[-1][1][0] >= dataMean else "#A53232"

        # Adjusts graph size
        wFig = 1920 - 200 * ms
        hFig = 540 - 100 * ms
        fig = pylab.figure(figsize=[int(wFig/100), int(hFig/100)], dpi=100,)
        fig.set_facecolor("#1E1E1E")

        # Changes graph style
        uiColor = "#dddddd"
        ax = fig.gca()
        ax.plot(tickerPrices, color=lineColor)
        ax.plot([0, len(tickerPrices)], [tickerPrices[-1], tickerPrices[-1]], color=uiColor)
        ax.fill_between(x=range(len(tickerPrices)), y1=tickerPrices, y2=0, color=fillColor)
        ax.set_facecolor("#373737")
        ax.spines["bottom"].set_color(uiColor)
        ax.spines["top"].set_color(uiColor)
        ax.spines["right"].set_color(uiColor)
        ax.spines["left"].set_color(uiColor)
        ax.tick_params(axis='x', colors=uiColor)
        ax.tick_params(axis='y', colors=uiColor)
        ax.set_xticks([], [])
        ax.set_title(f"{tickerName} Price", color=uiColor, size="xx-large", weight="bold")
        fig.tight_layout()
        ax.margins(x=0)
        ax.margins(y=0)

        # Draws graph data
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        graphData = renderer.tostring_rgb()
        size = canvas.get_width_height()

        # Saves finalized graphical surface
        surface = pg.image.fromstring(graphData, size, "RGB")
        surface = pg.transform.smoothscale(surface, (wFig, hFig))
        ui["graph"] = surface

    else: ui["graph"] = None

# Handles input and visualization
def handleUI(window, settings, ui, position, pressed, released, predictionsData):

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

    if ui["graph"] is not None: window.blit(ui["graph"], (150 * ms, 50 * ms))

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
    pg.draw.circle(window.display, settings.get(ui["updated"]), (1920 - 415 * ms, 1080 / 2 + 56 * ms), 9 * ms)

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
