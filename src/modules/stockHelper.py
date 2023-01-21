# Imports
from src.classes.Button import Button
import pandas_market_calendars as mcal
import datetime as dt

# Generates meta data
def generateMeta(predictionsData):

    meta = {}

    # Fetches last update date
    invalidDate = False
    lastUpdate = predictionsData.get("lastUpdate")
    try: lastUpdate = dt.datetime.strptime(lastUpdate, "%d/%m/%Y").date()
    except ValueError: invalidDate = True

    # Update date provided is valid
    if not invalidDate:

        nyse = mcal.get_calendar("NYSE")
        today = dt.date.today()
    
    
    meta["validUpdate"] = not invalidDate
    meta["updateDate"] = predictionsData.get("lastUpdate")
    
    

    return meta

def updateData():
    pass
