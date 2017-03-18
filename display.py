from socketIO_client import SocketIO

# myapp.py
import numpy as np
from bokeh.layouts import gridplot, layout, row, column
from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.stocks import AAPL, GOOG, IBM, MSFT
from random import randint
from datetime import date
from random import randint
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, Button, Select, TextInput
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
from bokeh.palettes import (Blues9, BrBG9, BuGn9, BuPu9, GnBu9, Greens9,
                            Greys9, OrRd9, Oranges9, PRGn9, PiYG9, PuBu9,
                            PuBuGn9, PuOr9, PuRd9, Purples9, RdBu9, RdGy9,
                            RdPu9, RdYlBu9, RdYlGn9, Reds9, Spectral9, YlGn9,
                            YlGnBu9, YlOrBr9, YlOrRd9, Inferno9, Magma9,
                            Plasma9, Viridis9, Accent8, Dark2_8, Paired9,
                            Pastel1_9, Pastel2_8, Set1_9, Set2_8, Set3_9,
                            )


standard_palettes = ['#3288bd', '#99d594', '#e6f598', '#fee08b', '#fc8d59', '#d53e4f', Blues9[0], BrBG9[0], BuGn9[0], BuPu9[0], GnBu9[0], Greens9[0],
                            Greys9[0], OrRd9[0], Oranges9[0], PRGn9[0], PiYG9[0], PuBu9[0],
                            PuBuGn9[0], PuOr9[0], PuRd9[0], Purples9[0], RdBu9[0], RdGy9[0],
                            RdPu9[0], RdYlBu9[0], RdYlGn9[0], Reds9[0], Spectral9[0], YlGn9[0],
                            YlGnBu9[0], YlOrBr9[0], YlOrRd9[0], Inferno9[0], Magma9[0],
                            Plasma9[0], Viridis9[0], Accent8[0], Dark2_8[0], Paired9[0],
                            Pastel1_9[0], Pastel2_8[0], Set1_9[0], Set2_8[0], Set3_9[0]]


fileName = 'current_stats.pkl'
plotfileName = 'current_plot_files.pkl'
lines = dict()

def datetime(x):
    print(x)
    return np.array(x, dtype=np.datetime64)


def build_order_table(data):

    source = ColumnDataSource(data)

    columns = [
            TableColumn(field="clientOrderId", title="clientOrderId"),
            TableColumn(field="status", title="status"),
            TableColumn(field="symbol", title="symbol"),
            TableColumn(field="side", title="side"),
            TableColumn(field="Qty", title="Qty"),
            TableColumn(field="EQty", title="EQty"),
            TableColumn(field="Avg", title="Avg"),
            TableColumn(field="PNL", title="PNL")
        ]
    data_table = DataTable(source=source, columns=columns, width=600, height = 200)

    return data_table


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
    data_table = DataTable(source=source, columns=columns, width=600, height = 500)

    return data_table



def update_table(data_table, data):
    data_table.source.data = data


def build_plot(data):
    p1 = figure(x_axis_type="datetime", title="Stock Prices - change", width=600, height = 400)
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Time'
    p1.yaxis.axis_label = 'Price'
    colors_indexes = np.random.permutation(list(range(len(standard_palettes))))
    color_index = 0
    for key in data :

        lines[key] = p1.line(data[key]['time'], data[key]['lastTrade'], legend=key, line_color = standard_palettes[colors_indexes[color_index]])
        color_index = color_index + 1
        if color_index == len(standard_palettes):
        	color_index = 0

    p1.legend.location = "top_left"
    return lines, p1





def update_plot(lines, new_data):
	for key in new_data:
		lines[key].data_source.data['x']  = lines[key].data_source.data['x'] + new_data[key]['time']
		lines[key].data_source.data['y'] = lines[key].data_source.data['y']  + new_data[key]['lastTrade']

################## TO REMOVE ####################


plot_f = open(plotfileName, 'rb')
plot_data = pickle.load(plot_f)
lines, p1 = build_plot(plot_data)
plot_f.close()


#################################################




f = open(fileName, 'rb')
current_stats = pickle.load(f)
data_table = build_stock_table(current_stats)
f.close()
currentPNL = 0
# put the button and plot in a layout and add to the document

server = 'http://emsapi.eu-west-2.elasticbeanstalk.com'
stocks_list = ['AAPL', 'AMD', 'BAC', 'BMY', 'C', 'CSCO', 'CYH', 'FB', 'FCX', 'GE',
               'MDLZ', 'MSFT', 'WMT', 'MU', 'INTC', 'PFE', 'VZ', 'WFX', 'XOM'
               ]


quantity = 100
def quantity_handler(attr, old, new):
	global quantity
	quantity = int(new)

symbol = stocks_list[0]
def ticker_handler(attr, old, new):
	global symbol
	symbol = new.upper()

def sellThreadFunc():
    global quantity
    global symbol
    t = Thread(target =sellFunc, args = (symbol, quantity))
    t.start()

def buyThreadFunc():
    global quantity
    global symbol
    t = Thread(target =buyFunc, args = (symbol, quantity))
    t.start()

