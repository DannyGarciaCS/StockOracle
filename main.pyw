# Imports
from src.classes.DataFile import DataFile
from src.classes.Window import Window
from src.modules.computingScene import boot as bootComputing
from src.modules.predictionsScene import boot as bootPredictions
from src.modules.settingsScene import boot as bootSettings
from src.modules.soInit import soInit

# Main function
def main():

    # Initializes data
    settings = DataFile("data/settings.datcs")
    if settings.get("initialBoot"): soInit(settings)
    window = Window(settings, "Market Oracle")
    scene = "predictions"
    running = True

    # Main program loop
    while running:

        # Loads predictions scene
        if scene == "predictions":
            running, scene = bootPredictions(window, settings)
        
        # Loads settings scene
        elif scene == "settings":
            running, scene = bootSettings(window, settings)
        
        # Loads computing scene
        elif scene == "computing":
            running, scene = bootComputing(window, settings)

    # Closes pygame
    window.quit()

# Main function call
if __name__ == "__main__":
    main()
