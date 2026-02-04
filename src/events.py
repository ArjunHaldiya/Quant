from dataclasses import dataclass
from enum import Enum, auto

class EventType(Enum) :
    MARKET = auto()
    SIGNAL = auto()
    ORDER = auto()
    FILL = auto()


@dataclass(frozen= True)
class Event:
    type: EventType

@dataclass(frozen=True)
class MarketEvent(Event):
    symbol :str
    dt: object
    open:float
    high: float
    low: float
    close: float
    volume: float

@dataclass(frozen=True)
class SignalEvent(Event):
    symbol:str
    dt: object
    signal : str #LONG,SHORT,EXIT
    strength : float = 1.0

@dataclass(frozen=True)
class OrderEvent(Event):
    symbol : str
    dt: object
    order_type: str #MKT
    direction: str #BUY OR SELL
    quantity : int

@dataclass(frozen=True)
class FillEvent(Event):
    symbol: str
    dt: object
    direction: str
    quantity: int
    fill_price : float
    commission: float = 0.0
    slippage: float = 0.0