def sellFunc(symbol, quantity):
	launch_order(symbol, quantity, 'SELL')

def buyFunc(symbol, quantity):
	launch_order(symbol, quantity, 'BUY')


trades = dict(symbol = [],
              side = [],
              exec_qty = [],
              exec_price = []
             )



newOrderSymbol = 'AAPL'
newOrderSide = 'BUY'

def order_response(*args):
    global newOrderSide
    global newOrderSymbol

    if(args[0]['type']=='ExecutionReport'):
    	print('Order RECEIVED : \n', args[0])
    
    symbol = newOrderSymbol
    side = 1 if newOrderSide == 'BUY' else -1
    if (args[0]['type']=='ExecutionReport'):
        trades['symbol'].append(symbol)
        trades['side'].append(side)
        trades['exec_qty'].append(args[0]['qty'])
        trades['exec_price'].append(args[0]['price'])


def compute_pnl(current_stats):
    global trades
    pnl = 0
    for i in range(len(trades['side'])):
        pnl += float(trades['side'][i])*(float(current_stats['lastTrade'][current_stats['symbol'].index(trades['symbol'][i])]) - float(trades['exec_price'][i]))*float(trades['exec_qty'][i])
    return pnl


def launch_order(symbol, qty, OrderType, clientOrderId = 13):
    global newOrderSide
    global newOrderSymbol
    newOrderSymbol = symbol
    newOrderSide = OrderType

    NewOrder = {'type': 'NewOrder', 'clientOrderId': str(clientOrderId), 'symbol': symbol , 'buySell': OrderType, 'qty': qty}
    with SocketIO(server) as socketIO:
        socketIO.emit('submitOrder', NewOrder)
        socketIO.on('onOrderMessage', order_response)
        socketIO.wait()




buyButton = Button(label="BUY", button_type="success")
buyButton.on_click(buyThreadFunc)

sellButton = Button(label="SELL", button_type="warning")
sellButton.on_click(sellThreadFunc)

select = Select(title="Ticker:", value=stocks_list[0], options=stocks_list)
select.on_change("value", ticker_handler)

quantity_input = TextInput(value="100", title="quantity:")
quantity_input.on_change("value", quantity_handler)


if currentPNL == 0 : 
    PNLbutton = Button(label="PNL : " + str(currentPNL), button_type="warning")
elif currentPNL >0 : 
    PNLbutton = Button(label="PNL : " + str(currentPNL), button_type="success")
else:
    PNLbutton = Button(label="PNL : " + str(currentPNL), button_type="danger")


disp_buttons =  dict(AAPL = Button(label= 'AAPL', button_type = "success"),
          AMD = Button(label= 'AMD', button_type = "success"),
          BAC = Button(label= 'BAC' , button_type = "success"),
          BMY = Button(label= 'BMY', button_type = "success"),
          C = Button(label= 'C', button_type = "success"),
          CSCO = Button(label= 'CSCO', button_type = "success"),
          CYH = Button(label= 'CYH', button_type = "success"),
          FB = Button(label= 'FB', button_type = "success"),
          FCX = Button(label= 'FCX', button_type = "success"),
          GE = Button(label= 'GE' , button_type = "success"),
          INTC = Button(label= 'INTC', button_type = "success"),
          MDLZ = Button(label= 'MDLZ', button_type = "success"),
          MSFT = Button(label= 'MSFT', button_type = "success"),
          MU = Button(label= 'MU', button_type = "success"),
          PFE = Button(label= 'PFE', button_type = "success"),
          VZ = Button(label= 'VZ', button_type = "success"),
          WFX = Button(label= 'WFX', button_type = "success"),
          WMT = Button(label= 'WMT', button_type = "success"),
          XOM = Button(label= 'XOM', button_type = "success")
            )


def update_display():

    print('update')
    f = open(fileName, 'rb')
    current_stats = pickle.load(f)
    f.close()
    update_table(data_table, current_stats)
    f_plot = open(plotfileName, 'rb')
    new_plot_data = pickle.load(f_plot)
    update_plot(lines,new_plot_data)
    f_plot.close()
    compute_pnl
    currentPNL = compute_pnl(current_stats)
    if currentPNL == 0 : 
        PNLbutton.label = "PNL : " + str(currentPNL)
        PNLbutton.button_type = "warning" 
    elif currentPNL >0 : 
        PNLbutton.label = "PNL : " + str(currentPNL)
        PNLbutton.button_type = "success" 
    else:
        PNLbutton.label = "PNL : " + str(currentPNL)
        PNLbutton.button_type = "danger" 


curdoc().add_root(row([column([column([data_table,row([sellButton, buyButton]),row([select,quantity_input])]),PNLbutton]),column([p1, column([row([disp_buttons[stocks_list[i*3+j]] for j in range(0,min(len(stocks_list)-i*3,3))]) for i in range(0,int(np.floor(len(stocks_list)/3)+1))])])]))
curdoc().add_periodic_callback(update_display, 1000)
