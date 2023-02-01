# Imports
from bs4 import BeautifulSoup
from src.classes.DataFile import DataFile
import pandas_market_calendars as mcal
import datetime as dt
from time import sleep
import yfinance as yf
import requests
import os

# Generates meta data
def generateMeta(predictionsData):

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

    return {
        "validDate": not invalidDate,
        "updateDate": predictionsData.get("lastUpdate"),
    }

# Collects missing data
def collectData(settings):

    # Loads data avoiding update errors
    predictionsData = DataFile("data/predictions.datcs")
    while predictionsData.data == {}:
        predictionsData = DataFile("data/predictions.datcs")

    # Determines if an update is even necessary
    meta = generateMeta(predictionsData)
    if not meta["validDate"]:

        composite = []

        # Tries fetching list from website
        try:

            for collection in settings.get("collections"):

                # Saves updated tickers list locally as backup
                tickers = fetchCollection(collection)
                with open(f"data/collections/{settings.get('collectionNames')[collection]}.datcs", "w") as file:
                    file.write(f"tickers::{str(tickers)}")

                # Adds ticker to composite if not 
                for ticker in tickers:
                    if ticker not in composite:
                        composite.append(ticker)

        except Exception as error:

            # Warning
            print("Warning: Failed to load ticker list. Using local backup.")
            print(f"Triggered by: {error}")

            # Loads tickers locally
            for collection in settings.get("collections"):

                for ticker in DataFile(
                f"data/collections/{settings.get('collectionNames')[collection]}.datcs").get("tickers"):
                    if ticker not in composite:
                        composite.append(ticker)
        
        # Updates collected tickers' data
        for num, ticker in enumerate(composite[:10]):

            # Loads data avoiding update errors
            predictionsData = DataFile("data/predictions.datcs")
            while predictionsData.data == {}:
                predictionsData = DataFile("data/predictions.datcs")

            # Prints current progress
            predictionsData.set("loadingMessage",
            f"Fetching {ticker} ({num+1}/{len(composite)} - {((num+1)/len(composite))*100:.2f}%)")
            predictionsData.save()

            if os.path.exists(f"data/prices/{ticker}"):
                pass
            else:

                os.makedirs(f"data/prices/{ticker}")
                today = dt.datetime.today().strftime("%Y-%m-%d:%M-%H")
                stock = yf.Ticker(ticker)

                for time in [["1m", "7d"], ["5m", "60d"], ["15m", "60d"],
                ["1h", "730d"], ["1d", "max"], ["1wk", "max"]]:

                    fileName = f"{ticker}_{time[0]}_{time[1]}.price"
                    fileContent = today + "\n"

                    history = stock.history(interval=time[0], period=time[1])
                    
                    # Writes collected file content
                    with open(f"data/prices/{ticker}/{fileName}", "w") as file:
                        file.write(fileContent)

# Builds models used for predictions
def buildModels(settings):
    pass

# Makes predictions using generated models
def makePredictions(settings):
    pass

# Fetches one of the available collections
def fetchCollection(id):

    tickers = []

    # Fetches wikipedia page with ticker list
    collections = [
        ("https://en.wikipedia.org/wiki/List_of_S&P_400_companies", 0, 0),
        ("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", 0, 0),
        ("https://en.wikipedia.org/wiki/List_of_S%26P_600_companies", 0, 1),

        ("https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average", 1, 1),
        ("https://en.wikipedia.org/wiki/Dow_Jones_Transportation_Average", 0, 0),
        ("https://en.wikipedia.org/wiki/Dow_Jones_Utility_Average", 1, 0),

        ("https://en.wikipedia.org/wiki/Nasdaq-100", 4, 1),
        ("https://en.wikipedia.org/wiki/Russell_1000_Index", 2, 1)
    ]

    page = requests.get(collections[id][0])
    soup = BeautifulSoup(page.content, "html.parser")

    # Loops over table rows
    table = soup.find_all("table")[collections[id][1]]
    rows = table.find_all("tr")
    for row in rows:

        # Finds and validate ticker names
        tickerRow = row.find_all("td")
        if len(tickerRow) < 2: continue
        tickerRow = tickerRow[collections[id][2]]
        if tickerRow is None: continue
        ticker = tickerRow.text.strip()
        if not ticker.isalpha(): continue
        tickers.append(ticker)

    return tickers
