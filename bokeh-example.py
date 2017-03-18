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
	data_table = DataTable(source=source, columns=columns, width=500, height=280)

	return data_table

def stock_table_update(source, data):
	data_table.source.patch(data)

def datetime(x):
    return np.array(x, dtype=np.datetime64)




p1 = figure(x_axis_type="datetime", title="Stock Closing Prices", width=600)
p1.grid.grid_line_alpha=0.3
p1.xaxis.axis_label = 'Date'
p1.yaxis.axis_label = 'Price'

print(AAPL['date'][0:10])
p1.line(datetime(AAPL['date']), AAPL['adj_close'], color='#A6CEE3', legend='AAPL')
p1.line(datetime(GOOG['date']), GOOG['adj_close'], color='#B2DF8A', legend='GOOG')
p1.line(datetime(IBM['date']), IBM['adj_close'], color='#33A02C', legend='IBM')
p1.line(datetime(MSFT['date']), MSFT['adj_close'], color='#FB9A99', legend='MSFT')
p1.legend.location = "top_left"



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

data_table = build_stock_table(data)

#show(row([data_table,p1]))  # open a browser
#show()

session = push_session(curdoc())
#curdoc().add_periodic_callback(update, 10) #period in ms
session.show()
session.loop_until_closed()

output_file("stocks.html", title="stocks.py example")



new_data = dict(
        symbol=[(0,'AAPL')],
        lastTrade=[(0,136.2)],
        change = [(0, -31)],
        high = [(0, 1370)],
        low = [(0, 12)],
        bid = [(0, 133)],
        ask = [(0, 32)],
        spread = [(0, 1)]
    )

data_table.source.patch(new_data)
print('DONE')
#stock_table_update(data_table, new_data)

