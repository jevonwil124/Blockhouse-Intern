import pandas as pd
from stock_data.models import StockPrice

def generate_report(symbol):
    prices = StockPrice.objects.filter(symbol=symbol).values('timestamp', 'open_price', 'close_price', 'high_price', 'low_price', 'volume')
    df = pd.DataFrame.from_records(prices)

    # Save report as CSV
    report_file = f'{symbol}_report.csv'
    df.to_csv(report_file, index=False)

    return report_file
