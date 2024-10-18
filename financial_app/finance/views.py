# finance/views.py
from django.http import JsonResponse
from finance.services.backtest_service import backtest
from finance.services.ml_service import predict_prices
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse
from .models import StockData  # Import your model to fetch data

from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Financial App!")


def backtest_view(request):
    symbol = request.GET.get('symbol', 'AAPL')
    initial_investment = float(request.GET.get('investment', 10000))
    result = backtest(symbol, initial_investment)
    return JsonResponse(result)



def predict_view(request, symbol):
    predictions = predict_prices(symbol)
    return JsonResponse({'symbol': symbol, 'predictions': predictions})



def generate_report(request, symbol):
    # Fetch actual and predicted data
    # This is just an example; you'll need to define how to fetch your data
    stock_data = StockData.objects.filter(symbol=symbol).order_by('date')
    
    dates = [data.date for data in stock_data]
    actual_prices = [data.close_price for data in stock_data]

    # Fetch predictions from your predictions table or logic
    # Replace the following line with your logic to get predicted data
    predicted_prices = [data.close_price * 1.05 for data in stock_data]  # Dummy prediction logic

    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(dates, actual_prices, label='Actual', marker='o')
    ax.plot(dates, predicted_prices, label='Predicted', marker='x')
    
    ax.set_title(f'Stock Prices for {symbol}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Return the plot as a PDF
    buffer = BytesIO()
    plt.savefig(buffer, format='pdf')
    buffer.seek(0)
    plt.close(fig)  # Close the figure to free memory

    return HttpResponse(buffer, content_type='application/pdf')

