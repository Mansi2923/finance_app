# finance_app/services/reporting.py
import matplotlib.pyplot as plt
import numpy as np

def plot_predictions(actual_prices, predicted_prices):
    plt.figure(figsize=(10, 5))
    plt.plot(actual_prices, label='Actual Prices', color='blue')
    plt.plot(predicted_prices, label='Predicted Prices', color='orange')
    plt.title('Actual vs Predicted Prices')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.savefig('finance_app/static/prediction_plot.png')  # Save the plot in a static directory

def calculate_metrics(backtest_results):
    total_return = ...  # Your calculation logic
    sharpe_ratio = ...  # Your calculation logic
    max_drawdown = ...  # Your calculation logic
    volatility = ...     # Your calculation logic
    win_rate = ...       # Your calculation logic

    return {
        "total_return": total_return,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "volatility": volatility,
        "win_rate": win_rate,
    }
