import pandas as pd
from src.events import MarketEvent, EventType

class CSVDataHandler: 
    """
    Streams one bar per cell as a MarketEvent.
    Expects CSV Columns: datetime,open,high,low,close,volume
    """

    def __init__(self, csv_path: str, symbol: str):
        self.symbol = symbol
        df = pd.read_csv(csv_path)
        if "datetime" not in df.columns:
            raise ValueError("CSV must contain a 'datatime' column")
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.sort_values("datetime").reset_index(drop=True)

        for c in ["open", "high", "low", "close", "volume"]:
            if c not in df.columns:
                df[c] = 0.0
        self.df = df
        self._i = 0
        self.length = len(df)

    def has_next(self) -> bool :
        return self._i < self.length
    
    def stream_next(self) -> MarketEvent:
        """Return next MarketEvent and advance pointer"""
        row = self.df.iloc[self._i]
        self._i +=1
        return MarketEvent(
            type = EventType.MARKET,
            symbol=self.symbol,
            dt = row["datetime"],
            open = float(row["open"]),
            high = float(row["high"]),
            low = float(row["low"]),
            close = float(row["close"]),
            volume = float(row.get("volume", 0.0)),
        )