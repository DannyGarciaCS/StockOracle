# Imports
import pandas_market_calendars as mcal
from src.classes.DataFile import DataFile
import datetime as dt
import sys
import os

# Disable print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore print
def enablePrint():
    sys.stdout = sys.__stdout__

# Loads data avoiding update errors
def safeLoad(path):
    file = DataFile(path)
    while file.data == {}:
        file = DataFile(path)
    return file

# Fetches a range of trading days
def tradingRange(dayRange):

    # Initializes search start and end
    today = dt.date.today()
    start = today - dt.timedelta(dayRange)

    # Fetches initial state of calendar
    nyse = mcal.get_calendar("NYSE")
    history = nyse.valid_days(start_date=start, end_date=today)

    # Keeps adding days until range is satisfied
    while(len(history) < dayRange):
        start -= dt.timedelta(1)
        history = nyse.valid_days(start_date=start, end_date=today)

    # Returns formatted range
    timeRange = [history[day].to_pydatetime() for day in range(len(history))]
    for time in timeRange: time.replace(hour=23); time.replace(minute=59)
    return timeRange

# Determines if given date is a training day
def isTradingDay(date):

    # Handles string inputs
    if type(date)==str:
        date = "".join(date.split("/"))
        date = "".join(date.split("-"))
        date = dt.datetime.strptime(date, "%d%m%Y").date()
    
    # Returns market status
    if date.weekday() > 4: return False
    elif date.hour < 9 or date.hour > 16: return False
    else: return True

# Determines if the given date is was the last trading day
def isLastTradingDay(date):

    # Handles string inputs
    if type(date)==str:
        date = "".join(date.split("/"))
        date = "".join(date.split("-"))
        date = dt.datetime.strptime(date, "%d%m%Y").date()

    nyse = mcal.get_calendar("NYSE")
    today = dt.date.today()
    start = today - dt.timedelta(14)

    # Last trading day
    lastTD = nyse.valid_days(start_date=start.strftime("%Y-%m-%d"), end_date=today.strftime("%Y-%m-%d"))[-1]
    lastTD = lastTD.to_pydatetime().date()
    return date >= lastTD

# Returns the next trading day
def nextTradingDay(date):
    
    # Initializes search start and end
    end = date + dt.timedelta(1)

    # Fetches initial state of calendar
    nyse = mcal.get_calendar("NYSE")
    history = nyse.valid_days(start_date=date, end_date=end)

    # Keeps adding days until range is satisfied
    while(len(history) != 2):
        end += dt.timedelta(1)
        history = nyse.valid_days(start_date=date, end_date=end)
    
    return history[-1].to_pydatetime().date()

def naiveDateTimeComparison(dateA, comparator,  dateB):

    if comparator == "<=":
        out = False

        # Compares year
        if dateA.year < dateB.year: out = True
        elif dateA.year == dateB.year:

            # Compares month
            if dateA.month < dateB.month: out = True
            if dateA.month == dateB.month:

                # Compares day
                if dateA.day < dateB.day: out = True
                if dateA.day == dateB.day:

                    # Compares hour
                    if dateA.hour < dateB.hour: out = True
                    if dateA.hour == dateB.hour:

                        # Compares minute
                        if dateA.minute < dateB.minute: out = True
                        if dateA.minute == dateB.minute: out = True
    
        return out
    