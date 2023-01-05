# Imports
import pygame as pg
from src.classes.File import File
from src.classes.Window import Window
from src.modules.predictionsScene import boot as bootPredictions
from src.modules.settingsScene import boot as bootSettings

# Main function
def main():

    # Initializes data
    settings = File("data/settings.datcs")
    window = Window(settings.get("screenX"), settings.get("screenY"),
    settings.get("displayX"), settings.get("displayY"), "Market Oracle")
    scene = "settings"
    running = True

    # Main program loop
    while running:

        # Loads predictions scene
        if scene == "predictions":
            running, scene = bootPredictions(window, settings)
        
        elif scene == "settings":
            running, scene = bootSettings(window, settings)

    # Closes pygame
    window.quit()

# Main function call
if __name__ == "__main__":
    main()
