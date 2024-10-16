import numpy as np
from stock_data.models import StockPrice

def backtest_strategy(symbol, initial_investment, moving_avg_short=50, moving_avg_long=200):
    prices = StockPrice.objects.filter(symbol=symbol).order_by('timestamp')
    prices_list = [price.close_price for price in prices]

    if len(prices_list) < moving_avg_long:
        return None  # Not enough data

    signals = np.zeros(len(prices_list))
    moving_avg_short_values = np.convolve(prices_list, np.ones(moving_avg_short)/moving_avg_short, mode='valid')
    moving_avg_long_values = np.convolve(prices_list, np.ones(moving_avg_long)/moving_avg_long, mode='valid')

    for i in range(1, len(moving_avg_short_values)):
        if moving_avg_short_values[i-1] > moving_avg_long_values[i-1] and moving_avg_short_values[i] <= moving_avg_long_values[i]:
            signals[i + moving_avg_short - 1] = -1  # Sell signal
        elif moving_avg_short_values[i-1] < moving_avg_long_values[i-1] and moving_avg_short_values[i] >= moving_avg_long_values[i]:
            signals[i + moving_avg_short - 1] = 1  # Buy signal

    # Calculate returns based on signals
    invested = initial_investment
    shares = 0
    total_return = 0

    for i in range(len(signals)):
        if signals[i] == 1:  # Buy
            shares = invested / prices_list[i]
            invested = 0
        elif signals[i] == -1 and shares > 0:  # Sell
            invested = shares * prices_list[i]
            shares = 0

    total_return = invested if invested > 0 else shares * prices_list[-1]
    return {
        'total_return': total_return,
        'trades_executed': np.sum(np.abs(signals)),
        'final_balance': total_return + initial_investment
    }
