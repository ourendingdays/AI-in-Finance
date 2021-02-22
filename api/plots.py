from bokeh import events
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.events import ButtonClick
from bokeh.models import CustomJS, Button, ColumnDataSource
from bokeh.models.widgets import DatePicker, Panel, Tabs
from bokeh.models.tools import HoverTool
from bokeh.layouts import row, column

from datetime import date, datetime, timedelta

from api.data_loader import prepare_data, seasonal_decompose, data_update, prepare_dummy_data
import api.js_callbacks as js
import api.config as cfg


class Plots(object):
    def __init__(self) -> None:
        super().__init__()
        self.prophet_df = None
        self.arima_df = None
        self.lstm_df = None
        self.trader_df = None
        self.plot = None

    def arima_tab(self):
        """Creates arima predictor tab.

        Returns:
            tab: bokeh tab component.

        @author: Yulia Khlyaka
        """
        ds = prepare_dummy_data()

        # create a new plot with a title and axis labels
        plot = figure(plot_width=800,
                      plot_height=500,
                      sizing_mode='fixed',
                      x_axis_type="datetime",
                      title="ARIMA forecaster",
                      **cfg.PLOT_OPTS)
        plot.toolbar.autohide = True
        plot.xaxis.axis_label = "Date"
        plot.yaxis.axis_label = "Price, USD"

        source = ColumnDataSource(data=ds)
        plot1 = plot.line('x', 'y',
                          source=source,
                          line_width=3,
                          legend_label="Prediction",
                          line_color='aqua')

        plot.circle('x', 'y_actual',
                    size=3,
                    color=cfg.PURPLE,
                    alpha=0.8,
                    legend_label="Actual value",
                    source=source)

        plot.varea('x', 'yhat_lower', 'yhat_upper',
                   fill_alpha=0.2,
                   legend_label="Confidence interval",
                   fill_color=cfg.LIGHT_PURPLE,
                   source=source)

        plot.add_tools(HoverTool(
            show_arrow=True,
            renderers=[plot1],
            tooltips=[
                ('x', '@x{%F}'),
                ('y', '$@y{%0.2f}'),
                ('y_actual', '$@y_actual{%0.2f}'),
                ('yhat_lower', '$@yhat_lower{%0.2f}'),
                ('yhat_upper', '$@yhat_upper{%0.2f}'),
            ],
            formatters={
                '@x': 'datetime',
                '@y': 'printf',
                '@y_actual': 'printf',
                '@yhat_lower': 'printf',
                '@yhat_upper': 'printf',
            },
            mode='vline'
        ))

        self.plot = plot

        button_reset = Button(label="Reset",
                              button_type="success")

        button_reset_callback = CustomJS(args=dict(source=source,
                                                   plot=plot),
                                         code=js.BUTTON_RESET_ARIMA)

        button_reset.js_on_click(button_reset_callback)

        layout = column(plot, button_reset)
        tab = Panel(child=layout, title='Arima predictor')

        return tab

    def prophet_tab(self):
        """Creates prophet predictor tab.

        Returns:
            tab: bokeh tab component.

        @author: Andrii Koval
        """
        ds = prepare_dummy_data()

        plot = figure(plot_width=800,
                      plot_height=500,
                      sizing_mode='fixed',
                      x_axis_type="datetime",
                      title="Prophet predictor",
                      **cfg.PLOT_OPTS)

        plot.toolbar.autohide = True
        plot.xaxis.axis_label = "Date"
        plot.yaxis.axis_label = "Price, USD"

        source = ColumnDataSource(data=ds)

        plot1 = plot.line('x', 'y',
                          source=source,
                          line_width=3,
                          legend_label="Prediction",
                          line_color=cfg.GREEN)
        plot.varea('x', 'yhat_lower', 'yhat_upper',
                   fill_alpha=0.2,
                   legend_label="Confidence interval",
                   fill_color=cfg.DARK_PURPLE,
                   source=source)

        plot.circle('x', 'y_actual',
                    size=3,
                    color=cfg.DARK_GREEN,
                    alpha=0.8,
                    legend_label="Actual value",
                    source=source)

        plot.add_tools(HoverTool(
            show_arrow=True,
            renderers=[plot1],
            tooltips=[
                ('x',   '@x{%F}'),
                ('y',  '$@y{%0.2f}'),
                ('yhat_lower',  '$@yhat_lower{%0.2f}'),
                ('yhat_upper',  '$@yhat_upper{%0.2f}'),
                ('y_actual',  '$@y_actual{%0.2f}'),
            ],
            formatters={
                '@x': 'datetime',
                '@y': 'printf',
                '@yhat_lower': 'printf',
                '@yhat_upper': 'printf',
                '@y_actual': 'printf',
            },
            mode='vline'
        ))

        self.plot = plot

        button_reset = Button(label="Reset",
                              button_type="success")

        button_reset_callback = CustomJS(args=dict(source=source,
                                                   plot=plot),
                                         code=js.BUTTON_RESET)

        button_reset.js_on_click(button_reset_callback)

        layout = column(plot, button_reset)
        tab = Panel(child=layout, title='Prophet predictor')

        return tab

    def lstm_tab(self):
        """Creates lstm predictor tab.

        Returns:
            tab: bokeh tab component.

        @author: Pavlo Mospan
        """
        ds = prepare_dummy_data()

        source = ColumnDataSource(data=ds)

        plot = figure(plot_width=800,
                      plot_height=500,
                      sizing_mode='fixed',
                      x_axis_type="datetime",
                      title="LSTM predictor",
                      **cfg.PLOT_OPTS)

        plot.circle('x', 'y_actual',
                    size=3,
                    color=cfg.PURPLE,
                    alpha=0.8,
                    legend_label="Actual value",
                    source=source)

        plot.varea('x', 'yhat_lower', 'yhat_upper',
                   fill_alpha=0.2,
                   legend_label="Confidence interval",
                   fill_color=cfg.LIGHT_PURPLE,
                   source=source)

        plot.toolbar.autohide = True
        plot.xaxis.axis_label = "Date"
        plot.yaxis.axis_label = "Price, USD"

        plot1 = plot.line('x', 'y',
                          source=source,
                          line_width=3,
                          legend_label="Prediction",
                          line_color="#eb34e8")
        plot.circle('x', 'y_actual',
                    size=3,
                    color=cfg.DARK_GREEN,
                    alpha=0.8,
                    legend_label="Actual value",
                    source=source)

        plot.add_tools(HoverTool(
            show_arrow=True,
            renderers=[plot1],
            tooltips=[
                ('x', '@x{%F}'),
                ('y', '$@y{%0.2f}'),
                ('y_actual', '$@y_actual{%0.2f}'),
                ('yhat_lower', '$@yhat_lower{%0.2f}'),
                ('yhat_upper', '$@yhat_upper{%0.2f}')
            ],
            formatters={
                '@x': 'datetime',
                '@y': 'printf',
                '@y_actual': 'printf',
                '@yhat_lower': 'printf',
                '@yhat_upper': 'printf',
            },
            mode='vline'
        ))

        self.plot = plot

        button_reset = Button(label="Reset",
                              button_type="success")

        button_reset_callback = CustomJS(args=dict(source=source,
                                                   plot=plot),
                                         code=js.BUTTON_RESET_LSTM)

        button_reset.js_on_click(button_reset_callback)

        layout = column(plot, button_reset)
        tab = Panel(child=layout, title='LSTM predictor')

        return tab

    def make_tabs(self):
        """Draws tabs for predictors graphs.

        Returns:
            script: bokeh script component.
            div: bokeh div component.

        @author: Andrii Koval, Yulia Khlyaka, Pavlo Mospan
        """
        tab1 = self.arima_tab()
        tab2 = self.prophet_tab()
        tab3 = self.lstm_tab()

        tabs = Tabs(tabs=[tab1, tab2, tab3])

        dt_pckr_strt = DatePicker(title='Select start of sync date',
                                  min_date=date(2017, 1, 1),
                                  max_date=date.today())
        start_picker_callback = CustomJS(args=dict(plot=self.plot),
                                         code=js.BUTTON_DATE)
        dt_pckr_strt.js_on_change('value', start_picker_callback)

        button_pred = Button(label="Predict",
                             button_type="success")

        button_pred_callback = CustomJS(args=dict(plot=tabs),
                                        code=js.BUTTON_PRED)
        button_pred.js_on_click(button_pred_callback)

        tab_callback = CustomJS(args=dict(plot=tabs),
                                code=js.BUTTON_TAB)
        tabs.js_on_change('active', tab_callback)

        end_date = date.today() + timedelta(weeks=+4)
        dt_pckr_end = DatePicker(title='Select end of sync date',
                                 min_date=date.today(),
                                 max_date=end_date)
        end_picker_callback = CustomJS(args=dict(plot=self.plot),
                                       code=js.BUTTON_DATE_END)
        dt_pckr_end.js_on_change('value', end_picker_callback)

        but_picker = column(dt_pckr_strt,
                            dt_pckr_end,
                            button_pred)

        layout = row(but_picker, tabs)

        script_tab, div_tab = components(layout)

        return script_tab, div_tab

    def make_plot(self):
        """Draws bitcoin price graph.

        Returns:
            script: bokeh script component.
            div: bokeh div component.

        @author: Andrii Koval, Yulia Khlyaka
        """
        df = prepare_data()
        plot = figure(plot_width=800,
                      plot_height=500,
                      sizing_mode='fixed',
                      x_axis_type="datetime",
                      title="Bitcoin price",
                      **cfg.PLOT_OPTS)

        plot.toolbar.autohide = True
        plot.xaxis.axis_label = "Date"
        plot.yaxis.axis_label = "Price, USD"

        plot.line(x='Date',
                  y='Close',
                  source=df,
                  line_width=3,
                  line_color=cfg.GREEN)
        plot.vbar(x='Date', top='Diff_abs',
                  color='Direction', source=df, width=0.5)

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

        dt_pckr_strt = DatePicker(title='Select start of sync date',
                                  min_date=date(2017, 1, 1),
                                  max_date=date.today())
        dt_pckr_strt2 = DatePicker(title='Select end of sync date',
                                   min_date=date(2017, 1, 1),
                                   max_date=date.today())

        start_picker_callback = CustomJS(args=dict(plot=plot), code="""
            plot.x_range.start = Date.parse(new Date(cb_obj.value));
        """)
        end_picker_callback = CustomJS(args=dict(plot=plot), code="""
            plot.x_range.end = Date.parse(new Date(cb_obj.value));
        """)
        dt_pckr_strt.js_on_change('value', start_picker_callback)
        dt_pckr_strt2.js_on_change('value', end_picker_callback)

        # add a button "update DataSet"
        button_load = Button(label="DATA UPDATE",
                             button_type="success")
        button_update_callback = CustomJS(args=dict(), code="""
                window.open("http://127.0.0.1:5000/dashboard" ,"_self");
                """)
        button_load.js_on_click(button_update_callback)
        button_load_callback = CustomJS(args=dict(), code=js.UPDATE)
        button_load.js_on_click(button_load_callback)
        button_load.js_on_event(events.ButtonClick, data_update())

        but_picker = column(dt_pckr_strt,
                            dt_pckr_strt2,
                            button_load)
        layout = row(but_picker, plot)
        script, div = components(layout)

        return script, div

    def make_trend(self):
        """Draws trend graphs.

        Returns:
            script: bokeh script component.
            div: bokeh div component.

        @author: Andrii Koval
        """
        df = prepare_data()
        seasonal, resid, trend = seasonal_decompose(df)

        plot_season = figure(plot_width=1200,
                             plot_height=300,
                             sizing_mode='fixed',
                             x_axis_type="datetime",
                             title="The seasonal component of the data series.",
                             **cfg.PLOT_OPTS)

        plot_season.toolbar.autohide = True
        plot_season.xaxis.axis_label = "Date"
        plot_season.yaxis.axis_label = "Price, USD"

        plot_season.line(x='Date',
                         y='Close',
                         source=seasonal,
                         line_width=3,
                         line_color='darkseagreen')

        plot_season.add_tools(HoverTool(
            show_arrow=True,
            tooltips=[
                ('date',   '@Date{%F}'),
                ('close',  '$@Close{%0.2f}'),
            ],
            formatters={
                '@Date': 'datetime',
                '@Close': 'printf',
            },
            mode='vline'
        ))

        plot_resid = figure(plot_width=1200,
                            plot_height=300,
                            sizing_mode='fixed',
                            x_axis_type="datetime",
                            title="The residual component of the data series.",
                            **cfg.PLOT_OPTS)

        plot_resid.toolbar.autohide = True
        plot_resid.xaxis.axis_label = "Date"
        plot_resid.yaxis.axis_label = "Price, USD"

        plot_resid.line(x='Date',
                        y='Close',
                        source=resid,
                        line_width=3,
                        line_color='aquamarine')

        plot_resid.add_tools(HoverTool(
            show_arrow=True,
            tooltips=[
                ('date',   '@Date{%F}'),
                ('close',  '$@Close{%0.2f}'),
            ],
            formatters={
                '@Date': 'datetime',
                '@Close': 'printf',
            },
            mode='vline'
        ))

        plot_trend = figure(plot_width=1200,
                            plot_height=300,
                            sizing_mode='fixed',
                            x_axis_type="datetime",
                            title="The trend component of the data series.",
                            **cfg.PLOT_OPTS)

        plot_trend.toolbar.autohide = True
        plot_trend.xaxis.axis_label = "Date"
        plot_trend.yaxis.axis_label = "Price, USD"

        plot_trend.line(x='Date',
                        y='Close',
                        source=trend,
                        line_width=3,
                        line_color='lightgreen')

        plot_trend.add_tools(HoverTool(
            show_arrow=True,
            tooltips=[
                ('date',   '@Date{%F}'),
                ('close',  '$@Close{%0.2f}'),
            ],
            formatters={
                '@Date': 'datetime',
                '@Close': 'printf',
            },
            mode='vline'
        ))

        layout = column(plot_season, plot_resid, plot_trend)
        script, div = components(layout)

        return script, div
