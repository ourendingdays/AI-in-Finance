from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.widgets import DatePicker
from bokeh.models.tools import HoverTool

from datetime import date
import pandas as pd
import numpy as np

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    """[summary]

    Returns:
        [type]: [description]

    @author: Andrii Koval
    """
    return render_template('index.html')


@app.route('/dashboard/')
def show_dashboard():
    """[summary]

    Returns:
        [type]: [description]

    @author: Andrii Koval
    """
    plot = make_plot()
    d_picker = date_picker()
    return render_template('layout.html',
                           script=plot[0],
                           div=plot[1],
                           script1=d_picker[0],
                           div1=d_picker[1])


def date_picker():
    """[summary]

    Returns:
        [type]: [description]

    @author: Andrii Koval
    """
    dt_pckr_strt = DatePicker(title='Select start of sync date',
                              min_date=date(2017, 1, 1),
                              max_date=date.today())

    script, div = components(dt_pckr_strt)
    return script, div


def prepare_data(path='data/BTC-USD.csv'):
    """[summary]

    Args:
        path ([type]): [description]

    Returns:
        [type]: [description]

    @author: Andrii Koval
    """
    df = pd.read_csv('data/BTC-USD.csv')
    df['Date'] = pd.to_datetime(df.Date, format='%Y-%m-%d')
    df['Diff'] = np.diff(df['Close'], prepend=[0])
    df['Diff'][0] = 0
    df['Direction'] = np.where(df['Diff'] >= 0, 'green', 'red')
    df['Diff_abs'] = np.abs(df['Diff'])
    print(df['Direction'][0:10])
    df = df[df['Date'] > '2020-01-01']
    return df


def make_plot():
    """[summary]

    Returns:
        [type]: [description]

    @author: Andrii Koval
    """
    df = prepare_data()
    plot = figure(sizing_mode='stretch_both',
                  x_axis_type="datetime",
                  title="Some Title")
    plot.border_fill_color = "whitesmoke"
    plot.min_border_left = 80
    plot.toolbar.autohide = True
    plot.xaxis.axis_label = "Date"
    plot.yaxis.axis_label = "Price, USD"
    plot.line(x='Date', y='Close', source=df, line_width=4, line_color="blue")
    plot.vbar(x='Date', top='Diff_abs',
              color='Direction', source=df, width=5.0)

    plot.add_tools(HoverTool(
        show_arrow=True,
        tooltips=[
            ('date',   '@Date{%F}'),
            ('close',  '$@Close{%0.2f}'),
            ('difference', '@Diff{%0.2f}')
        ],
        formatters={
            '@Date': 'datetime',
            '@Close': 'printf',
            '@Diff': 'printf'
        },
        mode='vline'
    ))

    script, div = components(plot)
    return script, div
