from collections import deque
import pandas as pd
from src.events import SignalEvent, EventType

class MovingAverageCrossStrategy:
    def __init__ (self, symbol: str, short_window: int = 2, long_window: int = 4):
        """using small window for the sample to actually see signals, 
        later to 20/50 for real data"""
        self.symbol = symbol
        self.short_window = short_window
        self.long_window = long_window
        self.prices = deque(maxlen=long_window + 5)
        self.in_position = False

    def on_market (self, market_event):
        self.prices.append(market_event.close)

        if len(self.prices) < self.long_window:
            return None

        s = pd.Series(self.prices)
        short_ma = s.tail(self.short_window).mean()
        long_ma = s.tail(self.long_window).mean()  

        if short_ma > long_ma and not self.in_position:
            self.in_position = True
            return SignalEvent(
                type = EventType.SIGNAL,
                symbol = self.symbol,
                dt = market_event.dt,
                signal= "LONG", 
                )

        if short_ma < long_ma and not self.in_position:
            self.in_position = False
            return SignalEvent(
                type = EventType.SIGNAL,
                symbol = self.symbol,
                dt = market_event.dt,
                signal= "EXIT", 
                )
        

        return None