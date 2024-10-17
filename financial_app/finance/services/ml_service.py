# finance/services/ml_service.py
import joblib

def load_model():
    return joblib.load('path_to_model.pkl')

def predict_prices(symbol):
    model = load_model()
    stock_data = StockData.objects.filter(symbol=symbol).order_by('date')
    closes = [float(data.close_price) for data in stock_data]
    predictions = model.predict([closes[-30:]])  # Predict next 30 days
    return predictions
