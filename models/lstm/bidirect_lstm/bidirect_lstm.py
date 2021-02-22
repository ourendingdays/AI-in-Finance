import numpy as np
import pandas as pd

from datetime import datetime, date, timedelta
from sklearn.preprocessing import MinMaxScaler


class Bidirect_LSTM:
    def __init__(self) -> None:
        super().__init__()
        self.scl = MinMaxScaler()
        self.SEQ_LEN = None
        self.whole_data = None
        self.whole_targets = None

    def get_prepared_data(self, df, SEQ_LEN):
        """
        Returns scaled array of values

        :param df: DataFrame with values to be scaled
        :return: array of prepared values

        @author: Pavlo Mospan
        """

        close_price = df.Close.values.reshape(-1, 1)
        scaled_close = self.scl.fit_transform(close_price)

        # length of the sequence that predicts the next day's value
        self.SEQ_LEN = SEQ_LEN

        # initializing numpday.ndarrays of the whole target and feature arrays
        self.whole_data = np.empty([1, 20, 1])
        self.whole_targets = np.empty([1, 1])

        X_train, y_train, X_test, y_test = self.preprocess(scaled_close, self.SEQ_LEN, train_split=0.95)

        return self.whole_data, self.whole_targets

    def to_sequences(self, data, seq_len):
        """
        Spliting data into sequences of the preset length
        and obtaining shape: [batch_size, sequence_length, n_features]

        :param data: array of values
        :param seq_len: sequence length

        :return: array of sequenced values

        @author: Pavlo Mospan
        """
        d = []

        for index in range(len(data) - seq_len + 1):
            d.append(data[index: index + seq_len])

        return np.array(d)

    def preprocess(self, data_raw, seq_len, train_split):
        """
        Building sequences by creating a sequence of a specified length at position 0.
        Then shifting one position to the right (e.g. 1) and creating another sequence.

        :param data_raw: array of values
        :param seq_len: sequence length
        :param train_split: percentage of train/test split

        :return: arrays of trained and test values

        @author: Pavlo Mospan
        """

        self.whole_data = self.to_sequences(data_raw, seq_len)
        self.whole_targets = self.whole_data[:, -1, :]

        num_train = int(train_split * self.whole_data.shape[0])

        X_train = self.whole_data[:num_train, :, :]
        y_train = self.whole_data[:num_train, -1, :]

        X_test = self.whole_data[num_train:, :, :]
        y_test = self.whole_data[num_train:, -1, :]

        return X_train, y_train, X_test, y_test

    def get_prediction_array(self, X):
        """
        Inserts an other array to the end of the whole_data sequence in order to make
        array for predicting tomorrow's value

        :param X: array of target or feature values

        :return: array of shape (None, 20, 1)

        @author: Pavlo Mospan
        """
        next = len(X)
        a = np.insert(X, [next], X[next - 1], axis=0)
        for i_ in range(len(a[100]) - 1):
            if (i_ == 20):
                a[next][i_][0] == a[next][i_-1][0]
            else:
                a[next][i_][0] = a[next][i_ + 1][0]

        return a

    def get_forecast(self, y_hat, targ_array, num_data_points, df):
        """
        Rescales values back with MinMaxScaler and appends date and arrays of actual and predicted values to one DataFrame

        :param y_hat: predicted values
        :param targ_array: array of target true values
        :param num_data_points: number of days(data points in the whole DataFrame)
        :param df: DataFrame of Bitcoin prices

        :return: forecast DataFrame with date, actual and predicted values

        @author: Pavlo Mospan
        """
        y_true_inverse = self.scl.inverse_transform(targ_array)
        y_hat_inverse = self.scl.inverse_transform(y_hat)

        # where the sequence prediction started from
        started_ = num_data_points - len(y_true_inverse) + 1

        tomorrow = date.today() + timedelta(days=1)
        tomorrow = tomorrow.strftime('%Y-%m-%d')

        ds = []

        for i_ in df.Date[started_:]:
            ds.append(i_.strftime('%Y-%m-%d'))

        ds.append(tomorrow)

        y_true = y_true_inverse.reshape(len(y_true_inverse), )
        y_true[-1] = 0
        y_pred = y_hat_inverse.reshape(len(y_hat_inverse), )

        d = {"ds": ds, "y_actual": y_true, 'yhat': y_pred}
        forecast = pd.DataFrame(d)
        return forecast