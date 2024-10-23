import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import sys
import os

# Add the project's root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from finance_app.models import StockData  # Now this should work

# Fetch historical stock price data from the database
def fetch_historical_data(symbol):
    # Replace with your actual field names if they differ
    data = StockData.objects.filter(symbol=symbol).values_list('close_price', flat=True)
    return np.array(list(data)).reshape(-1, 1)  # Reshape for sklearn

# Load your target data (this could be future prices, for instance)
# This example assumes your target is the next day's price; adjust as necessary.
def fetch_target_data(symbol):
    # For simplicity, we will just use a placeholder; replace with your actual target data fetching
    return np.array([3, 5, 7, 11, 13])  # Replace with your actual target values

# Example usage
symbol = 'AAPL'  # Example stock symbol

# Get historical and target data
historical_data = fetch_historical_data(symbol)  # Replace with actual feature set
target_data = fetch_target_data(symbol)  # Replace with actual target values

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(historical_data, target_data, test_size=0.2)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the model
model_path = os.path.join(os.path.dirname(__file__), 'stock_price_model.pkl')
joblib.dump(model, model_path)

print(f"Model saved to {model_path}")
