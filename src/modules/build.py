# Imports
import contextlib
from bs4 import BeautifulSoup
from src.classes.DataFile import DataFile
import pandas_market_calendars as mcal
import datetime as dt
import multiprocessing
import yfinance as yf
import requests
import threading
import pickle
import os
from time import sleep
import glob

# Collects missing data
def collectData(settings):

    # Loads data avoiding update errors
    predictionsData = DataFile("data/predictions.datcs")
    while predictionsData.data == {}:
        predictionsData = DataFile("data/predictions.datcs")

    # Splits work amongst different usable processors
    baseTickers, trainingTickers, jointTickers = buildCollection(settings)

    # Updates data if necessary
    if not isLastTradingDay(predictionsData.get("dataUpdate")):
        resetData(jointTickers, settings)

    # Saves date of update
    today = dt.date.today().strftime("%d-%m-%Y")
    predictionsData.set("dataUpdate", today)
    predictionsData.save()

    return baseTickers, trainingTickers

# Resets stored ticker data with new one
def resetData(jointTickers, settings):

    # Deletes all stored price data
    files = glob.glob("data/prices/*")
    for file in files:
        os.remove(file)

    count = len(jointTickers)
    usableCPU = multiprocessing.cpu_count() - 1
    if settings.get("safeMode"): usableCPU -= 1

    if usableCPU > 1 and count > usableCPU:

        # Generates multiprocessing ticker batches
        overflow = False
        batchSize = len(jointTickers) / usableCPU
        if type(batchSize) != int:
            batchSize = int(batchSize)
            overflow = True
        tickerBatches = [jointTickers[tick:tick + batchSize] for tick in range(0, len(jointTickers), batchSize)]

        # Equals stack of tickers to processors
        if overflow:
            extra = tickerBatches.pop(-1)
            tickerBatches[-1] += extra

    else: tickerBatches = [jointTickers]

    # Starts main threads
    threads = [threading.Thread(target=updateProgress, args=(count, )),
    threading.Thread(target=handleStack, args=(settings, tickerBatches[0], ))]
    for thread in threads: thread.start()

    # Starts processes
    processes = []
    for processID in range(len(tickerBatches) - 1):

        process = multiprocessing.Process(target=handleStack, args=(settings, tickerBatches[processID + 1],))
        processes.append(process)
        process.start()

    # Waits for updates to finish
    for thread in threads: thread.join()
    for process in processes: process.join()

# Updates progress status 
def updateProgress(count):

    # Continues searching until we have all tickers
    found = len(next(os.walk("data/prices"))[1])
    while found < count:
        found = len(next(os.walk("data/prices"))[1])

        # Loads data avoiding update errors
        predictionsData = DataFile("data/predictions.datcs")
        while predictionsData.data == {}:
            predictionsData = DataFile("data/predictions.datcs")

        # Prints current progress
        predictionsData.set("loadingMessage",
        f"Fetched {found}/{count} tickers ({(found/count) * 100:.2f}%)")
        predictionsData.save()
        sleep(0.2)

# Initializes a stack of tickers
def handleStack(settings, stack):

    ### Implemented multithreading solution here, but rate of download was too fast and locked database
    ### Will only do multiprocessing, no multithreading for data fetching
    for ticker in stack:
            initializeTicker(ticker)

# Builds ticker from scratch
def initializeTicker(ticker):

    # Fetches build data
    directory = f"data/prices/{ticker}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    stock = yf.Ticker(ticker)

    fileName = f"{directory}/{ticker}.price"
    fileContent = []

    # Fetches data
    with contextlib.suppress(Exception):
        
        history = stock.history(interval="1d", period="max")
        indices = history.index.tolist()
        for index in range(len(indices)): indices[index] = indices[index].strftime("%d-%m-%Y:%M-%H")
        values = history.get(["High", "Low", "Volume"]).values.tolist()

        # Saves data
        fileContent.extend((indices[entry], values[entry]) for entry in range(len(indices)))

    with open(fileName, 'wb') as file:
        pickle.dump(fileContent, file)

# Builds models used for predictions
def buildModels(settings, baseTickers, trainingTickers):
    
    # Loads data avoiding update errors
    predictionsData = DataFile("data/predictions.datcs")
    while predictionsData.data == {}:
        predictionsData = DataFile("data/predictions.datcs")
    
    print("building data")



    #while True:


    #    for ticker in trainingTickers



# Makes predictions using generated models
def makePredictions(settings):
    pass

# Determines if the given date is was the last trading day
def isLastTradingDay(date):

    # Handles string inputs
    if type(date)==str:
        date = "".join(date.split("/"))
        date = "".join(date.split("-"))
        date = dt.datetime.strptime(date, "%d%m%Y").date()

    nyse = mcal.get_calendar("NYSE")
    today = dt.date.today()
    dateRange = dt.timedelta(14)
    start = today - dateRange

    # Last trading day
    lastTD = nyse.valid_days(start_date=start.strftime("%Y-%m-%d"), end_date=today.strftime("%Y-%m-%d"))[-1]
    lastTD = lastTD.to_pydatetime().date()
    return date >= lastTD

# Builds ticker collection
def buildCollection(settings):

    # Initializes composites
    jointTickers = []
    baseTickers = []
    trainingTickers = []
    tickerSets = [baseTickers, trainingTickers, jointTickers]

    # Defines collections
    baseCollections = settings.get("collections")
    trainingCollections = settings.get("trainingCollections")
    jointCollection = baseCollections
    for collection in trainingCollections:
        if collection not in jointCollection: jointCollection.append(collection)
    collectionSets = [baseCollections, trainingCollections, jointCollection]

    # Fetches collection tickers
    for collection in jointCollection:

        # Fetches tickers online and saves backup
        try:

            # Fetches tickers list
            tickers = fetchCollection(collection)
            with open(f"data/collections/{settings.get('collectionNames')[collection]}.datcs", "w") as file:
                file.write(f"tickers::{str(tickers)}")
            tickerSort(tickers, collection, collectionSets, tickerSets)

        except Exception as error:

            # Warning
            print(f"Warning: Failed to load collection '{settings.get('collectionNames')[collection]}'. " + \
            "Using local backup.")
            print(f"Triggered by: {error}")

            # Fetches tickers list
            tickers = DataFile(f"data/collections/{settings.get('collectionNames')[collection]}.datcs").get("tickers")
            tickerSort(tickers, collection, collectionSets, tickerSets)

    return baseTickers, trainingTickers, jointTickers

# Adds missing tickers to appropriate collections
def tickerSort(tickers, collection, collectionSets, tickerSets):
    for collectionSet, tickerSet in zip(collectionSets, tickerSets):
        if collection in collectionSet:
            for ticker in tickers:
                if ticker not in tickerSet:
                    tickerSet.append(ticker)

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
