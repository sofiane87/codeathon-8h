# myapp.py
import numpy as np
from bokeh.layouts import gridplot, layout, row, column
from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.stocks import AAPL, GOOG, IBM, MSFT
from random import randint
from datetime import date
from random import randint
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.io import output_file, show
from bokeh.models.layouts import WidgetBox
from bokeh.models.layouts import VBox as vform
from bokeh.client import push_session
from bokeh.plotting import curdoc
import time


from random import random

from bokeh.layouts import column
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc


def datetime(x):
    print(x)
    return np.array(x, dtype=np.datetime64)


def build_stock_table(data):

    source = ColumnDataSource(data)

    columns = [
            TableColumn(field="symbol", title="Symbol"),
            TableColumn(field="lastTrade", title="LastTrade"),
            TableColumn(field="change", title="Change"),
            TableColumn(field="high", title="High"),
            TableColumn(field="low", title="Low"),
            TableColumn(field="bid", title="Bid"),
            TableColumn(field="ask", title="Ask"),
            TableColumn(field="spread", title="Spread")
        ]
    data_table = DataTable(source=source, columns=columns, width=600)

    return data_table

def update_stock_table(data_table, data):
    data_table.source.data = data


def build_plot(data):
    p1 = figure(x_axis_type="datetime", title="Stock Prices", width=600, height = 400)
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'
    lines = dict()

    for i in range(len(data['symbol'])):
        lines[data['symbol'][i]] = p1.line(data[data['symbol'][i]]['time'], data[data['symbol'][i]]['lastTrade'], legend=data['symbol'][i])

    p1.legend.location = "top_left"
    return lines, p1


def update_plot(plot_handle, lines, new_data):
    lines[new_data['symbol']].data_source.data['x'].append(new_data[new_data['symbol']]['time'])
    print(len(lines[new_data['symbol']].data_source.data['x']))
    lines[new_data['symbol']].data_source.data['y'].append(new_data[new_data['symbol']]['lastTrade'])
    print(len(lines[new_data['symbol']].data_source.data['y']))


data = dict(
        symbol=['AAPL'],
        lastTrade=[136.2],
        change = [-3],
        high = [137],
        low = [126],
        bid = [13],
        ask = [32],
        spread = [1]
    )


plot_data = dict(
    symbol=['AAPL'],
    AAPL = dict(
            time = [time.time()],
            lastTrade = [15]
        )
    )
data_table = build_stock_table(data)
lines, p1 = build_plot(plot_data)

i = 0

ds = data_table.source


# create a callback that will add a number in a random location
def random_update():
    global i


    ### Updating the table
    new_data = dict(
        symbol=['AAPL'],
        lastTrade=[random()*70 + 15],
        change = [ random()*70 + 15],
        high = [ random()*70 + 15],
        low = [ random()*70 + 15],
        bid = [ random()*70 + 15],
        ask = [ random()*70 + 15],
        spread = [ random()*70 + 15]
    )

    # BEST PRACTICE --- update .data in one step with a new dict
    update_stock_table(data_table, new_data)

    ### Updating Plot
    new_plot_data = dict(
        symbol='AAPL',
        AAPL = dict(
                time = time.time(),
                lastTrade = random()*2 + 15
            )
        )

    ## 
    update_plot(p1, lines,new_plot_data)
    i = i + 1



session = push_session(curdoc())


# put the button and plot in a layout and add to the document
curdoc().add_root(row([data_table,p1]))
curdoc().add_periodic_callback(random_update, 1000)

session.show() # open the document in a browser

session.loop_until_closed() # run forever