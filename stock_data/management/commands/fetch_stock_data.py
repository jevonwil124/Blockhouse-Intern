import requests
from django.core.management.base import BaseCommand
from stock_data.models import StockPrice
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Fetch financial data from Alpha Vantage API'

    def handle(self, *args, **kwargs):
        symbol = 'AAPL'  # You can change this to any stock symbol you want
        api_key = 'WJL49CK6946B6UXY'  # Replace with your API key
        end_date = datetime.now()
        start_date = end_date - timedelta(days=730)  # 2 years of data
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&datatype=json'

        response = requests.get(url)
        if response.status_code != 200:
            self.stderr.write(f"Error fetching data: {response.text}")
            return

        data = response.json().get('Time Series (Daily)', {})
        for date_str, metrics in data.items():
            # Parse date_str into a datetime object
            date = datetime.strptime(date_str, '%Y-%m-%d')

            # Compare datetime objects
            if start_date <= date <= end_date:
                StockPrice.objects.update_or_create(
                    symbol=symbol,
                    timestamp=date.date(),  # Store the date part only
                    defaults={
                        'open_price': float(metrics['1. open']),
                        'close_price': float(metrics['4. close']),
                        'high_price': float(metrics['2. high']),
                        'low_price': float(metrics['3. low']),
                        'volume': int(metrics['5. volume']),
                    }
                )
        self.stdout.write('Financial data fetched successfully.')

