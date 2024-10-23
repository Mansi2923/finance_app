import joblib
import os

def load_model():
    model_path = os.path.join(os.path.dirname(__file__), 'stock_price_model.pkl')
    model = joblib.load(model_path)
    return model

def predict_prices(model, historical_data):
    # Prepare the data for prediction
    X_predict = historical_data[-30:]  # Use the last 30 days for prediction
    return model.predict(X_predict.reshape(-1, 1))  # Adjust shape as needed
