import requests
from django.shortcuts import render
from .models import StockData
from .services.backtesting import run_backtest, backtest_moving_average_strategy
from .services.ml_model import load_model, predict_prices
import numpy as np
from .services.metrics import calculate_metrics
from django.http import HttpResponse, JsonResponse
import pandas as pd 




ALPHA_VANTAGE_API_KEY = 'M1E0IS480KTP9GQL'

def fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()

    # Debug print to see the fetched data
    print("Fetched data:", data)

    if 'Time Series (Daily)' in data:
        for date, values in data['Time Series (Daily)'].items():
            StockData.objects.update_or_create(
                symbol=symbol,
                date=date,
                defaults={
                    'open_price': values['1. open'],
                    'close_price': values['4. close'],
                    'high_price': values['2. high'],
                    'low_price': values['3. low'],
                    'volume': values['5. volume'],
                }
            )
    else:
        print("Error: Unable to fetch stock data. Response:", data)

model = load_model()

def home(request):
    # Fetch stock data for AAPL (or any symbol you choose)
    fetch_stock_data('AAPL')

    # Load the model
    model = load_model()

    # Assuming you want to use historical stock data from your database
    historical_data = StockData.objects.filter(symbol='AAPL').values_list('close_price', flat=True)
    historical_data = np.array(list(historical_data))  # Convert to NumPy array for prediction

    # Run the prediction
    predicted_prices = predict_prices(model, historical_data)

    # Prepare the portfolio using your backtest function
    portfolio = run_backtest('AAPL')

    # Assuming you have actual prices to compare with, you can get them like this:
    actual_prices = historical_data[-len(predicted_prices):]  # Take the last N prices to match predicted prices

    # Calculate metrics
    metrics = calculate_metrics(predicted_prices, actual_prices)  # Pass both predicted and actual prices

    # Check if portfolio is empty
    if isinstance(portfolio, str):  # Check if an error message was returned
        portfolio_dict = {"error": portfolio}  # Set error message in the context
    elif portfolio.empty:
        portfolio_dict = {}
    else:
        portfolio_dict = portfolio.to_dict('index')  # Convert portfolio data to dictionary for display

    context = {
        'stocks': StockData.objects.all(),
        'portfolio': portfolio_dict,
        'predicted_prices': predicted_prices,
        'metrics': metrics  # Include metrics in context if needed
    }

    return render(request, 'home.html', context)


def download_report(request):
    # Fetch your stock data or metrics for the report
    stock_data = StockData.objects.filter(symbol='AAPL').values()
    # Convert to DataFrame for easy handling
    df = pd.DataFrame.from_records(stock_data)

    # You can perform any necessary calculations or manipulations here
    # For example, adding key metrics to the report

    # Create a CSV file from the DataFrame
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stock_report.csv"'

    df.to_csv(response, index=False)
    return response