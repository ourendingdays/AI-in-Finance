from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
import matplotlib

from datetime import datetime

from api.plots import Plots
from api.data_loader import load_currency
from models.predictor import Predictor

matplotlib.use('Agg')

app = Flask(__name__)
Bootstrap(app)

CURRS = ['BTC-USD']

plots = Plots()
predictor = Predictor()


@app.route('/')
def index():
    """Index endpoint

    @author: Andrii Koval
    """

    start = '2015-08-07'
    end = datetime.today().strftime('%Y-%m-%d')

    for curr in CURRS:
        load_currency(currency=curr,
                      start_date=start,
                      end_date=end,
                      path=f'data/{curr}.csv')

    return render_template('index.html')


@app.route('/prophet', methods=['POST', 'GET'])
def prophet():
    """Prophet output endpoint.
    Sends data to bokeh js handler.

    @author: Andrii Koval
    """
    if request.method == 'POST':
        return jsonify(message='Post message')
    elif request.method == 'GET':
        data = plots.prophet_df

        data['ds'] = data['ds'].astype(str)
        data = {'ds': data['ds'].tolist(),
                'yhat': data['yhat'].tolist(),
                'yhat_lower': data['yhat_lower'].tolist(),
                'yhat_upper': data['yhat_upper'].tolist(),
                'y_actual': data['y_actual'].tolist()
                }

        return jsonify(isError=False,
                       message="Success",
                       statusCode=200,
                       data=data), 200


@app.route('/arima', methods=['POST', 'GET'])
def arima():
    """Arima output endpoint.
    Sends data to bokeh js handler.

    @author: Yulia Khlyaka
    """
    if request.method == 'POST':
        return jsonify(message='Post message')
    elif request.method == 'GET':
        data = plots.arima_df

        data['ds'] = data['ds'].astype(str)
        data = {'ds': data['ds'].tolist(),
                'yhat': data['yhat'].tolist(),
                'y_actual': data['y_actual'].tolist(),
                'yhat_lower': data['yhat_lower'].tolist(),
                'yhat_upper': data['yhat_upper'].tolist()
                }

        return jsonify(isError=False,
                       message="Success",
                       statusCode=200,
                       data=data), 200


@app.route('/lstm', methods=['POST', 'GET'])
def lstm():
    """LSTM output endpoint.
    Sends data to bokeh js handler.

    @author: Pavlo Mospan
    """
    if request.method == 'POST':
        return jsonify(message='Post message')
    elif request.method == 'GET':
        data = plots.lstm_df
        data['ds'] = data['ds'].astype(str)
        data = {'ds': data['ds'].tolist(),
                'yhat': data['yhat'].tolist(),
                'y_actual': data['y_actual'].tolist(),
                'yhat_lower': data['yhat_lower'].tolist(),
                'yhat_upper': data['yhat_upper'].tolist()
                }

        return jsonify(isError=False,
                       message="Success",
                       statusCode=200,
                       data=data), 200


@app.route('/predict_model', methods=['GET', 'POST'])
def predict_model():
    """Predict endpoint.
    Sets model name to predict.

    @author: Andrii Koval
    """
    data = request.json

    if data:
        predictor.pred_dict["model"] = data["model"]
    else:
        pass

    return 'Non tam praeclarum est scire latine, quam turpe nescire'


@app.route('/predict_date', methods=['GET', 'POST'])
def predict_start():
    """Predict date endpoint.
    Sets start date of training data.

    @author: Andrii Koval
    """
    data = request.json

    if data:
        predictor.pred_dict["start_date"] = data["start_date"]
    else:
        pass

    return 'Non tam praeclarum est scire latine, quam turpe nescire'


@app.route('/predict_date_end', methods=['GET', 'POST'])
def predict_end():
    """Predict date end endpoint.
    Sets end date for prediction.

    @author: Andrii Koval
    """
    data = request.json

    if data:
        predictor.pred_dict["end_date"] = data["end_date"]
    else:
        pass

    return 'Non tam praeclarum est scire latine, quam turpe nescire'


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Predict endpoint.
    Chooses model for prediction and predcits
    bitcoin price for the given time period.

    @author: Andrii Koval, Yulia Khlyaka, Pavlo Mospan
    """
    data = request.json

    if data:
        predict = bool(data["predict"])

        if predict:
            if predictor.pred_dict["model"] == 0:
                # ARIMA
                arima_forecast = predictor.get_prediction_arima()
                plots.arima_df = arima_forecast
            elif predictor.pred_dict["model"] == 1:
                # Prophet
                prophet_forecast = predictor.get_prediction_prophet()
                plots.prophet_df = prophet_forecast
            elif predictor.pred_dict["model"] == 2:
                # LSTM
                lstm_forecast = predictor.get_prediction_bidirectlstm()
                plots.lstm_df = lstm_forecast
    else:
        pass

    return 'Non tam praeclarum est scire latine, quam turpe nescire'


@app.route('/dashboard/')
def show_dashboard():
    """Dashboard endpoint.
    Draws bokeh plots.

    @author: Andrii Koval
    """
    script, div = plots.make_plot()
    script_tab, div_tab = plots.make_tabs()
    script_trend, div_trend = plots.make_trend()

    return render_template('layout.html',
                           script=script,
                           div=div,
                           script_trend=script_trend,
                           div_trend=div_trend,
                           script_tab=script_tab,
                           div_tab=div_tab)
