import requests

ALPHA_VANTAGE_API_KEY = 'your_api_key_here'  # Replace with your actual API key

def test_fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        
        print("Fetched data:", data)
        
        if 'Time Series (Daily)' in data:
            print(f"Successfully fetched data for {symbol}.")
        else:
            print("Error: Unable to fetch stock data. Response:", data)
    except requests.exceptions.RequestException as e:
        print("Network error occurred:", e)
    except Exception as e:
        print("An error occurred:", e)

# Test the function with a single symbol
test_fetch_stock_data('AAPL')
