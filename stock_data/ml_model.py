import pickle
import numpy as np
from stock_data.models import StockPrice

class StockPricePredictor:
    def __init__(self, model_path):
        with open(model_path, 'rb') as file:
            self.model = pickle.load(file)

    def predict(self, symbol):
        prices = StockPrice.objects.filter(symbol=symbol).order_by('timestamp')
        if not prices.exists():
            return None
        features = np.array([price.close_price for price in prices])[-30:]  # Last 30 days
        predictions = self.model.predict(features.reshape(-1, 1))  # Reshape for single feature
        return predictions
