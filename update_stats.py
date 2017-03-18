from socketIO_client import SocketIO
import numpy as np


# myapp.py
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
from threading import Thread
 
from random import random

from bokeh.layouts import column
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
import pickle

server = 'http://emsapi.eu-west-2.elasticbeanstalk.com'
stocks_list = ['AAPL', 'AMD', 'BAC', 'BMY', 'C', 'CSCO', 'CYH', 'FB', 'FCX', 'GE', 'INTC', 'MDLZ', 'MSFT', 'WMT', 'MU', 'INTC', 'PFE', 'VZ', 'WFX', 'WMT', 'XOM']


current_stats = dict(symbol = ['AAPL', 'AMD', 'BAC', 'BMY', 'C', 'CSCO', 'CYH', 'FB', 'FCX', 'GE', 'INTC', 'MDLZ', 'MSFT', 'MU', 'PFE', 'VZ', 'WFX', 'WMT', 'XOM'],
                     lastTrade = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     change = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     high = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     low = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
                     bid = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     ask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     spread = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                     )

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
    p1 = figure(x_axis_type="datetime", title="Stock Prices", width=600, height = 600)
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
    lines[new_data['symbol']].data_source.data['y'].append(new_data[new_data['symbol']]['lastTrade'])

################## TO REMOVE ####################

plot_data = dict(
    symbol=['AAPL'],
    AAPL = dict(
            time = [time.time()],
            lastTrade = [15]
        )
    )

#################################################

def buildDisplay():

    data_table = build_stock_table(current_stats)
    lines, p1 = build_plot(plot_data)

    # put the button and plot in a layout and add to the document

    curdoc().add_root(row([data_table,p1]))
    while True:
        print('updating')
        update_display(data_table)
        time.sleep(5)


def update_display(data_table):
    print('updating')
    update_stock_table(data_table, current_stats)

#



## curdoc().add_periodic_callback(random_update, 1000)

timer = 0
plot_dict = dict(AAPL = dict(
            time = [],
            lastTrade = []),
  AMD = dict(
    time = [],
    lastTrade = []),
  BAC = dict(
    time = [],
    lastTrade = []),
  BMY = dict(
    time = [],
    lastTrade = []),
  C = dict(
    time = [],
    lastTrade = []),
  CSCO = dict(
    time = [],
    lastTrade = []),
  CYH = dict(
    time = [],
    lastTrade = []),
  FB = dict(
    time = [],
    lastTrade = []),
  FCX = dict(
    time = [],
    lastTrade = []),
  GE = dict(
    time = [],
    lastTrade = []),
  INTC = dict(
    time = [],
    lastTrade = []),
  MDLZ = dict(
    time = [],
    lastTrade = []),
  MSFT = dict(
    time = [],
    lastTrade = []),
  WMT = dict(
    time = [],
    lastTrade = []),
  MU = dict(
    time = [],
    lastTrade = []),
  PFE = dict(
    time = [],
    lastTrade = []),
  VZ = dict(
    time = [],
    lastTrade = []),
  WFX = dict(
    time = [],
    lastTrade = []),
  XOM = dict(
    time = [],
    lastTrade = [])
    )



def market_data_response(*args):
    global timer
    global plot_dict
    if args[0]['type'] == 'BBO':
        current_ticker = args[0]['symbol']
        current_ticker_index = current_stats['symbol'].index(current_ticker)
        # update bid, ask, spread
        current_stats['bid'][current_ticker_index] = args[0]['bid']
        # ask
        current_stats['ask'][current_ticker_index] = args[0]['ask']
        # spread
        current_stats['spread'][current_ticker_index] = round(float(args[0]['ask']) - float(args[0]['bid']), 4)

    if args[0]['type'] == 'TRADE':
        current_ticker = args[0]['symbol']
        current_ticker_index = current_stats['symbol'].index(current_ticker)
        # lastPrice, change, high, low
        previous_price = current_stats['lastTrade'][current_ticker_index]
        current_stats['lastTrade'][current_ticker_index] = args[0]['lastPrice']
        # chance
        current_stats['change'][current_ticker_index] = float(previous_price) - float(current_stats['lastTrade'][current_ticker_index])
        # high
        if(float(args[0]['lastPrice']) > float(current_stats['high'][current_ticker_index])):
            current_stats['high'][current_ticker_index] = args[0]['lastPrice']
        # low
        if(float(args[0]['lastPrice']) < float(current_stats['low'][current_ticker_index])):
            current_stats['low'][current_ticker_index] = args[0]['lastPrice']

        plot_dict[args[0]['symbol']]['lastTrade'].append((float(args[0]['lastPrice']) - float(previous_price))/float(previous_price))
        plot_dict[args[0]['symbol']]['time'].append(args[0]['time'])

    if (timer == 0) or ((time.time() - timer)>=0.5):
        timer = time.time()
        fileName = 'current_stats.pkl'
        f = open(fileName, 'wb')
        pickle.dump(current_stats,f)
        plotfileName = 'current_plot_files.pkl'
        plot_f = open(plotfileName, 'wb')
        pickle.dump(plot_dict,plot_f)
        plot_dict = dict(AAPL = dict(
            time = [],
            lastTrade = []),
          AMD = dict(
            time = [],
            lastTrade = []),
          BAC = dict(
            time = [],
            lastTrade = []),
          BMY = dict(
            time = [],
            lastTrade = []),
          C = dict(
            time = [],
            lastTrade = []),
          CSCO = dict(
            time = [],
            lastTrade = []),
          CYH = dict(
            time = [],
            lastTrade = []),
          FB = dict(
            time = [],
            lastTrade = []),
          FCX = dict(
            time = [],
            lastTrade = []),
          GE = dict(
            time = [],
            lastTrade = []),
          INTC = dict(
            time = [],
            lastTrade = []),
          MDLZ = dict(
            time = [],
            lastTrade = []),
          MSFT = dict(
            time = [],
            lastTrade = []),
          MU = dict(
            time = [],
            lastTrade = []),
          PFE = dict(
            time = [],
            lastTrade = []),
          VZ = dict(
            time = [],
            lastTrade = []),
          WFX = dict(
            time = [],
            lastTrade = []),
          WMT = dict(
            time = [],
            lastTrade = []),
          XOM = dict(
            time = [],
            lastTrade = [])
            )
        print('saved')

def listen():
    print('Thread Started')
    with SocketIO(server) as socketIO:
        socketIO.on('onMarketData', market_data_response)
        socketIO.emit('subscribe', stocks_list)
        socketIO.wait()

# t2 = Thread(target = buildDisplay)
# t2.start()
# t2.join()
t = Thread(target = listen)
t.start()
t.join()