import pandas as pd
import yfinance as yf
import datetime as dt


def yfinance_data(ticker, interval='1d', years_data=7):

    """
    Download data
    ticker = Ticker to download
    inverval = 1d, 1m, 1a, etc.
    years_data = number of years to get

    DATES EXAMPLE = '2022-10-06'
    """

    try:

        start = dt.datetime.today() - dt.timedelta(365*years_data)
        start = start.strftime('%Y-%m-%d')

        end = dt.datetime.today() + dt.timedelta(1)
        end = end.strftime('%Y-%m-%d')

        data = yf.download(tickers=ticker, interval=interval, auto_adjust=True, start=start, end=end)


        data.index = pd.to_datetime(data.index)
        data = data.tz_localize(None)

    except:
        data = pd.DataFrame()

    return data
