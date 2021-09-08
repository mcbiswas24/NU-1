from django.shortcuts import render
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# Create your views here.
def MainPage(request):
    stock_data = pd.read_json(r'C:\Users\DELL\Desktop\Hackathon\OHCLEngine\Dashboard\stock_list.json')
    symbols = stock_data['symbol'].unique().tolist()
    stock = stock_data[stock_data['symbol'] == 'AAPL']
    stock = stock[['open','close','high','low','date']]

    sym = yf.Ticker("AAPL")

    descr = sym.info['longBusinessSummary']
    com_name = sym.info['longName']

    fig = go.Figure(data=go.Ohlc(x=stock['date'],
                open=stock['open'],
                high=stock['high'],
                low=stock['low'],
                close=stock['close']))
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.write_image(r"C:\Users\DELL\Desktop\Hackathon\OHCLEngine\Dashboard\static\Dashboard\Images\fig1.png")


    return render(request,"Dashboard/index.html",{'symbols':symbols,'stock':stock,'name': com_name,'descr': descr,'sym_name':'AAPL',
    'interval':'Monthly'})

def ShowStock(request):
    symbol = request.POST['symbol']
    interval = request.POST['interval']

    stock_data = pd.read_json(r'C:\Users\DELL\Desktop\Hackathon\OHCLEngine\Dashboard\stock_list.json')
    symbols = stock_data['symbol'].unique().tolist()
    stock = stock_data[stock_data['symbol'] == symbol]
    stock = stock[['open','close','high','low','date']]
    sym = yf.Ticker(symbol)

    descr = sym.info['longBusinessSummary']
    com_name = sym.info['longName']
    

    if interval == "Weekly":
        stock['week'] = stock['date'].dt.week
        st = stock.groupby(['week']).agg({'open':'first', 'high':'max', 'low':'min', 'close':'last'})
        st['date'] = stock['week'].unique()
        stock = st.copy()

    fig = go.Figure(data=go.Ohlc(x=stock['date'],
                open=stock['open'],
                high=stock['high'],
                low=stock['low'],
                close=stock['close']))
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.write_image(r"C:\Users\DELL\Desktop\Hackathon\OHCLEngine\Dashboard\static\Dashboard\Images\fig1.png")

    return render(request,"Dashboard/index.html",{'symbols':symbols,'stock':stock,'name': com_name,'descr': descr,'sym_name':symbol,
    'interval':interval})