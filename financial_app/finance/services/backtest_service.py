# finance/services/backtest_service.py
from finance.models import StockData
import numpy as np

def moving_average(data, window):
    return np.convolve(data, np.ones(window), 'valid') / window

def backtest(symbol, initial_investment, short_window=50, long_window=200):
    stock_data = StockData.objects.filter(symbol=symbol).order_by('date')
    closes = [float(data.close_price) for data in stock_data]
    dates = [data.date for data in stock_data]

    short_ma = moving_average(closes, short_window)
    long_ma = moving_average(closes, long_window)

    position = None
    balance = initial_investment
    for i in range(len(long_ma)):
        if short_ma[i] < long_ma[i] and position is None:
            position = balance / closes[i]
            balance = 0
        elif short_ma[i] > long_ma[i] and position is not None:
            balance = position * closes[i]
            position = None

    return {"total_balance": balance, "number_of_trades": position is None}

