import pandas as pd
import numpy as np
from datetime import datetime
import statsmodels.api as sm
import yfinance as yf


def load_currency(currency, start_date, end_date, path):
    """Load currency using yahoo finance api.

    Args:
        currency (str): currncy to download.
        start_date (str): start date.
        end_date (str): end date.
        path (str): where to save in .csv format.

    Returns:
        df: DataFrame

    @author: Andrii Koval
    """
    df = yf.download(currency,
                     start=start_date,
                     end=end_date,
                     progress=False)
    last_day = df.index[-1].strftime('%Y-%m-%d')
    if last_day == datetime.today().strftime('%Y-%m-%d'):
        pass
    else:
        df.to_csv(path)

    return df


def prepare_data(path='data/BTC-USD.csv', start_date='2017-01-01'):
    """Loads .csv file and prepares data for future use.

    Args:
        path (str): path to .csv file

    Returns:
        df: preprocessed DataFrame

    @author: Andrii Koval
    """
    df = pd.read_csv('data/BTC-USD.csv')
    df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d')
    df['Diff'] = np.diff(df['Close'], prepend=[0])
    df['Direction'] = np.where(df['Diff'] >= 0, 'green', 'red')
    df['Diff_abs'] = np.abs(df['Diff'])
    df = df[df['Date'] > start_date]

    return df


def prepare_dummy_data():
    """Prepares dummy data for model tabs

    Returns:
        ds: dummy data dict

    @author: Andrii Koval
    """
    data = prepare_data()

    ds = {
        "x": [x.to_pydatetime() for x in data['Date'].tolist()],
        "y": [x+2000 for x in data['Close'].tolist()],
        "yhat_lower": [x-5000 for x in data['Close'].tolist()],
        "yhat_upper": [x+5000 for x in data['Close'].tolist()],
        "y_actual": data['Close'].tolist()
    }

    return ds


def seasonal_decompose(df):
    """Seasonal decomposition using moving averages.

    Args:
        df (DataFrame): Pandas df for decomposition.

    Returns:
        seasonal: The seasonal component of the data series.
        resid: The residual component of the data series.
        trend: The trend component of the data series.

    @author: Andrii Koval
    """
    # Resampling to monthly frequency
    df.index = df.Date
    df_month = df.resample('M').mean()
    seasonal = sm.tsa.seasonal_decompose(df_month.Close).seasonal
    resid = sm.tsa.seasonal_decompose(df_month.Close).resid
    trend = sm.tsa.seasonal_decompose(df_month.Close).trend

    seasonal = seasonal.reset_index()
    resid = resid.reset_index()
    trend = trend.reset_index()

    seasonal = seasonal.rename(columns={"seasonal": "Close"})
    resid = resid.rename(columns={"resid": "Close"})
    trend = trend.rename(columns={"trend": "Close"})

    return seasonal, resid, trend


def load_data_arima(start_date='2018-01-01', end_date='2020-02-01'):
    """Loads .csv file and prepares data for future use.

    Args:
        path (str): path to .csv file

    Returns:
        df: preprocessed DataFrame

    @author: Yulia Khlyaka
    """
    # loading data
    try:
        df = pd.read_csv('data/BTC-USD.csv')

    except FileNotFoundError:
        print('FileNotFoundError')
    df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d')
    # # Producing and visualizing forecasts
    cols = ['Open', 'Low', 'High', 'Volume', 'Adj Close']
    df.drop(cols, axis=1, inplace=True)

    # Resampling to daily frequency
    df.index = df.Date
    df = df[(df['Date'] > start_date) & (df['Date'] < end_date)]
    df = df.resample('D').mean()

    return df


def load_df_bidirectlstm(name, start_date):
    """Loads DataFrames of given values.
    E.x.: Bitcoin, using yahoo finance api.
    Takes out one Closed value and fills possible
    empty values with the nearest value available in the time series

    :param name: value to be downloaded
    :param start_date: start date

    :return: DataFrame of loaded currency

    @author: Pavlo Mospan
    """

    df = yf.download(name, start=start_date)
    df = df.reset_index()

    return df


def data_update():
    """Loads data from yahoo!finance and save as *.csv file

    Args:
        :param start_date: 2017-01-01
        :param end_date: today

    @author: Yulia Khlyaka
    """
    end_date = datetime.today()
    data_df = yf.download('BTC-USD',
                          start='2017-01-01',
                          end=end_date,
                          group_by="ticker")
    filename = 'data/BTC-USD.csv'
    data_df.to_csv(filename)
