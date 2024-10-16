from django.test import TestCase
from .backtesting import backtest_strategy

class BacktestStrategyTests(TestCase):
    def test_backtest_strategy(self):
        result = backtest_strategy('AAPL', 1000)
        self.assertIsNotNone(result)
        self.assertIn('total_return', result)
        self.assertIn('trades_executed', result)

