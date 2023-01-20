# Imports
import pygame as pg
from sys import exit
from src.classes.Button import Button
from src.classes.Toggle import Toggle
from src.classes.Slider import Slider
from src.classes.Dropdown import Dropdown

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
        response = handleUI(window, settings, ui, position, pressed, released)
        if type(response) != type({}): return response
        ui = response
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
def generateUI(window, settings, buttons=True, toggles=True, sliders=True, dropdowns=True, text=True, misc=True):

    # More compact argument
    ms = settings.get("menuScale")

    ui = {}

    # Generates batch of buttons
    if buttons:
        ui["buttons"] = [
            Button(window, (5 * ms, 5 * ms), (90 * ms, 90 * ms), drawIcon=True, drawBackground=False,
            iconBase="media/screenerIconBase.png",
            iconHighlight="media/screenerIconHighlight.png",
            iconClick="media/screenerIconClick.png",
            iconSize=(55 * ms, 55 * ms), drawHint = True, hintParameters = (window, settings, (20 * ms, 110 * ms),
            "Stock screener (Not Implemented Yet)", "U", 20 * ms)),

            Button(window, (5 * ms, 105 * ms), (90 * ms, 90 * ms), drawIcon=True, drawBackground=False,
            iconBase="media/rulesIconBase.png",
            iconHighlight="media/rulesIconHighlight.png",
            iconClick="media/rulesIconClick.png",
            iconSize=(55 * ms, 55 * ms), drawHint = True, hintParameters = (window, settings, (20 *ms, 210 * ms),
            "Rules editor (Not Implemented Yet)", "U", 20 * ms)),

            Button(window, (5 * ms, 205 * ms), (90 * ms, 90 * ms), drawIcon=True, drawBackground=False,
            iconBase="media/predictionsIconBase.png",
            iconHighlight="media/predictionsIconHighlight.png",
            iconClick="media/predictionsIconClick.png",
            iconSize=(55 * ms, 55 * ms), drawHint = True, hintParameters = (window, settings,
            (20 * ms, 310 * ms), "Predictions dashboard", "U", 20 * ms)),

            Button(window, (5 * ms, 1080 - 195 * ms), (90 * ms, 90 * ms), "active", drawIcon=True, drawBackground=False,
            iconBase="media/settingsIconBase.png",
            iconHighlight="media/settingsIconHighlight.png",
            iconClick="media/settingsIconClick.png",
            iconSize=(55 * ms, 55 * ms), drawHint = True, hintParameters = (window, settings,
            (20 * ms, 1080 - 260 * ms), "Change settings", "D", 20 * ms)),

            Button(window, (5 * ms, 1080 - 95 * ms), (90 * ms, 90 * ms), drawIcon=True, drawBackground=False,
            iconBase="media/exitIconBase.png",
            iconHighlight="media/exitIconHighlight.png",
            iconClick="media/exitIconClick.png",
            iconSize=(55 * ms, 55 * ms), drawHint = True, hintParameters = (window, settings,
            (20 * ms, 1080 - 160 * ms), "Quit Stock Oracle", "D", 20 * ms))
        ]

    # Generates batch of toggles
    if toggles:
        ui["toggles"] = [
            Toggle(window, (330 * ms, 178 * ms), (55 * ms, 28 * ms), settings.get("fullscreen"),
            borderRadius=round(20 * ms), margin=5 * ms, colorBase=settings.get("CRmenuL"),
            colorActive=settings.get("CRhighlightL"), colorHighlight=settings.get("CRmenuXL"))
        ]
    
    if sliders:

        width = 185 * ms
        ui["sliders"] = [
            Slider(window, (330 * ms, 100 * ms), (width, 45 * ms),
            initialFill = width * ((settings.get("menuScale") - 0.65) / 0.7),
            colorBase=settings.get("CRmenuL"), colorPointer=settings.get("CRhighlightL"),
            colorShadow=settings.get("CRhighlightD"), trackMargin = 17 * ms, trackRadius = round(8 * ms),
            pointerMargin = 10 * ms, pointerRadius = round(15 * ms))
        ]

    # Generates batch of dropdowns
    if dropdowns:

        # Fetches screen settings
        screen = [settings.get("screenX"), settings.get("screenY")]
        display = [settings.get("displayX"), settings.get("displayY")]
        resolutions = []

        # Fetches valid resolutions
        for resolution in [[720, 480], [854, 480], [960, 540], [1280, 720], [1366, 768], [1600, 900],
        [1920, 1080], [2560, 1440], [3200, 1800], [3840, 2160], [5120, 2880], [7680, 4320]]:

            if resolution != screen and resolution[0] <= display[0] and resolution[1] <= display[1]:
                resolutions.append(resolution)

        ui["dropdowns"] = [
            Dropdown(window, (330 * ms, 240 * ms), (185 * ms, 45 * ms), f"{screen[0]} x {screen[1]}",
            settings.get("fullscreen"), drawBorder=False, borderRadius=round(20 * ms), 
            items=[f"{resolution[0]} x {resolution[1]}" for resolution in resolutions],
            textSize=round(settings.get("TXTread") * ms), colorBase = settings.get("CRmenuL"),
            colorHighlight = settings.get("CRmenuXL"), textColor = settings.get("CRstrokeL"),
            lockedColor = settings.get("CRstrokeD"))
        ]
    
    # Generates batch of text
    if text:
        settingsFont = pg.font.Font("media/latoBold.ttf", round(settings.get("TXTread") * ms))
        titleFont = pg.font.Font("media/latoBlack.ttf", round(settings.get("TXTtitle") * ms))
        ui["text"] = [
            (titleFont.render("Settings", True, settings.get("CRstrokeL")), (130 * ms, 18 * ms)),
            (settingsFont.render("UI Scale", True, settings.get("CRstrokeL")), (185 * ms, 108 * ms)),
            (settingsFont.render("Fullscreen", True, settings.get("CRstrokeL")), (185 * ms, 178 * ms)),
            (settingsFont.render("Resolution", True, settings.get("CRstrokeL")), (185 * ms, 248 * ms))
            
        ]
    
    # Generates unclassifiable elements
    if misc:
        warningFont = pg.font.Font("media/latoBold.ttf", round(settings.get("TXTread") * ms))
        warningIcon = pg.image.load("media/warningIcon.png").convert_alpha()
        ui["misc"] = [
            pg.transform.scale(warningIcon, (38 * ms, 38 * ms)),
            warningFont.render("Resolution can't be changed on fullscreen mode", True, settings.get("CRbad"))
        ]

    return ui

