from datetime import datetime, date, timedelta

import numpy as np
import pandas as pd
from fbprophet import Prophet
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
from tensorflow.keras.models import load_model

from api.data_loader import prepare_data, load_data_arima, load_df_bidirectlstm
from models.lstm.bidirect_lstm.bidirect_lstm import Bidirect_LSTM


class Predictor(object):
    def __init__(self) -> None:
        super().__init__()
        self.pred_dict = {
            "model": 0,
            "start_date": '2020-01-12',
            "end_date": '2021-01-30'
        }

        self.lstm_param = {
            'bitcoin': 'BTC-USD',
            'stock_market': '%5EGSPC',
            'usdx_index': 'DX-Y.NYB',
            'gold': 'GC=F',
            'start_date_lstm': '2017-01-01',

            'TRAIN': 0,
            'forward_days': 1
        }

    def get_prediction_prophet(self):
        """Predicts future price of bitcoin using prophet model.

        Returns:
            forecast: prophet forecast.

        @author: Andrii Koval
        """
        df = prepare_data(self.pred_dict["start_date"])
        df = df.rename(columns={"Date": "ds", "Close": "y"})

        model = Prophet()
        model.fit(df)

        today = datetime.today()
        end = datetime.strptime(self.pred_dict["end_date"], '%Y-%m-%d')
        diff = (end - today).days
        future = model.make_future_dataframe(periods=diff, freq='D')
        forecast = model.predict(future)

        forecast['y_actual'] = model.history['y']
        forecast = forecast.fillna(0)

        return forecast

    def get_prediction_arima(self):
        """Predicts future price of bitcoin using arima model.

         Returns:
             forecast: arima forecast.

         @author: Yulia Khlyaka
         """
        # training data
        date1 = pd.to_datetime(self.pred_dict['start_date'])
        date2 = pd.to_datetime(self.pred_dict['end_date'])

        # loading data
        df = load_data_arima(start_date=date1, end_date=date2)

        # Model
        mod = SARIMAX(df, order=(0, 1, 1), seasonal_order=(1, 1, 1, 12))
        res = mod.fit(disp=-1)

        # Getting the forecast of future values
        date_pr1 = date1 + timedelta(days=1)
        date_pr2 = date2 + timedelta(days=10)
        a_forecast = res.get_prediction(
            start=date_pr1, end=date_pr2)  # prediction for  +10 days

        pred_ci = a_forecast.conf_int()
        lower = np.array(pred_ci['lower Close'])
        upper = np.array(pred_ci['upper Close'])

        forecast = a_forecast.predicted_mean
        forecast = forecast.reset_index()

        forecast.columns = ['ds', 'yhat']

        forecast['yhat_lower'] = lower
        forecast['yhat_upper'] = upper

        # actual values
        history_df = df[date1: date2]
        history_df = np.array(history_df)
        a = np.zeros(shape=((len(forecast)-len(history_df)), 1))
        history_df = np.vstack((history_df, a))
        forecast['y_actual'] = history_df

        forecast = forecast.fillna(0)

        return forecast

    def get_prediction_bidirectlstm(self):
        """Predicts future price of bitcoin using bidirectional model

         Returns:
             forecast: bidirectional lstm forecast.

         @author: Pavlo Mospan
         """
        today = datetime.today().strftime('%Y-%m-%d')
        yesterday = date.today() - timedelta(days=1)
        yesterday = yesterday.strftime('%Y-%m-%d')

        df = load_df_bidirectlstm(
            name=[self.lstm_param['bitcoin']], start_date=self.lstm_param['start_date_lstm'])

        # number of rows in DF
        num_data_points = df.index.stop

        bidirect_lstm = Bidirect_LSTM()

        whole_data, whole_targets = bidirect_lstm.get_prepared_data(
            df=df, SEQ_LEN=20)
        pred_array = bidirect_lstm.get_prediction_array(whole_data)
        targ_array = bidirect_lstm.get_prediction_array(whole_targets)

        # Loading Model
        file_name = 'models/lstm/bidirect_lstm/BidirectLSTM_BTC-1f.h5'
        model = load_model(file_name)

        # Predicting
        y_hat = model.predict(pred_array)

        # Receiving forecast of datastamp, actual and predicted values
        forecast = bidirect_lstm.get_forecast(
            y_hat, targ_array, num_data_points, df)

        rmse = mean_squared_error(
            forecast['y_actual'][:-1], forecast['yhat'][:-1], squared=False)

        # Counting upper/loweer values
        upper = [forecast['yhat'][i] + rmse for i in range(len(y_hat))]
        lower = [forecast['yhat'][i] - rmse for i in range(len(y_hat))]
        forecast['yhat_lower'] = lower
        forecast['yhat_upper'] = upper

        return forecast
