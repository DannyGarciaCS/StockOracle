# Imports
import pygame as pg
from src.classes.File import File
from src.classes.Window import Window
from src.modules.predictionsScene import boot as bootPredictions

# Main function
def main():

    # Initializes data
    settings = File("data/settings.datcs")
    window = Window(settings["screenX"], settings["screenY"], settings["displayX"], settings["displayY"], "PyScreen")
    scene = "predictions"
    running = True

    # Main program loop
    while running:

        # Loads predictions scene
        if scene == "predictions":
            running, scene = bootPredictions(window, settings)

    # CLoses pygame
    window.quit()

# Main function call
if __name__ == "__main__":
    main()
