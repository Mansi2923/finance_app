import pandas as pd
import numpy as np
from finance_app.models import StockData


def calculate_metrics(predicted_prices, actual_prices):
    """Calculate key financial metrics."""
    metrics = {}
    metrics['mean_absolute_error'] = np.mean(np.abs(predicted_prices - actual_prices))
    metrics['mean_squared_error'] = np.mean((predicted_prices - actual_prices) ** 2)
    metrics['root_mean_squared_error'] = np.sqrt(metrics['mean_squared_error'])
    # Add other metrics as necessary
    return metrics


def backtest_moving_average_strategy(symbol, short_window=40, long_window=100):
    # Fetch the stock data from the database
    stock_data = StockData.objects.filter(symbol=symbol).order_by('date')
    
    if not stock_data.exists():
        # Return an empty DataFrame instead of a string
        return pd.DataFrame()

    # Convert the query result to a pandas DataFrame for easier manipulation
    data = pd.DataFrame(list(stock_data.values('date', 'close_price')))
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)

    # Calculate the moving averages
    data['short_mavg'] = data['close_price'].rolling(window=short_window, min_periods=1).mean()
    data['long_mavg'] = data['close_price'].rolling(window=long_window, min_periods=1).mean()

    # Create signals
    data['signal'] = 0
    data['signal'][short_window:] = np.where(data['short_mavg'][short_window:] > data['long_mavg'][short_window:], 1, 0)
    
    # Generate trading positions (1: buy, 0: hold/sell)
    data['positions'] = data['signal'].diff()

    # Calculate returns (buy when positions == 1, sell when positions == -1)
    initial_capital = 10000.0  # Example starting capital
    positions = pd.DataFrame(index=data.index).fillna(0.0)
    positions[symbol] = 100 * data['positions']  # Buy 100 shares
    portfolio = positions.multiply(data['close_price'], axis=0)
    portfolio['cash'] = initial_capital - (positions.diff().multiply(data['close_price'], axis=0)).cumsum()
    portfolio['total'] = portfolio[symbol] + portfolio['cash']

    return portfolio

# Example output
def run_backtest(symbol):
    portfolio = backtest_moving_average_strategy(symbol)
    return portfolio