def handleUI(window, settings, ui, position, pressed, released):

    # More compact argument
    ms = settings.get("menuScale")

    # Draws navigation menu
    pg.draw.rect(window.display, settings.get("CRmenuL"), pg.Rect(0, 0, 100 * ms, 1080))
    pg.draw.rect(window.display, settings.get("CRstrokeL"), pg.Rect(94 * ms,
    1080 - 190 * ms, 6 * ms, 80 * ms))

    # Draws settings container
    pg.draw.rect(window.display,  settings.get("CRmenuXD"), pg.Rect(125 * ms, 70 * ms,
    1920 - 150 * ms, 1080 - 95 * ms), border_radius=round(10 * ms))

    # Draws custom elements
    for text in ui["text"]: window.blit(*text)
    for button in ui["buttons"]: button.update(position, pressed, released)
    for toggle in ui["toggles"]: toggle.update(position, released)
    for slider in ui["sliders"]: slider.update(position, pressed, released)
    for dropdown in ui["dropdowns"]: dropdown.update(position, released)
    for button in ui["buttons"]: button.drawHint()

    # Draws fullscreen warning warnings
    if settings.get("fullscreen"):
        window.blit(ui["misc"][0], (540 * ms, 245 * ms))
        window.blit(ui["misc"][1], (600 * ms, 250 * ms))

    # Handles toggles
    if ui["toggles"][0].changed:

        # Changes fullscreen status
        settings.set("fullscreen", not settings.get("fullscreen"))
        settings.save()
        window.toggleFullscreen()
        ui["dropdowns"][0].changeLock(settings.get("fullscreen"))
    
    # Dropdown change
    if ui["dropdowns"][0].changed:
        
        # Changes screen resolution
        value = ui["dropdowns"][0].selected.split(" x ")
        value = list(map(int, value))
        settings.set("screenX", value[0])
        settings.set("screenY", value[1])
        settings.save()
        window.resize(*value)

        # Updates dropdown
        ui["dropdowns"] = generateUI(window, settings, buttons=False, toggles=False,
        sliders=False, dropdowns=True, text=False, misc=False)["dropdowns"]

    # Handles buttons
    if ui["buttons"][0].send: pass
    if ui["buttons"][1].send: pass
    if ui["buttons"][2].send: return True, "predictions"
    if ui["buttons"][4].send: return False, "NA"

    # Handles sliders
    if ui["sliders"][0].changed:
        sliders = ui["sliders"]
        settings.set("menuScale", 0.65 + (0.7 * ui["sliders"][0].percent))
        settings.save()
        ui = generateUI(window, settings, sliders=False)
        ui["sliders"] = sliders

        width = 185 * ms
        ui["sliders"][0].reconstruct(window, (330 * ms, 100 * ms), (width, 45 * ms), initialFill = \
            width * ((settings.get("menuScale") - 0.65) / 0.7),
            kwargs = {"colorBase":settings.get("CRmenuL"), "colorPointer":settings.get("CRhighlightL"),
            "colorShadow":settings.get("CRhighlightD"), "trackMargin":17 * ms, "trackRadius":round(8 * ms),
            "pointerMargin":10 * ms, "pointerRadius":round(15 * ms)})

    return ui
