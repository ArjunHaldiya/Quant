from collections import deque
import pandas as pd
from src.events import SignalEvent, EventType


print("Strategy fiel : ", __file__)
class MovingAverageCrossStrategy:
    def __init__ (self, symbol: str, short_window: int = 2, long_window: int = 3):
        """using small window for the sample to actually see signals, 
        later to 20/50 for real data"""
        self.symbol = symbol
        self.short_window = short_window
        self.long_window = long_window
        self.prices = deque(maxlen=long_window + 5)
        self.in_position = False
        self.prev_relation = None


    def on_market(self, market_event):
        self.prices.append(market_event.close)

        if len(self.prices) < self.long_window:
            return None

        s = pd.Series(self.prices)
        short_ma = s.tail(self.short_window).mean()
        long_ma  = s.tail(self.long_window).mean()

        # robust relation with tolerance
        eps = 1e-9
        diff = short_ma - long_ma
        if diff > eps:
            relation = "ABOVE"
        elif diff < -eps:
            relation = "BELOW"
        else:
            relation = "EQUAL"

        print(
            #f"    [DEBUG] {market_event.dt} short_ma={short_ma:.2f} long_ma={long_ma:.2f} "
            f"relation={relation} prev={self.prev_relation} in_position={self.in_position}"
        )

        # first time: store state and wait
        if self.prev_relation is None:
            self.prev_relation = relation
            if relation == "ABOVE" and not self.in_position:
                self.in_position = True

                return SignalEvent(
                    type = EventType.SIGNAL,
                    symbol= self.symbol,
                    dt = market_event.dt,
                    signal= "LONG",
                )
            return None

        # CROSS UP: BELOW/EQUAL -> ABOVE
        if (self.prev_relation in ("BELOW", "EQUAL")) and (relation == "ABOVE") and (not self.in_position):
            self.in_position = True
            self.prev_relation = relation
            return SignalEvent(
                type=EventType.SIGNAL,
                symbol=self.symbol,
                dt=market_event.dt,
                signal="LONG",
            )

        # CROSS DOWN: ABOVE/EQUAL -> BELOW
        if (self.prev_relation in ("ABOVE", "EQUAL")) and (relation == "BELOW") and (self.in_position):
            self.in_position = False
            self.prev_relation = relation
            return SignalEvent(
                type=EventType.SIGNAL,
                symbol=self.symbol,
                dt=market_event.dt,
                signal="EXIT",
            )

        self.prev_relation = relation
        return None
