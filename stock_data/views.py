from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .backtesting import backtest_strategy
from .ml_model import StockPricePredictor
from .reports import generate_report

@api_view(['POST'])
def backtest(request):
    symbol = request.data.get('symbol')
    initial_investment = request.data.get('initial_investment', 1000)
    result = backtest_strategy(symbol, initial_investment)

    if result:
        return Response(result, status=status.HTTP_200_OK)
    return Response({'error': 'Not enough data for backtesting.'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def predict(request):
    symbol = request.data.get('symbol')
    predictor = StockPricePredictor('path/to/your/model.pkl')
    predictions = predictor.predict(symbol)

    if predictions is not None:
        return Response(predictions.tolist(), status=status.HTTP_200_OK)
    return Response({'error': 'No historical data found for this symbol.'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def report(request, symbol):
    report_file = generate_report(symbol)
    with open(report_file, 'rb') as file:
        response = HttpResponse(file.read(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{report_file}"'
        return response


