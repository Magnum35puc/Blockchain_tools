from backtesting import Strategy
import pandas as pd

def RSI(array, n):
    result  = pd.Series(array).diff() / array[:,1:] 
    res = result * 100
    return res



class Pct_Change(Strategy):
        n1 = 10
        n2 = 20

        def init(self):
            close = self.data.Close
            self.sma1 = self.I(RSI, close, self.n1)
            self.sma2 = self.I(RSI, close, self.n2)

        def next(self):
            pass



