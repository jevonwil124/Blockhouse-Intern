# finance/management/commands/fetch_stock_data.py
import requests
from django.core.management.base import BaseCommand
from finance.models import StockData
from datetime import datetime
import time

ALPHA_VANTAGE_API_KEY = 'DKLM4XCNK5LTI103'

class Command(BaseCommand):
    help = 'Fetches daily stock data from Alpha Vantage API'

    def handle(self, *args, **kwargs):
        symbol = "AAPL"
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}&outputsize=full"
        response = requests.get(url)
        data = response.json().get("Time Series (Daily)", {})
        
        for date_str, prices in data.items():
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            StockData.objects.update_or_create(
                symbol=symbol,
                date=date,
                defaults={
                    'open_price': prices['1. open'],
                    'close_price': prices['4. close'],
                    'high_price': prices['2. high'],
                    'low_price': prices['3. low'],
                    'volume': prices['5. volume'],
                }
            )
        self.stdout.write(self.style.SUCCESS(f"Successfully fetched data for {symbol}"))
