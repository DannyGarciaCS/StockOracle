# Imports
from bs4 import BeautifulSoup
from src.classes.DataFile import DataFile
from src.classes.PriceFile import PriceFile
import pandas_market_calendars as mcal
import datetime as dt
from time import sleep
import yfinance as yf
import requests
import os









# Collects missing data
def collectData(settings):

    # Loads data avoiding update errors
    predictionsData = DataFile("data/predictions.datcs")
    while predictionsData.data == {}:
        predictionsData = DataFile("data/predictions.datcs")

    # Updates data if necessary
    meta = generateMeta(predictionsData)
    if not meta["validDate"]:

        baseTickers, trainingTickers, jointTickers = buildCollection(settings)

        # Updates collected tickers' data
        for num, ticker in enumerate(jointTickers[:10]):

            # Loads data avoiding update errors
            predictionsData = DataFile("data/predictions.datcs")
            while predictionsData.data == {}:
                predictionsData = DataFile("data/predictions.datcs")

            # Prints current progress
            predictionsData.set("loadingMessage",
            f"Fetching {ticker} ({num+1}/{len(jointTickers)} - {((num+1)/len(jointTickers))*100:.2f}%)")
            predictionsData.save()

            # Updates ticker if such exists and isn't corrupted
            create = False
            if os.path.exists(f"data/prices/{ticker}"):

                # Fetches ticker prices
                tickerPrices = [PriceFile(f"data/prices/{ticker}/{name}.price") for name in 
                [f"{ticker}_{time[0]}_{time[1]}" for time in [["1m", "7d"], ["5m", "60d"],
                ["15m", "60d"], ["1h", "730d"], ["1d", "max"], ["1wk", "max"]]]]

                # Creates files from scratch if corrupted
                for price in tickerPrices:
                    if price.isCorrupted():
                        create = True
                        break

                # Updates if there is uncorrupted data
                if not create: updateTicker(ticker, tickerPrices)
            else: create = True
            
            # Ticker does not exist or is corrupted
            if create: initializeTicker(ticker)
    
    return baseTickers, trainingTickers



# Updates an already existing ticker
def updateTicker(ticker, tickerPrices):

    
    today = dt.datetime.now().strftime("%Y-%m-%d:%M-%H")

                
# Builds ticker from scratch
def initializeTicker(ticker):

    # Fetches build data
    os.makedirs(f"data/prices/{ticker}")
    stock = yf.Ticker(ticker)

    # Loops over available time
    for time in [["1m", "7d"], ["5m", "60d"], ["15m", "60d"],
    ["1h", "730d"], ["1d", "max"], ["1wk", "max"]]:

        fileName = f"{ticker}_{time[0]}_{time[1]}.price"
        fileContent = ""

        try:

            # Fetches entries
            history = stock.history(interval=time[0], period=time[1])
            indices = history.index.tolist()
            values = history.get(["High", "Low", "Volume"]).values.tolist()

            # Ensures data was collected
            if not fileContent: raise ValueError("Could not find ticker data.")

            # Formats entries
            for entry in range(len(indices)):
                fileContent += f"{str(indices[entry])}::{str(values[entry])}\n"

        except Exception as error:

            print(f"Error loading data: {error}")
            fileContent = "NA"

        # Writes collected file content
        with open(f"data/prices/{ticker}/{fileName}", "w") as file:
            file.write(fileContent)

# Builds models used for predictions
def buildModels(settings, baseTickers, trainingTickers):
    pass

# Makes predictions using generated models
def makePredictions(settings):
    pass







# Generates meta data
def generateMeta(predictionsData):

    # Fetches last update date
    invalidDate = False
    lastUpdate = predictionsData.get("lastUpdate")
    try: lastUpdate = dt.datetime.strptime(lastUpdate, "%d/%m/%Y").date()
    except ValueError: invalidDate = True

    # Update date provided is valid
    if not invalidDate: invalidDate = isLastTradingDay(lastUpdate)
    return {
        "validDate": not invalidDate,
        "updateDate": predictionsData.get("lastUpdate"),
    }

# Determines if the given date is was the last trading day
def isLastTradingDay(date):

    nyse = mcal.get_calendar("NYSE")
    today = dt.date.today()
    dateRange = dt.timedelta(14)
    start = today - dateRange

    # Last trading day
    lastTD = nyse.valid_days(start_date=start.strftime("%Y-%m-%d"), end_date=today.strftime("%Y-%m-%d"))[-1]
    lastTD = lastTD.to_pydatetime().date()
    return not (date >= lastTD)

# Builds ticker collection
def buildCollection(settings):

    # Initializes composites
    baseTickers = []
    trainingTickers = []
    jointTickers = []

    # Defines collections
    baseCollections = settings.get("collections")
    trainingCollections = settings.get("trainingCollections")
    jointCollection = baseCollections
    for collection in trainingCollections:
        if collection not in jointCollection: jointCollection.append(collection)

    # Fetches collection tickers
    for collection in jointCollection:

        # Fetches tickers online and saves backup
        try:

            # Fetches tickers list
            tickers = fetchCollection(collection)
            with open(f"data/collections/{settings.get('collectionNames')[collection]}.datcs", "w") as file:
                file.write(f"tickers::{str(tickers)}")

            # Adds missing tickers to appropriate collections
            for collectionSet, tickerSet in zip([baseCollections, trainingCollections, jointCollection],
            [baseTickers, trainingTickers, jointTickers]):
                if collection in collectionSet:
                    for ticker in tickers:
                        if ticker not in tickerSet:
                            tickerSet.append(ticker)

        # Was not able to fetch tickers online, using local backup
        except Exception as error:

            # Warning
            print(f"Warning: Failed to load collection '{settings.get('collectionNames')[collection]}'. " + \
            "Using local backup.")
            print(f"Triggered by: {error}")

            # Fetches tickers list
            tickers = DataFile(f"data/collections/{settings.get('collectionNames')[collection]}.datcs").get("tickers")

            # Adds missing tickers to appropriate collections
            for collectionSet, tickerSet in zip([baseCollections, trainingCollections, jointCollection],
            [baseTickers, trainingTickers, jointTickers]):
                if collection in collectionSet:
                    for ticker in tickers:
                        if ticker not in tickerSet:
                            tickerSet.append(ticker)
    
    return baseTickers, trainingTickers, jointTickers

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
