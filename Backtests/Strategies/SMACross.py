from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd


def SMA(array, n):
    """Simple moving average"""
    return pd.Series(array).rolling(n).mean()

class SmaCross(Strategy):
        n1 = 10
        n2 = 30

        def init(self):
            close = self.data.Close
            self.sma1 = self.I(SMA, close, self.n1)
            self.sma2 = self.I(SMA, close, self.n2)

        def next(self):
            if crossover(self.sma1, self.sma2):
                self.buy()
            elif crossover(self.sma2, self.sma1):
                self.sell()