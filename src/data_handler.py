import pandas as pd
from src.events import MarketEvent, EventType
import yfinance  as yf
from collections import deque

class CSVDataHandler: 
    """
    Streams one bar per cell as a MarketEvent.
    Expects CSV Columns: datetime,open,high,low,close,volume
    """

    def __init__(self, symbol: str, start = None, end = None, interval = "1d"):
        self.symbol = symbol
        self.interval = interval
        self.raw = yf.download(ticket = symbol, start = start , end = end, interval=interval, progress = False)
        self.df = self.raw.reset_index()
        self.idx = 0
        self.df = self.df.dropna().reset_index(drop = True)
        
    def has_next(self) -> bool :
        return self.idx < len(self.df)
    
    def stream_next(self) -> MarketEvent:
        """Return next MarketEvent and advance pointer"""
        row = self.df.iloc[self.idx]
        dt = row['Date'] if 'Date' in row.index else row.Name 
        me =  MarketEvent(
            type = EventType.MARKET,
            symbol=self.symbol,
            dt = pd.to_datetime(dt),
            open = float(row["Open"]),
            high = float(row["High"]),
            low = float(row["Low"]),
            close = float(row["Close"]),
            volume = int(row["Volume"]),
        )
        self.idx += 1
        return me