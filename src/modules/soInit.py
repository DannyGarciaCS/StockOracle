# Imports
from src.classes.File import File
import pygame as pg
import ctypes

# Initial program configuration
def soInit(settings):

    # Determines valid initial resolution
    setResolution = None
    user32 = ctypes.windll.user32
    monitorRes = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    for resolution in [[640, 360], [720, 480], [854, 480], [960, 540], [1280, 720], [1366, 768], [1600, 900],
    [1920, 1080], [2560, 1440], [3200, 1800], [3840, 2160], [5120, 2880], [7680, 4320]]:

        # Fetches one resolution below current monitor's
        if resolution[0] < monitorRes[0] and resolution[1] < monitorRes[1]:
            setResolution = resolution
        else: break
    
    # Resets settings to the originals
    originalSettings = File("data/annotatedSettings.datcs")
    for key in originalSettings.data:
        settings.set(key, originalSettings.data[key])

    print(setResolution)
    
    # Sets fetched resolution and saves
    settings.set("screenX", setResolution[0])
    settings.set("screenY", setResolution[1])
    settings.save()
