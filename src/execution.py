from src.events import FillEvent, EventType

class SimulatedExecutionHandler :
    """Converts ORDER -> FILL
    for now: fill orders immediatly at current bar close.
    Adds simple slippage and commission to be realistic."""

    def __init__ (self, slippage_bps: float = 2.0, commission : float = 1.0):
        self.slippage_bps = slippage_bps
        self.commission = commission

    def execute_order (self, order_event, market_event):
        price = market_event.close
        slip = price * (self.slippage_bps / 10000.0)

        fill_price = price + slip if order_event.direction == "BUY" else price - slip

        return FillEvent (
            type=EventType.FILL,
            symbol = order_event.symbol,
            dt = market_event.dt,
            direction= order_event.direction,
            quantity=order_event.quantity,
            fill_price=fill_price,
            commission=self.commission,
            slippage=slip,
        )
    