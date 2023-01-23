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
        dateRange = dt.timedelta(14)
        start = today - dateRange

        # Last trading day
        lastTD = nyse.valid_days(start_date=start.strftime("%Y-%m-%d"), end_date=today.strftime("%Y-%m-%d"))[-1]
        lastTD = lastTD.to_pydatetime().date()
        invalidDate = not (lastUpdate >= lastTD)

    meta["validUpdate"] = not invalidDate
    meta["updateDate"] = predictionsData.get("lastUpdate")

    return meta

def updateData():
    pass
