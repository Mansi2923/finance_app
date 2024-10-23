# finance_app/services/metrics.py

import numpy as np

def calculate_metrics(predicted_prices, actual_prices):
    """Calculate key financial metrics."""
    metrics = {}
    metrics['mean_absolute_error'] = np.mean(np.abs(predicted_prices - actual_prices))
    metrics['mean_squared_error'] = np.mean((predicted_prices - actual_prices) ** 2)
    metrics['root_mean_squared_error'] = np.sqrt(metrics['mean_squared_error'])
    # Add other metrics as necessary
    return metrics
